from dataclasses import dataclass
from Network import load_network
from typing import Set, List, Tuple, Dict, Any
import schemdraw
import schemdraw.elements as elm
import NodalAnalysis

class UnknownElement(Exception): pass

class RealCurrentSource(elm.sources.SourceI):
    def __init__(self, I: float, R: float, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._I = -I # generator counter arrow system
        self._R = R
        self._name = name
        self.label(f'${self._name}$\n ${I}\\mathrm{{A}} / {R}\\Omega$')

    @property
    def name(self) -> str:
        return self._name

    @property
    def current(self) -> float:
        return self._I

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    def values(self) -> Dict[str, float]:
        return {'I' : self.current, 'R' : self.R}

class Resistor(elm.twoterm.ResistorIEC):
    def __init__(self, R: float, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._R = R
        self._name = name
        self.label(f'${self._name}={self._R}\\Omega$')

    @property
    def name(self) -> str:
        return self._name

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    def values(self) -> Dict[str, float]:
        return {'R' : self._R}

class Line(elm.lines.Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        return ''

class Ground(elm.Ground):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        return 'Ground'

element_type = {
    RealCurrentSource : "real_current_source",
    Resistor : "resistor",
    Line : "line",
    Ground : "ground"
}
    
def round_node(node: schemdraw.util.Point) -> schemdraw.util.Point:
    def local_round(x):
        return round(x, ndigits=2)
    return schemdraw.util.Point((local_round(node.x), local_round(node.y)))

def get_nodes(element: schemdraw.elements.Element) -> Tuple[schemdraw.util.Point, schemdraw.util.Point]:
    return round_node(element.absanchors['start']), round_node(element.absanchors['end'])

def get_identical_nodes(node: schemdraw.util.Point, elements: List[schemdraw.elements.Element2Term]) -> Set[schemdraw.util.Point]:
    lines = [element for element in elements if element_type[type(element)] == "line"]
    identical_nodes = set()
    for line in lines:
        n1, n2 = get_nodes(line)
        if node == n1:
            identical_nodes.add(n2)
        elif node == n2:
            identical_nodes.add(n1)
    return identical_nodes

def get_node_direction(node1: schemdraw.util.Point, node2: schemdraw.util.Point) -> Tuple[int, int]:
    delta = node2 - node1
    delta_x = +1 if delta.x >= 0 else -1
    delta_y = +1 if delta.y >= 0 else -1
    return delta_x, delta_y

@dataclass(frozen=True)
class SchemdrawNetwork:
    drawing: schemdraw.Drawing

    @property
    def two_term_elements(self) -> List[schemdraw.elements.Element2Term]:
        return [e for e in self.drawing.elements if isinstance(e, schemdraw.elements.Element2Term)]

    @property
    def all_nodes(self) -> Set[schemdraw.util.Point]:
        nodes = {round_node(e.absanchors['start']) for e in self.two_term_elements}
        nodes = nodes.union({round_node(e.absanchors['end']) for e in self.two_term_elements})
        return nodes

    @property
    def unique_nodes(self) -> Set[schemdraw.util.Point]:
        nodes = self.all_nodes
        for node in self.all_nodes:
            if node in nodes:
                for n in get_identical_nodes(node, self.two_term_elements):
                    nodes.remove(n)
        return nodes

    @property
    def ordered_unique_nodes(self) -> List[schemdraw.util.Point]:
        return list(self.unique_nodes)

    @property
    def unique_node_mapping(self) -> Dict[schemdraw.util.Point, schemdraw.util.Point]:
        node_mapping = {}
        for n in self.all_nodes:
            identical_nodes = get_identical_nodes(n, self.two_term_elements)
            current_unique_node = self.unique_nodes.intersection(identical_nodes)
            if len(current_unique_node) > 0:
                node_mapping.update({n: current_unique_node.pop()})
            else:
                node_mapping.update({n: n})
        return node_mapping

    @property
    def dependency_list(self) -> List[Dict[str, Any]]:
        el = []
        elements = [e for e in self.two_term_elements if element_type[type(e)] != "line"]
        for e in elements:
            n1, n2 = get_nodes(e)
            d = {
                "type": element_type[type(e)],
                "id" : e.name,
                "N1" : self.get_node_index(n1),
                "N2" : self.get_node_index(n2)
            }
            d.update(e.values())
            el.append(d)
        return el

    def get_node_index(self, node: schemdraw.util.Point) -> int:
        return self.ordered_unique_nodes.index(self.unique_node_mapping[node])

    def get_element_from_name(self, name: str) -> schemdraw.elements.Element:
        elements = [e for e in self.two_term_elements if e.name == name]
        if len(elements) == 0:
            raise UnknownElement
        else:
            return elements[0]

def draw_voltage(schemdraw_network: SchemdrawNetwork, element_name: str, reverse: bool = False) -> schemdraw.Drawing:
    network = load_network(schemdraw_network.dependency_list)
    V = NodalAnalysis.calculate_branch_voltages(network)

    element = schemdraw_network.get_element_from_name(element_name)
    n1, n2 = get_nodes(element)
    i1, i2 = schemdraw_network.get_node_index(n1), schemdraw_network.get_node_index(n2)

    V_branch = NodalAnalysis.calculate_branch_voltage(V, i1, i2)
    if reverse:
        V_branch *= -1

    # adjust missing direction information of CurrentLabel() method
    dx, dy = get_node_direction(n1, n2)
    if dx < 0 or dy < 0:
        reverse = not reverse

    return elm.CurrentLabel(top=False, reverse=reverse).at(element).label(f'{V_branch:2.2f}V')

def draw_current(schemdraw_network: SchemdrawNetwork, element_name: str, reverse: bool = False) -> schemdraw.Drawing:
    network = load_network(schemdraw_network.dependency_list)
    V = NodalAnalysis.calculate_branch_voltages(network)

    element = schemdraw_network.get_element_from_name(element_name)
    n1, n2 = get_nodes(element)
    i1, i2 = schemdraw_network.get_node_index(n1), schemdraw_network.get_node_index(n2)

    V_branch = NodalAnalysis.calculate_branch_voltage(V, i1, i2)
    if reverse:
        V_branch *= -1
    I_branch = V_branch / element.R
    return elm.CurrentLabelInline(top=False, reverse=reverse).at(element).label(f'{I_branch:2.2f}A')