from dataclasses import dataclass
import schemdraw.elements, schemdraw.util
from . import Elements as elm
from .NetworkBranchTranslators import network_translator_map
from .CircuitComponentTranslators import circuit_translator_map
from .Display import red, blue, print_voltage, print_current
from ..Network.network import Network
from ..Network.solution import NetworkSolution
from .SchemdrawTranslatorTypes import ElementTranslatorMap
from ..Circuit.circuit import Circuit
from typing import Any

class UnknownElement(Exception): pass
class MultipleGroundNodes(Exception): pass

def get_node_direction(node1: schemdraw.util.Point, node2: schemdraw.util.Point) -> tuple[int, int]:
    delta = node2 - node1
    delta_x = +1 if delta.x >= 0 else -1
    delta_y = +1 if delta.y >= 0 else -1
    return delta_x, delta_y

def round_node(node: schemdraw.util.Point) -> schemdraw.util.Point:
    def local_round(x):
        return round(x, ndigits=2)
    return schemdraw.util.Point((local_round(node.x), local_round(node.y)))

def get_nodes(element: schemdraw.elements.Element, n_labels: tuple[str, ...]=('start', 'end')) -> list[schemdraw.util.Point]:
    return [round_node(element.absanchors[n_label]) for n_label in n_labels]

@dataclass(frozen=True)
class SchematicDiagramAnalyzer:
    drawing: elm.Schematic

    @property
    def all_elements(self) -> list[schemdraw.elements.Element]:
        return self.drawing.elements

    @property
    def circuit_elements(self) -> list[schemdraw.elements.Element]:
        def has_name_property(e: schemdraw.elements.Element):
            try:
                _ = e.name
            except AttributeError:
                return False
            return True
        return [e for e in self.all_elements if has_name_property(e)]

    @property
    def line_elements(self) -> list[elm.Line]:
        return [e for e in self.all_elements if type(e) is elm.Line]
    
    @property
    def node_elements(self) -> list[elm.Node]:
        return [e for e in self.all_elements if isinstance(e, elm.Node)]

    @property
    def all_nodes(self) -> set[schemdraw.util.Point]:
        nodes = {round_node(e.absanchors['start']) for e in self.circuit_elements}
        nodes = nodes.union({round_node(e.absanchors['end']) for e in self.circuit_elements})
        nodes = nodes.union({round_node(e.absanchors['start']) for e in self.line_elements})
        nodes = nodes.union({round_node(e.absanchors['end']) for e in self.line_elements})
        return nodes

    @property
    def unique_nodes(self) -> set[schemdraw.util.Point]:
        nodes = self.all_nodes
        for node in self.all_nodes:
            if node in nodes:
                for n in self._get_equal_electrical_potential_nodes(node).intersection(nodes):
                    nodes.remove(n)
                nodes.add(node)
        return nodes

    @property
    def node_label_mapping(self) -> dict[schemdraw.util.Point, str]:
        node_labels = {self.unique_node_mapping[get_nodes(e)[0]] : e.node_id for e in self.node_elements}
        node_index = len(node_labels)+1
        unlabeled_nodes = [p for p in self.unique_nodes if p not in node_labels.keys()]
        for p in unlabeled_nodes:
            while str(node_index) in node_labels.values():
                node_index += 1
            node_labels.update({p : str(node_index)})
        return node_labels

    @property
    def unique_node_mapping(self) -> dict[schemdraw.util.Point, schemdraw.util.Point]:
        node_mapping = {}
        for n in self.all_nodes:
            identical_nodes = self._get_equal_electrical_potential_nodes(n)
            identical_nodes.remove(n)
            current_unique_node = self.unique_nodes.intersection(identical_nodes)
            if len(current_unique_node) > 0:
                node_mapping.update({n: current_unique_node.pop()})
            else:
                node_mapping.update({n: n})
        return node_mapping

    @property
    def ground(self) -> schemdraw.util.Point:
        ground_nodes = [n for n in self.node_elements if type(n) == elm.Ground]
        if len(ground_nodes) > 1:
            raise MultipleGroundNodes
        if len(ground_nodes) == 0:
            return list(self.unique_nodes)[0]
        else:
            return get_nodes(ground_nodes[0])[0]

    @property
    def ground_label(self) -> str:
        return self._get_node_index(self.ground)

    def translate_elements(self, translator_map : ElementTranslatorMap) -> list[Any]:
        def translate(element: schemdraw.elements.Element) -> Any:
            return translator_map[type(element)](element, tuple(map(self._get_node_index, get_nodes(element))))
        def translator_available(element: schemdraw.elements.Element) -> bool:
            return type(element) in translator_map.keys()
        return [translate(e) for e in self.all_elements if translator_available(e)]

    def _get_equal_electrical_potential_nodes(self, node: schemdraw.util.Point) -> set[schemdraw.util.Point]:
        equal_electrical_potential_nodes = set([node])
        old_length = 0
        while len(equal_electrical_potential_nodes) > old_length:
            old_length = len(equal_electrical_potential_nodes)
            for line in self.line_elements:
                n1, n2 = get_nodes(line)
                if n1 in equal_electrical_potential_nodes:
                    equal_electrical_potential_nodes.add(n2)
                elif n2 in equal_electrical_potential_nodes:
                    equal_electrical_potential_nodes.add(n1)
        return equal_electrical_potential_nodes

    def _get_node_index(self, node: schemdraw.util.Point) -> str:
        return self.node_label_mapping[self.unique_node_mapping[node]]

    def get_element(self, name: str) -> schemdraw.elements.Element:
        elements = [e for e in self.circuit_elements if e.name == name]
        if len(elements) == 0:
            raise UnknownElement(f'Element {name} not known')
        else:
            return elements[0]

def network_parser(schematic: elm.Schematic) -> Network:
    schematic_diagram = SchematicDiagramAnalyzer(schematic)
    return Network(
        branches=schematic_diagram.translate_elements(network_translator_map),
        zero_node_label=schematic_diagram.ground_label
    )

def circuit_parser(schematic: elm.Schematic) -> Circuit:
    schematic_diagram = SchematicDiagramAnalyzer(schematic)
    return schematic_diagram.translate_elements(circuit_translator_map)

@dataclass
class SchematicDiagramSolution:
    diagram_parser: SchematicDiagramAnalyzer
    solution: NetworkSolution

    def draw_voltage(self, name: str, reverse: bool = False, precision: int = 3) -> elm.VoltageLabel:
        element = self.diagram_parser.get_element(name)
        V_branch = self.solution.get_voltage(name)
        if reverse:
            V_branch *= -1
        # adjust counting arrow system of voltage sources for display
        if type(element) is elm.VoltageSource or type(element) is elm.RealVoltageSource:
            reverse = not reverse
        # adjust missing direction information of CurrentLabel() method
        n1, n2 = get_nodes(element)
        dx, dy = get_node_direction(n1, n2)
        if dx < 0 or dy < 0:
            reverse = not reverse
        v_label_args = elm.v_label_args.get(type(element), {})
        return elm.VoltageLabel(element, label=f'{print_voltage(V_branch, precision=precision)}', reverse=reverse, color=blue, **v_label_args)

    def draw_current(self, name: str, reverse: bool = False, end: bool = False, precision=3) -> elm.CurrentLabel:
        element = self.diagram_parser.get_element(name)
        I_branch = self.solution.get_current(name)
        if reverse:
            I_branch *= -1
        if end:
            reverse = not reverse
        i_label_args = elm.i_label_args.get(type(element), {})
        return elm.CurrentLabel(element, label=f'{print_current(I_branch, precision=precision)}', reverse=reverse, start=not end, color=red, **i_label_args)
