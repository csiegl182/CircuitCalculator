from dataclasses import dataclass
from .Network import NetworkSolver, Network, Branch, resistor, current_source, real_current_source, voltage_source, real_voltage_source
from typing import Callable, Type, TypeVar 
import schemdraw
from .Utils import scientific_float

blue = '#02468F'
red = '#D20000'

class UnknownElement(Exception): pass
class MultipleGroundNodes(Exception): pass

def print_current(I: complex, precision: int = 3) -> str:
    real_part = scientific_float(I.real, precision=precision, use_exp_prefix=True, exp_prefixes={-6: 'u', -3: 'm', 3: 'k'})
    if I.imag/precision < 1:
        return real_part
    else:
        imag_part = scientific_float(I.imag, precision=precision, use_exp_prefix=True, exp_prefixes={-6: 'u', -3: 'm', 3: 'k'})
        return f'{real_part} + j{imag_part}'

def print_voltage(V: complex, precision: int = 3) -> str:
    real_part = scientific_float(V.real, precision=precision, use_exp_prefix=True, exp_prefixes={-6: 'u', -3: 'm', 3: 'k'})
    if V.imag/precision < 1:
        return real_part
    else:
        imag_part = scientific_float(V.imag, precision=precision, use_exp_prefix=True, exp_prefixes={-6: 'u', -3: 'm', 3: 'k'})
        return f'{real_part} + j{imag_part}'

class VoltageSource(schemdraw.elements.sources.SourceV):
    def __init__(self, V: float, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        if reverse:
            self._V = -V
        else:
            self._V = V
        self._name = name
        self.label(f'{self._name}={print_voltage(V, precision=precision)}V', rotate=True)

        a, b = (1.5, 0.7), (-0.5, 0.7)
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=blue))

    @property
    def name(self) -> str:
        return self._name

    @property
    def V(self) -> float:
        return self._V

    def values(self) -> dict[str, float]:
        return {'U' : self.V}

class RealVoltageSource(schemdraw.elements.sources.SourceV):
    def __init__(self, V: float, R: float, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        if reverse:
            self._V = -V
        else:
            self._V = V
        self._R = R
        self._name = name
        self.label(f'{self._name} {print_voltage(V, precision=precision)}V / {R}$\\Omega$')

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

    def values(self) -> dict[str, float]:
        return {'U' : self.V, 'R' : self.R}

class CurrentSource(schemdraw.elements.sources.SourceI):
    def __init__(self, I: float, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        if reverse:
            self._I = -I
        else:
            self._I = I
        self._name = name
        self.label(f'{self._name}={print_current(I, precision=precision)}A', rotate=True)

        a, b = (1.2, -0.3), (1.8, -0.3)
        self.segments.append(schemdraw.Segment((a, b), arrow='->', arrowwidth=.3, arrowlength=.4, color=red))

    @property
    def name(self) -> str:
        return self._name

    @property
    def I(self) -> float:
        return self._I

    def values(self) -> dict[str, float]:
        return {'I' : self.I}

class RealCurrentSource(schemdraw.elements.sources.SourceI):
    def __init__(self, I: float, R: float, name: str, *args, reverse=False, precision=3, **kwargs):
        super().__init__(*args, reverse=reverse, **kwargs)
        if reverse:
            self._I = -I
        else:
            self._I = I
        self._R = R
        self._name = name
        self.label(f'{self._name} {print_current(I)}A / {R}$\\Omega$')

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

    def values(self) -> dict[str, float]:
        return {'I' : self.I, 'R' : self.R}

class Resistor(schemdraw.elements.twoterm.ResistorIEC):
    def __init__(self, R: float, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._R = R
        self._name = name
        self.label(f'{self._name}={self._R}$\\Omega$', rotate=True)

    @property
    def name(self) -> str:
        return self._name

    @property
    def R(self) -> float:
        return self._R

    @property
    def G(self) -> float:
        return 1/self._R

    def values(self) -> dict[str, float]:
        return {'R' : self._R}

class Line(schemdraw.elements.lines.Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        return ''

class Node(schemdraw.elements.Element):
    def __init__(self, id: str = '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_id = id
        self.params['theta'] = 0
        self.params['drop'] = (0, 0)
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)

    @property
    def name(self) -> str:
        return f'Node {self.node_id}'

class LabelNode(Node):
    def __init__(self, id : str = '', id_loc : str = '', *args, **kwargs):
        super().__init__(id, *args, **kwargs)
        self.segments.append(schemdraw.SegmentCircle([0, 0], 0.12, fill='black'))
        if id_loc != '':
            if id_loc == 'W':
                label_param = {'loc': 'left', 'align': ['right', 'center']}
            elif id_loc == 'N':
                label_param = {'loc': 'top', 'align': ['center', 'bottom']}
            elif id_loc == 'E':
                label_param = {'loc': 'right', 'align': ['left', 'center']}
            else: # id_loc == 'S'
                label_param = {'loc': 'bottom', 'align': ['center', 'top']}
            self.bbox = self.get_bbox(includetext=False)
            self.add_label(f'{self.node_id}', **label_param)

    @property
    def name(self) -> str:
        return f'Node {self.node_id}'

class Ground(Node):
    def __init__(self, id: str = '0', *args, **kwargs):
        super().__init__(id, *args, **kwargs)
        gndgap = 0.12
        gnd_lead = 0.4
        resheight = schemdraw.elements.twoterm.resheight
        gap = schemdraw.elements.twoterm.gap
        self.segments.append(schemdraw.Segment(
            [(0, 0), (0, -gnd_lead), (-resheight, -gnd_lead),
             (resheight, -gnd_lead), gap, (-resheight*.7, -gndgap-gnd_lead),
             (resheight*.7, -gndgap-gnd_lead), gap,
             (-resheight*.2, -gndgap*2-gnd_lead),
             (resheight*.2, -gndgap*2-gnd_lead)]))

    @property
    def name(self) -> str:
        return 'Ground'
        
SchemdrawElement = TypeVar('SchemdrawElement', bound=schemdraw.elements.Element)
SchemdrawElementTranslator = Callable[[SchemdrawElement, Callable[[schemdraw.util.Point], str]], tuple[Branch, str]]

def real_current_source_translator(element: RealCurrentSource, node_mapper: Callable[[schemdraw.util.Point], str]) -> tuple[Branch, str]:
    n1, n2 = get_nodes(element)
    return Branch(node_mapper(n1), node_mapper(n2), real_current_source(element.I, element.R)), element.name

def line_translator(element: Line, node_mapper: Callable[[schemdraw.util.Point], str]) -> tuple[Branch, str]:
    n1, _ = get_nodes(element)
    return Branch(node_mapper(n1), node_mapper(n1), resistor(R=0)), element.name

def resistor_translator(element: Resistor, node_mapper: Callable[[schemdraw.util.Point], str]) -> tuple[Branch, str]:
    n1, n2 = get_nodes(element)
    return Branch(node_mapper(n1), node_mapper(n2), resistor(element.R)), element.name

def current_source_translator(element: CurrentSource, node_mapper: Callable[[schemdraw.util.Point], str]) -> tuple[Branch, str]:
    n1, n2 = get_nodes(element)
    return Branch(node_mapper(n1), node_mapper(n2), current_source(element.I)), element.name

def real_voltage_source_translator(element: RealVoltageSource, node_mapper: Callable[[schemdraw.util.Point], str]) -> tuple[Branch, str]:
    n1, n2 = get_nodes(element)
    return Branch(node_mapper(n2), node_mapper(n1), real_voltage_source(element.V, element.R)), element.name

def voltage_source_translator(element: VoltageSource, node_mapper: Callable[[schemdraw.util.Point], str]) -> tuple[Branch, str]:
    n1, n2 = get_nodes(element)
    return Branch(node_mapper(n2), node_mapper(n1), voltage_source(element.V)), element.name

element_translator : dict[Type[schemdraw.elements.Element], SchemdrawElementTranslator] = {
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

def get_nodes(element: schemdraw.elements.Element) -> tuple[schemdraw.util.Point, schemdraw.util.Point]:
    return round_node(element.absanchors['start']), round_node(element.absanchors['end'])

def get_node_direction(node1: schemdraw.util.Point, node2: schemdraw.util.Point) -> tuple[int, int]:
    delta = node2 - node1
    delta_x = +1 if delta.x >= 0 else -1
    delta_y = +1 if delta.y >= 0 else -1
    return delta_x, delta_y

@dataclass(frozen=True)
class SchemdrawNetwork:
    drawing: schemdraw.Drawing

    @property
    def elements(self) -> list[schemdraw.elements.Element]:
        return self.drawing.elements

    @property
    def two_term_elements(self) -> list[schemdraw.elements.Element2Term]:
        return [e for e in self.elements if isinstance(e, schemdraw.elements.Element2Term)]

    @property
    def line_elements(self) -> list[Line]:
        return [e for e in self.two_term_elements if type(e) is Line]
    
    @property
    def node_elements(self) -> list[Node]:
        return [e for e in self.elements if isinstance(e, Node)]

    @property
    def all_nodes(self) -> set[schemdraw.util.Point]:
        nodes = {round_node(e.absanchors['start']) for e in self.two_term_elements}
        nodes = nodes.union({round_node(e.absanchors['end']) for e in self.two_term_elements})
        return nodes

    @property
    def unique_nodes(self) -> set[schemdraw.util.Point]:
        nodes = self.all_nodes
        for node in self.all_nodes:
            if node in nodes:
                for n in self.get_equal_electrical_potential_nodes(node).intersection(nodes):
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
            identical_nodes = self.get_equal_electrical_potential_nodes(n)
            identical_nodes.remove(n)
            current_unique_node = self.unique_nodes.intersection(identical_nodes)
            if len(current_unique_node) > 0:
                node_mapping.update({n: current_unique_node.pop()})
            else:
                node_mapping.update({n: n})
        return node_mapping

    @property
    def ground(self) -> schemdraw.util.Point:
        ground_nodes = [n for n in self.node_elements if type(n) == Ground]
        if len(ground_nodes) > 1:
            raise MultipleGroundNodes
        if len(ground_nodes) == 0:
            return list(self.unique_nodes)[0]
        else:
            return get_nodes(ground_nodes[0])[0]

    @property
    def network(self) -> Network:
        translator = lambda e : element_translator[type(e)](e, self.get_node_index)[0]
        return Network(
            branches=[translator(e) for e in self.two_term_elements if type(e) is not Line],
            zero_node_label=self.get_node_index(self.ground)
            )

    def get_equal_electrical_potential_nodes(self, node: schemdraw.util.Point) -> set[schemdraw.util.Point]:
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

    def get_node_index(self, node: schemdraw.util.Point) -> str:
        return self.node_label_mapping[self.unique_node_mapping[node]]

    def get_element_from_name(self, name: str) -> schemdraw.elements.Element:
        elements = [e for e in self.two_term_elements if e.name == name]
        if len(elements) == 0:
            raise UnknownElement
        else:
            return elements[0]

    def get_branch_from_name(self, id: str) -> Branch:
        element = self.get_element_from_name(id)
        return element_translator[type(element)](element, self.get_node_index)[0]

class SchemdrawSolution:

    def __init__(self, schemdraw_network: SchemdrawNetwork, solver: NetworkSolver):
        self.schemdraw_network = schemdraw_network
        self.network_solution = solver(self.schemdraw_network.network)

    def draw_voltage(self, element_name: str, reverse: bool = False, precision = 3) -> schemdraw.Drawing:
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
        return schemdraw.elements.CurrentLabel(top=False, reverse=reverse, color=blue).at(element).label(f'{print_voltage(V_branch, precision=precision)}V')

    def draw_current(self, element_name: str, reverse: bool = False, start: bool = True, ofst: float = 0.8, precision=3) -> schemdraw.Drawing:
        element = self.schemdraw_network.get_element_from_name(element_name)
        branch = self.schemdraw_network.get_branch_from_name(element_name)
        I_branch = self.network_solution.get_current(branch)
        # adjust counting arrow system of voltage sources for display
        if type(element) is VoltageSource or type(element) is RealVoltageSource:
            start = False
        if start is False:
            reverse = not reverse
        return schemdraw.elements.CurrentLabelInline(reverse=reverse, start=start, color=red, ofst=ofst).at(element).label(f'{print_current(I_branch, precision=precision)}A')
