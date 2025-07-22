from ..Circuit.solution import DCSolution, ComplexSolution, EmptySolution
from ..Circuit import solution as sol

from . import Elements as elm
from . import Display as dsp
from .DiagramTranslator import SchematicDiagramParser, circuit_translator

from dataclasses import dataclass, field
from typing import Protocol
import numpy as np

class DiagramSolution(Protocol):
    def get_voltage(self, name: str, reverse: bool) -> str:
        ...
    def get_current(self, name: str, reverse: bool) -> str:
        ...
    def get_power(self, name: str) -> str:
        ...
    def get_potential(self, name: str) -> str:
        ...
    @property
    def solution(self) -> object:
        ...

@dataclass
class EmptyDiagramSolution:
    solution: EmptySolution = field(default_factory=lambda: EmptySolution())
    def get_voltage(self, name: str, reverse: bool) -> str:
        return f'V[{name}]'
    def get_current(self, name: str, reverse: bool) -> str:
        return f'I[{name}]'
    def get_power(self, name: str) -> str:
        return f'P[{name}]'
    def get_potential(self, name: str) -> str:
        return f'φ[{name}]'

@dataclass
class TimeDomainSteadyStateDiagramSolution:
    solution: ComplexSolution
    deg: bool = False
    hertz: bool = False
    sin: bool = False
    precision: int = 3

    def get_voltage(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        v = self.solution.get_voltage(name)
        if np.isnan(v):
            return f'v[{name}](t)'
        return dsp.print_sinosoidal(
            value=sign*v,
            unit='V',
            precision=self.precision,
            w=self.solution.w,
            sin=self.sin,
            deg=self.deg,
            hertz=self.hertz
        )

    def get_current(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        i = self.solution.get_voltage(name)
        if np.isnan(i):
            return f'i[{name}](t)'
        return dsp.print_sinosoidal(
            value=sign*i,
            unit='A',
            precision=self.precision,
            w=self.solution.w,
            sin=self.sin,
            deg=self.deg,
            hertz=self.hertz
        )

    def get_power(self, name: str) -> str:
        p = self.solution.get_voltage(name)
        if np.isnan(p):
            return f'p[{name}](t)'
        return dsp.print_sinosoidal(
            value=self.solution.get_power(name),
            unit='W',
            precision=self.precision,
            w=self.solution.w,
            sin=self.sin,
            deg=self.deg,
            hertz=self.hertz
        )

    def get_potential(self, name: str) -> str:
        phi = self.solution.get_voltage(name)
        if np.isnan(phi):
            return f'φ[{name}](t)'
        return dsp.print_sinosoidal(
            value=self.solution.get_potential(name),
            unit='V',
            precision=self.precision,
            w=self.solution.w,
            sin=self.sin,
            deg=self.deg,
            hertz=self.hertz
        )

@dataclass
class ComplexNetworkDiagramSolution:
    solution: ComplexSolution
    deg: bool = False
    polar: bool = False
    precision: int = 3

    def get_voltage(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        v = self.solution.get_voltage(name)
        if np.isnan(v):
            return f'V({name})'
        return dsp.print_complex(
            value=sign*v,
            unit='V',
            precision=self.precision,
            polar=self.polar,
            deg=self.deg
        )

    def get_current(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        i = self.solution.get_current(name)
        if np.isnan(i):
            return f'I({name})'
        return dsp.print_complex(
            value=sign*i,
            unit='A',
            precision=self.precision,
            polar=self.polar,
            deg=self.deg
        )

    def get_power(self, name: str) -> str:
        s = self.solution.get_power(name)
        if np.isnan(s):
            return f'S({name})'
        return dsp.print_complex(
            value=s,
            unit='VA',
            precision=self.precision,
            polar=self.polar,
            deg=self.deg
        )

    def get_potential(self, name: str) -> str:
        phi = self.solution.get_potential(name)
        if np.isnan(phi):
            return f'φ({name})'
        return dsp.print_complex(
            value=phi,
            unit='V',
            precision=self.precision,
            polar=self.polar,
            deg=self.deg
        )

@dataclass
class RealNetworkDiagramSolution:
    solution: DCSolution
    precision: int = 3

    def get_voltage(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        v = self.solution.get_voltage(name)
        if np.isnan(v):
            return f'V({name})'
        return dsp.print_real(sign*v, unit='V', precision=self.precision)

    def get_current(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        i = self.solution.get_current(name)
        if np.isnan(i):
            return f'I({name})'
        return dsp.print_real(sign*i, unit='A', precision=self.precision)

    def get_power(self, name: str) -> str:
        p = self.solution.get_power(name)
        if np.isnan(p):
            return f'P({name})'
        return dsp.print_active_power(p, precision=self.precision)

    def get_potential(self, name: str) -> str:
        phi = self.solution.get_potential(name)
        if np.isnan(phi):
            return f'φ({name})'
        return dsp.print_real(phi, unit='V', precision=self.precision)

@dataclass
class SchematicDiagramSolution:
    diagram_parser: SchematicDiagramParser
    solution: DiagramSolution

    def draw_voltage(self, name: str, reverse: bool = False, offset: float = 0) -> elm.VoltageLabel:
        element = self.diagram_parser.get_element(name)
        vlabel = self.solution.get_voltage(name=name, reverse=reverse)
        return elm.VoltageLabel(element, vlabel=vlabel, reverse=reverse if not element.is_reverse else not reverse, color=dsp.blue, ofst=offset)

    def draw_current(self, name: str, reverse: bool = False, end: bool = False) -> elm.CurrentLabel:
        element = self.diagram_parser.get_element(name)
        ilabel = self.solution.get_current(name=name, reverse=reverse if not end else not reverse)
        return elm.CurrentLabel(element, ilabel=ilabel, reverse=reverse if not element.is_reverse else not reverse, start=not end, color=dsp.red)

    def draw_power(self, name: str, offset: float = 0) -> elm.PowerLabel:
        element = self.diagram_parser.get_element(name)
        plabel = self.solution.get_power(name=name)
        return elm.PowerLabel(element, plabel=plabel, color=dsp.green, offset=offset)

    def draw_potential(self, name: str, loc:str = '') -> elm.LabelNode:
        element = self.diagram_parser.get_element(name)
        phi_label = self.solution.get_potential(name=name)
        return elm.LabelNode(id_loc=loc, name=phi_label, at=element.absdrop[0], color=dsp.blue)

def empty_solution(schematic: elm.Schematic) -> SchematicDiagramSolution:
    return SchematicDiagramSolution(
        diagram_parser=SchematicDiagramParser(schematic),
        solution=EmptyDiagramSolution()
    )

def single_frequency_time_domain_steady_state_solution(schematic: elm.Schematic, w: float = 0, sin: bool = False, deg: bool = False, hertz: bool = False) -> SchematicDiagramSolution:
    digagram_parser = SchematicDiagramParser(schematic)
    solution = TimeDomainSteadyStateDiagramSolution(
        solution=sol.complex_solution(circuit=circuit_translator(schematic), w=w),
        deg=deg,
        hertz=hertz,
        sin=sin
    )
    return SchematicDiagramSolution(
        diagram_parser=digagram_parser,
        solution=solution
    )

def single_frequency_complex_solution(schematic: elm.Schematic, w: float = 0, precision: int = 3, polar: bool = False, deg: bool = False) -> SchematicDiagramSolution:
    diagram_parser = SchematicDiagramParser(schematic)
    solution = ComplexNetworkDiagramSolution(
        solution=sol.complex_solution(circuit=circuit_translator(schematic), w=w),
        deg=deg,
        polar=polar,
        precision=precision
    )
    return SchematicDiagramSolution(
        diagram_parser=diagram_parser,
        solution=solution,
    )

def complex_solution(schematic: elm.Schematic, precision: int = 3, polar: bool = False, deg: bool = False) -> SchematicDiagramSolution:
    diagram_parser = SchematicDiagramParser(schematic)
    solution = ComplexNetworkDiagramSolution(
        solution=sol.complex_solution(circuit=circuit_translator(schematic)),
        deg=deg,
        polar=polar,
        precision=precision
    )
    return SchematicDiagramSolution(
        diagram_parser=diagram_parser,
        solution=solution,
    )

def real_solution(schematic: elm.Schematic, precision: int = 3) -> SchematicDiagramSolution:
    diagram_parser = SchematicDiagramParser(schematic)
    solution = RealNetworkDiagramSolution(
        solution=sol.dc_solution(circuit=circuit_translator(schematic)),
        precision=precision
    )
    return SchematicDiagramSolution(
        diagram_parser=diagram_parser,
        solution=solution
    )