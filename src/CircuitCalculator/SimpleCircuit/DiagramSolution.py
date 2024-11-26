from ..Circuit.solution import ComplexSolution, DCSolution

from . import Elements as elm
from . import Display as dsp
from .DiagramTranslator import SchematicDiagramParser, circuit_translator

from dataclasses import dataclass
from typing import Protocol

class DiagramSolution(Protocol):
    def get_voltage(self, name: str, reverse: bool) -> str:
        ...
    def get_current(self, name: str, reverse: bool) -> str:
        ...
    def get_power(self, name: str, reverse: bool) -> str:
        ...
    def get_potential(self, name: str) -> str:
        ...

class EmptyDiagramSolution:
    def get_voltage(self, name: str, reverse: bool) -> str:
        return ''
    def get_current(self, name: str, reverse: bool) -> str:
        return ''
    def get_power(self, name: str, reverse: bool) -> str:
        return ''
    def get_potential(self, name: str) -> str:
        return ''

@dataclass
class TimeDomainSteadyStateDiagramSolution:
    solution: ComplexSolution
    deg: bool = False
    hertz: bool = False
    sin: bool = False
    precision: int = 3

    def get_voltage(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        return dsp.print_sinosoidal(
            value=sign*self.solution.get_voltage(name),
            unit='V',
            precision=self.precision,
            w=self.solution.w,
            sin=self.sin,
            deg=self.deg,
            hertz=self.hertz
        )

    def get_current(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        return dsp.print_sinosoidal(
            value=sign*self.solution.get_current(name),
            unit='A',
            precision=self.precision,
            w=self.solution.w,
            sin=self.sin,
            deg=self.deg,
            hertz=self.hertz
        )

    def get_power(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        return dsp.print_sinosoidal(
            value=sign*self.solution.get_power(name),
            unit='W',
            precision=self.precision,
            w=self.solution.w,
            sin=self.sin,
            deg=self.deg,
            hertz=self.hertz
        )

    def get_potential(self, name: str) -> str:
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
        return dsp.print_complex(
            value=sign*self.solution.get_voltage(name),
            unit='V',
            precision=self.precision,
            polar=self.polar,
            deg=self.deg
        )

    def get_current(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        return dsp.print_complex(
            value=sign*self.solution.get_current(name),
            unit='A',
            precision=self.precision,
            polar=self.polar,
            deg=self.deg
        )

    def get_power(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        return dsp.print_complex(
            value=sign*self.solution.get_power(name),
            unit='W',
            precision=self.precision,
            polar=self.polar,
            deg=self.deg
        )

    def get_potential(self, name: str) -> str:
        return dsp.print_complex(
            value=self.solution.get_potential(name),
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
        return dsp.print_real(sign*self.solution.get_voltage(name), unit='V', precision=self.precision)

    def get_current(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        return dsp.print_real(sign*self.solution.get_current(name), unit='A', precision=self.precision)

    def get_power(self, name: str, reverse: bool) -> str:
        sign = -1 if reverse else 1
        return dsp.print_active_power(sign*self.solution.get_power(name), precision=self.precision)

    def get_potential(self, name: str) -> str:
        return dsp.print_real(self.solution.get_potential(name), unit='V', precision=self.precision)

@dataclass
class SchematicDiagramSolution:
    diagram_parser: SchematicDiagramParser
    solution: DiagramSolution

    def draw_voltage(self, name: str, reverse: bool = False) -> elm.VoltageLabel:
        element = self.diagram_parser.get_element(name)
        vlabel = self.solution.get_voltage(name=name, reverse=reverse)
        return elm.VoltageLabel(element, vlabel=vlabel, reverse=reverse if not element.is_reverse else not reverse, color=dsp.blue)

    def draw_current(self, name: str, reverse: bool = False, end: bool = False) -> elm.CurrentLabel:
        element = self.diagram_parser.get_element(name)
        ilabel = self.solution.get_current(name=name, reverse=reverse if not end else not reverse)
        return elm.CurrentLabel(element, ilabel=ilabel, reverse=reverse if not element.is_reverse else not reverse, start=not end, color=dsp.red)

    def draw_power(self, name: str, reverse: bool = False) -> elm.PowerLabel:
        element = self.diagram_parser.get_element(name)
        plabel = self.solution.get_power(name=name, reverse=reverse)
        return elm.PowerLabel(element, plabel=plabel, color=dsp.green)

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
        solution=ComplexSolution(circuit=circuit_translator(schematic), w=w),
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
        solution=ComplexSolution(circuit=circuit_translator(schematic), w=w),
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
        solution=ComplexSolution(circuit=circuit_translator(schematic)),
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
        solution=DCSolution(circuit=circuit_translator(schematic)),
        precision=precision
    )
    return SchematicDiagramSolution(
        diagram_parser=diagram_parser,
        solution=solution
    )