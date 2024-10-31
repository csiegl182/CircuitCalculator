from ..Network.solution import NetworkSolver, NetworkSolution
from ..Network.NodalAnalysis.bias_point_analysis import nodal_analysis_bias_point_solver
from ..Circuit.solution import ComplexSolution, DCSolution

from . import Elements as elm
from . import Display as dsp
from .DiagramTranslator import SchematicDiagramParser, circuit_translator

from dataclasses import dataclass
from typing import Callable
from functools import partial

class UnknownElement(Exception): pass
class MultipleGroundNodes(Exception): pass
class UnknownTranslator(Exception): pass

@dataclass
class SchematicDiagramSolution:
    diagram_parser: SchematicDiagramParser
    solution: ComplexSolution | NetworkSolution
    voltage_display: Callable[[complex], str]
    current_display: Callable[[complex], str]
    power_display: Callable[[complex], str]

    def draw_voltage(self, name: str, reverse: bool = False) -> elm.VoltageLabel:
        element = self.diagram_parser.get_element(name)
        V_branch = self.solution.get_voltage(name)
        if reverse:
            V_branch *= -1
        return elm.VoltageLabel(element, vlabel=self.voltage_display(V_branch), reverse=reverse if not element.is_reverse else not reverse, color=dsp.blue)

    def draw_current(self, name: str, reverse: bool = False, end: bool = False) -> elm.CurrentLabel:
        element = self.diagram_parser.get_element(name)
        I_branch = self.solution.get_current(name)
        if reverse:
            I_branch *= -1
        if end:
            reverse = not reverse
        return elm.CurrentLabel(element, ilabel=self.current_display(I_branch), reverse=reverse if not element.is_reverse else not reverse, start=not end, color=dsp.red)

    def draw_power(self, name: str, reverse: bool = False) -> elm.PowerLabel:
        element = self.diagram_parser.get_element(name)
        P_branch = self.solution.get_power(name)
        return elm.PowerLabel(element, plabel=self.power_display(P_branch), color=dsp.green)

    def draw_potential(self, name: str, loc:str = '') -> elm.LabelNode:
        element = self.diagram_parser.get_element(name)
        node_potential = self.solution.get_potential(node_id=name)
        return elm.LabelNode(id_loc=loc, name=self.voltage_display(node_potential), at=element.absdrop[0], color=dsp.blue)

def time_domain_steady_state_solution(schematic: elm.Schematic, solver: NetworkSolver = nodal_analysis_bias_point_solver, w: float = 0, sin: bool = False, deg: bool = False, hertz: bool = False) -> SchematicDiagramSolution:
    digagram_parser = SchematicDiagramParser(schematic)
    solution = ComplexSolution(circuit=circuit_translator(schematic), solver=solver, w=w)
    return SchematicDiagramSolution(
        diagram_parser=digagram_parser,
        solution=solution,
        voltage_display=partial(dsp.print_sinosoidal, unit='V', w=w, sin=sin, deg=deg, hertz=hertz),
        current_display=partial(dsp.print_sinosoidal, unit='A', w=w, sin=sin, deg=deg, hertz=hertz),
        power_display=dsp.print_active_reactive_power
    )

def single_frequency_solution(schematic: elm.Schematic, solver: NetworkSolver = nodal_analysis_bias_point_solver, w: float = 0, precision: int = 3, polar: bool = False, deg: bool = False) -> SchematicDiagramSolution:
    diagram_parser = SchematicDiagramParser(schematic)
    solution = ComplexSolution(circuit=circuit_translator(schematic), solver=solver, w=w)
    return SchematicDiagramSolution(
        diagram_parser=diagram_parser,
        solution=solution,
        voltage_display=partial(dsp.print_complex, unit='V', precision=precision, polar=polar, deg=deg),
        current_display=partial(dsp.print_complex, unit='A', precision=precision, polar=polar, deg=deg),
        power_display=partial(dsp.print_complex, unit='VA', precision=precision, polar=polar, deg=deg)
    )

def complex_network_dc_solution(schematic: elm.Schematic, solver: NetworkSolver = nodal_analysis_bias_point_solver, precision: int = 3) -> SchematicDiagramSolution:
    diagram_parser = SchematicDiagramParser(schematic)
    solution = ComplexSolution(circuit=circuit_translator(schematic), solver=solver)
    return SchematicDiagramSolution(
        diagram_parser=diagram_parser,
        solution=solution,
        voltage_display=partial(dsp.print_complex, unit='V', precision=precision),
        current_display=partial(dsp.print_complex, unit='A', precision=precision),
        power_display=partial(dsp.print_complex, unit='VA', precision=precision)
    )

def real_network_dc_solution(schematic: elm.Schematic, solver: NetworkSolver = nodal_analysis_bias_point_solver, precision: int = 3) -> SchematicDiagramSolution:
    diagram_parser = SchematicDiagramParser(schematic)
    solution = DCSolution(circuit=circuit_translator(schematic), solver=solver)
    return SchematicDiagramSolution(
        diagram_parser=diagram_parser,
        solution=solution,
        voltage_display=partial(dsp.print_real, unit='V', precision=precision),
        current_display=partial(dsp.print_real, unit='A', precision=precision),
        power_display=lambda x: dsp.print_active_power(x.real, precision=precision)
    )