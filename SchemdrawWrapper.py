from dataclasses import dataclass
import Network
from typing import Callable, Set, List, Tuple, Dict, Any, Type, TypeVar, Union
import schemdraw

class UnknownElement(Exception): pass

class VoltageSource(schemdraw.elements.sources.SourceV):
    def __init__(self, V: float, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._V = V
        self._name = name
        self.label(f'${self._name}$\n ${V}\\mathrm{{V}}$')

    @property
    def name(self) -> str:
        return self._name

    @property
    def V(self) -> float:
        return self._V

    def values(self) -> Dict[str, float]:
        return {'U' : self.V}

class RealVoltageSource(schemdraw.elements.sources.SourceV):
    def __init__(self, V: float, R: float, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._V = V
        self._R = R
        self._name = name
        self.label(f'${self._name}$\n ${V}\\mathrm{{V}} / {R}\\Omega$')

    @property
    def name(self) -> str:
        return self._name

    @property
    def V(self) -> float:
        return self._V

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    def values(self) -> Dict[str, float]:
        return {'U' : self.V, 'R' : self.R}

class CurrentSource(schemdraw.elements.sources.SourceI):
    def __init__(self, I: float, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._I = I
        self._name = name
        self.label(f'${self._name}$\n ${I}\\mathrm{{A}}$')

    @property
    def name(self) -> str:
        return self._name

    @property
    def I(self) -> float:
        return self._I

    def values(self) -> Dict[str, float]:
        return {'I' : self.I}

class RealCurrentSource(schemdraw.elements.sources.SourceI):
    def __init__(self, I: float, R: float, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._I = I
        self._R = R
        self._name = name
        self.label(f'${self._name}$\n ${I}\\mathrm{{A}} / {R}\\Omega$')

    @property
    def name(self) -> str:
        return self._name

    @property
    def I(self) -> float:
        return self._I

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    def values(self) -> Dict[str, float]:
        return {'I' : self.I, 'R' : self.R}

class Resistor(schemdraw.elements.twoterm.ResistorIEC):
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

class Line(schemdraw.elements.lines.Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        return ''

class Ground(schemdraw.elements.Ground):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        return 'Ground'

        
SchemdrawElement = TypeVar('SchemdrawElement', bound=schemdraw.elements.Element)
SchemdrawElementTranslator = Callable[[SchemdrawElement, Callable[[schemdraw.util.Point], int]], Tuple[Network.Branch, str]]

def real_current_source_translator(element: RealCurrentSource, node_mapper: Callable[[schemdraw.util.Point], int]) -> Tuple[Network.Branch, str]:
    n1, n2 = get_nodes(element)
    return Network.Branch(node_mapper(n1), node_mapper(n2), Network.real_current_source(element.I, element.R)), element.name

def line_translator(element: Line, node_mapper: Callable[[schemdraw.util.Point], int]) -> Tuple[Network.Branch, str]:
    n1, _ = get_nodes(element)
    return Network.Branch(node_mapper(n1), node_mapper(n1), Network.resistor(R=0)), element.name

def resistor_translator(element: Resistor, node_mapper: Callable[[schemdraw.util.Point], int]) -> Tuple[Network.Branch, str]:
    n1, n2 = get_nodes(element)
    return Network.Branch(node_mapper(n1), node_mapper(n2), Network.resistor(element.R)), element.name

def current_source_translator(element: CurrentSource, node_mapper: Callable[[schemdraw.util.Point], int]) -> Tuple[Network.Branch, str]:
    n1, n2 = get_nodes(element)
    return Network.Branch(node_mapper(n1), node_mapper(n2), Network.current_source(element.I)), element.name

def real_voltage_source_translator(element: RealVoltageSource, node_mapper: Callable[[schemdraw.util.Point], int]) -> Tuple[Network.Branch, str]:
    n1, n2 = get_nodes(element)
    return Network.Branch(node_mapper(n2), node_mapper(n1), Network.real_voltage_source(element.V, element.R)), element.name

def voltage_source_translator(element: VoltageSource, node_mapper: Callable[[schemdraw.util.Point], int]) -> Tuple[Network.Branch, str]:
    n1, n2 = get_nodes(element)
    return Network.Branch(node_mapper(n2), node_mapper(n1), Network.voltage_source(element.V)), element.name

element_translator : Dict[Type[schemdraw.elements.Element], SchemdrawElementTranslator] = {
    RealCurrentSource : real_current_source_translator,
    Resistor : resistor_translator,
    Line : line_translator,
    CurrentSource: current_source_translator,
    RealVoltageSource : real_voltage_source_translator,
    VoltageSource: voltage_source_translator,
}

element_type = {
    RealCurrentSource : "real_current_source",
    Resistor : "resistor",
    Line : "line",
    Ground : "ground",
    CurrentSource: "current_source",
    RealVoltageSource : "real_voltage_source",
    VoltageSource: "voltage_source",
}
    
def round_node(node: schemdraw.util.Point) -> schemdraw.util.Point:
    def local_round(x):
        return round(x, ndigits=2)
    return schemdraw.util.Point((local_round(node.x), local_round(node.y)))

def get_nodes(element: schemdraw.elements.Element) -> Tuple[schemdraw.util.Point, schemdraw.util.Point]:
    return round_node(element.absanchors['start']), round_node(element.absanchors['end'])

def get_node_direction(node1: schemdraw.util.Point, node2: schemdraw.util.Point) -> Tuple[int, int]:
    delta = node2 - node1
    delta_x = +1 if delta.x >= 0 else -1
    delta_y = +1 if delta.y >= 0 else -1
    return delta_x, delta_y

@dataclass(frozen=True)
class SchemdrawNetwork:
    drawing: schemdraw.Drawing

    @property
    def elements(self) -> List[schemdraw.elements.Element]:
        return self.drawing.elements

    @property
    def two_term_elements(self) -> List[schemdraw.elements.Element2Term]:
        return [e for e in self.elements if isinstance(e, schemdraw.elements.Element2Term)]

    @property
    def line_elements(self) -> List[schemdraw.elements.lines.Line]:
        return [e for e in self.two_term_elements if isinstance(e, schemdraw.elements.lines.Line)]

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
                for n in self.get_equal_electrical_potential_nodes(node).intersection(nodes):
                    nodes.remove(n)
                nodes.add(node)
        return nodes

    @property
    def ordered_unique_nodes(self) -> List[schemdraw.util.Point]:
        return list(self.unique_nodes)

    @property
    def unique_node_mapping(self) -> Dict[schemdraw.util.Point, schemdraw.util.Point]:
        node_mapping = {}
        for n in self.all_nodes:
            identical_nodes = self.get_equal_electrical_potential_nodes(n)
            identical_nodes.remove(n)
            current_unique_node = self.unique_nodes.intersection(identical_nodes)
            if len(current_unique_node) > 0:
                node_mapping.update({n: current_unique_node.pop()})
            else:
                node_mapping.update({n: n})
        return node_mapping

    @property
    def network(self) -> Network.Network:
        translator = lambda e : element_translator[type(e)](e, self.get_node_index)[0]
        return Network.Network([translator(e) for e in self.two_term_elements if type(e) is not Line])

    def get_equal_electrical_potential_nodes(self, node: schemdraw.util.Point) -> Set[schemdraw.util.Point]:
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

    def get_node_index(self, node: schemdraw.util.Point) -> int:
        return self.ordered_unique_nodes.index(self.unique_node_mapping[node])

    def get_element_from_name(self, name: str) -> schemdraw.elements.Element:
        elements = [e for e in self.two_term_elements if e.name == name]
        if len(elements) == 0:
            raise UnknownElement
        else:
            return elements[0]

    def get_branch_from_name(self, id: str) -> Network.Branch:
        element = self.get_element_from_name(id)
        return element_translator[type(element)](element, self.get_node_index)[0]

class SchemdrawSolution:

    def __init__(self, schemdraw_network: SchemdrawNetwork, solver: Network.NetworkSolver):
        self.schemdraw_network = schemdraw_network
        self.network_solution = solver(self.schemdraw_network.network)

    def draw_voltage(self, element_name: str, reverse: bool = False) -> schemdraw.Drawing:
        element = self.schemdraw_network.get_element_from_name(element_name)
        branch = self.schemdraw_network.get_branch_from_name(element_name)
        V_branch = self.network_solution.get_voltage(branch)
        if reverse:
            V_branch *= -1
        # adjust counting arrow system of voltage sources for display
        if type(element) is VoltageSource or type(element) is RealVoltageSource:
            reverse = not reverse
        # adjust missing direction information of CurrentLabel() method
        n1, n2 = get_nodes(element)
        dx, dy = get_node_direction(n1, n2)
        if dx < 0 or dy < 0:
            reverse = not reverse
        return schemdraw.elements.CurrentLabel(top=False, reverse=reverse).at(element).label(f'{V_branch:2.2f}V')

    def draw_current(self, element_name: str, reverse: bool = False, start: bool = True) -> schemdraw.Drawing:
        element = self.schemdraw_network.get_element_from_name(element_name)
        branch = self.schemdraw_network.get_branch_from_name(element_name)
        I_branch = self.network_solution.get_current(branch)
        # adjust counting arrow system of voltage sources for display
        if type(element) is VoltageSource or type(element) is RealVoltageSource:
            start = False
        if start is False:
            reverse = not reverse
        return schemdraw.elements.CurrentLabelInline(reverse=reverse, start=start).at(element).label(f'{I_branch:2.2f}A')
