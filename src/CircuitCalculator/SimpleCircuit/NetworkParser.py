from dataclasses import dataclass
from schemdraw import elements, util
from . import Elements as elm
from .ElementTranslators import element_translator, round_node, get_nodes, translator_available, SchemdrawElementTranslator
from .Display import red, blue, print_voltage, print_current
from ..Network.network import Network, Branch
from ..Network.solution import NetworkSolver

class UnknownElement(Exception): pass
class MultipleGroundNodes(Exception): pass

def get_node_direction(node1: util.Point, node2: util.Point) -> tuple[int, int]:
    delta = node2 - node1
    delta_x = +1 if delta.x >= 0 else -1
    delta_y = +1 if delta.y >= 0 else -1
    return delta_x, delta_y

@dataclass(frozen=True)
class NetworkDiagramParser:
    drawing: elm.Schematic

    @property
    def all_elements(self) -> list[elements.Element]:
        return self.drawing.elements

    @property
    def circuit_elements(self) -> list[elements.Element]:
        return [e for e in self.all_elements if translator_available(e)]

    @property
    def line_elements(self) -> list[elm.Line]:
        return [e for e in self.all_elements if type(e) is elm.Line]
    
    @property
    def node_elements(self) -> list[elm.Node]:
        return [e for e in self.all_elements if isinstance(e, elm.Node)]

    @property
    def all_nodes(self) -> set[util.Point]:
        nodes = {round_node(e.absanchors['start']) for e in self.circuit_elements}
        nodes = nodes.union({round_node(e.absanchors['end']) for e in self.circuit_elements})
        nodes = nodes.union({round_node(e.absanchors['start']) for e in self.line_elements})
        nodes = nodes.union({round_node(e.absanchors['end']) for e in self.line_elements})
        return nodes

    @property
    def unique_nodes(self) -> set[util.Point]:
        nodes = self.all_nodes
        for node in self.all_nodes:
            if node in nodes:
                for n in self._get_equal_electrical_potential_nodes(node).intersection(nodes):
                    nodes.remove(n)
                nodes.add(node)
        return nodes

    @property
    def node_label_mapping(self) -> dict[util.Point, str]:
        node_labels = {self.unique_node_mapping[get_nodes(e)[0]] : e.node_id for e in self.node_elements}
        node_index = len(node_labels)+1
        unlabeled_nodes = [p for p in self.unique_nodes if p not in node_labels.keys()]
        for p in unlabeled_nodes:
            while str(node_index) in node_labels.values():
                node_index += 1
            node_labels.update({p : str(node_index)})
        return node_labels

    @property
    def unique_node_mapping(self) -> dict[util.Point, util.Point]:
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
    def ground(self) -> util.Point:
        ground_nodes = [n for n in self.node_elements if type(n) == elm.Ground]
        if len(ground_nodes) > 1:
            raise MultipleGroundNodes
        if len(ground_nodes) == 0:
            return list(self.unique_nodes)[0]
        else:
            return get_nodes(ground_nodes[0])[0]

    @property
    def network(self) -> Network:
        def translator(e) -> Branch:
            return element_translator[type(e)](e, self._get_node_index)
        return Network(
            branches=[translator(e) for e in self.all_elements if translator_available(e)],
            zero_node_label=self._get_node_index(self.ground)
            )

    def _get_equal_electrical_potential_nodes(self, node: util.Point) -> set[util.Point]:
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

    def _get_node_index(self, node: util.Point) -> str:
        return self.node_label_mapping[self.unique_node_mapping[node]]

    def get_element(self, name: str) -> elements.Element:
        elements = [e for e in self.circuit_elements if e.name == name]
        if len(elements) == 0:
            raise UnknownElement
        else:
            return elements[0]

    def get_branch(self, id: str) -> Branch:
        element = self.get_element(id)
        return element_translator[type(element)](element, self._get_node_index)

class SchemdrawSolution:

    def __init__(self, schemdraw_network: NetworkDiagramParser, solver: NetworkSolver):
        self.schemdraw_network = schemdraw_network
        self.network_solution = solver(self.schemdraw_network.network)

    def draw_voltage(self, name: str, reverse: bool = False, precision: int = 3, top: bool = False) -> elm.VoltageLabel:
        element = self.schemdraw_network.get_element(name)
        branch = self.schemdraw_network.get_branch(name)
        V_branch = self.network_solution.get_voltage(branch.id)
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
        return elm.VoltageLabel(element, label=f'{print_voltage(V_branch, precision=precision)}V', reverse=reverse, color=blue, top=top)

    def draw_current(self, element_name: str, reverse: bool = False, start: bool = True, ofst: float = 0, precision=3) -> elm.CurrentLabel:
        element = self.schemdraw_network.get_element(element_name)
        branch = self.schemdraw_network.get_branch(element_name)
        I_branch = self.network_solution.get_current(branch.id)
        if reverse:
            I_branch *= -1
        # adjust counting arrow system of voltage sources for display
        # if type(element) is elm.VoltageSource or type(element) is elm.RealVoltageSource:
        #     start = False
        # if start is False:
        #     reverse = not reverse
        return elm.CurrentLabel(element, label=f'{print_current(I_branch, precision=precision)}A', reverse=reverse, start=start, color=red, ofst=ofst)
