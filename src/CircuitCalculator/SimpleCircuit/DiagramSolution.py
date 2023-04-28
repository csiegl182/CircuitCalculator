from ..Network.solution import NetworkSolution

from . import Elements as elm
from . import Display as dsp
from .DiagramParser import SchematicDiagramParser, get_nodes, get_node_direction

from dataclasses import dataclass
from typing import Callable
from functools import partial

class UnknownElement(Exception): pass
class MultipleGroundNodes(Exception): pass
class UnknownTranslator(Exception): pass

@dataclass
class SchematicDiagramSolution:
    diagram_parser: SchematicDiagramParser
    solution: NetworkSolution
    voltage_display: Callable[[complex], str]
    current_display: Callable[[complex], str]
    power_display: Callable[[complex], str]

    def draw_voltage(self, name: str, reverse: bool = False) -> elm.VoltageLabel:
        element = self.diagram_parser.get_element(name)
        V_branch = self.solution.get_voltage(name)
        if reverse:
            V_branch *= -1
        # adjust counting arrow system of voltage sources for display
        if type(element) is elm.VoltageSource or type(element) is elm.RealVoltageSource:
            reverse = not reverse
        # adjust missing direction information of CurrentLabel() method | TODO: Diese Funktion muss in VoltageLabel rein
        n1, n2 = get_nodes(element) # TODO: Nach Elements
        dx, dy = get_node_direction(n1, n2)
        if dx < 0 or dy < 0:
            reverse = not reverse
        return elm.VoltageLabel(element, label=self.voltage_display(V_branch), reverse=reverse, color=dsp.blue)

    def draw_current(self, name: str, reverse: bool = False, end: bool = False) -> elm.CurrentLabel:
        element = self.diagram_parser.get_element(name)
        I_branch = self.solution.get_current(name)
        if reverse:
            I_branch *= -1
        if end:
            reverse = not reverse
        return elm.CurrentLabel(element, label=self.current_display(I_branch), reverse=reverse, start=not end, color=dsp.red)

    def draw_power(self, name: str, reverse: bool = False) -> elm.PowerLabel:
        element = self.diagram_parser.get_element(name)
        P_branch = self.solution.get_power(name)
        return elm.PowerLabel(element, label=self.power_display(P_branch), color=dsp.green)

def time_domain_solution(digagram_parser: SchematicDiagramParser, solution: NetworkSolution, w: float = 0, sin: bool = False, deg: bool = False, hertz: bool = False) -> SchematicDiagramSolution:
    return SchematicDiagramSolution(
        diagram_parser=digagram_parser,
        solution=solution,
        voltage_display=partial(dsp.print_sinosoidal, unit='V', w=w, sin=sin, deg=deg, hertz=hertz),
        current_display=partial(dsp.print_sinosoidal, unit='A', w=w, sin=sin, deg=deg, hertz=hertz),
        power_display=dsp.print_active_reactive_power
    )

def complex_solution(digagram_parser: SchematicDiagramParser, solution: NetworkSolution, precision: int = 3, polar: bool = False, deg: bool = False) -> SchematicDiagramSolution:
    return SchematicDiagramSolution(
        diagram_parser=digagram_parser,
        solution=solution,
        voltage_display=partial(dsp.print_complex, unit='V', precision=precision, polar=polar, deg=deg),
        current_display=partial(dsp.print_complex, unit='A', precision=precision, polar=polar, deg=deg),
        power_display=partial(dsp.print_complex, unit='VA', precision=precision, polar=polar, deg=deg)
    )