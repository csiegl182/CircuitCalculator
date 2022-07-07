from NodalAnalysis import *
from Network import load_network, load_network_from_json
from typing import Set, List, Tuple, Dict, Any
import json
import schemdraw
import schemdraw.elements as elm

class RealCurrentSource(elm.sources.SourceI):
    def __init__(self, I: float, R: float, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current = I
        self._resistance = R
        self._name = name
        self.label(self._name)

    @property
    def name(self) -> str:
        return self._name

    @property
    def current(self) -> float:
        return self._current

    @property
    def resistance(self) -> float:
        return self._resistance

    @property
    def inductance(self) -> float:
        return 1/self._resistance

    def values(self) -> Dict[str, float]:
        return {'I' : self.current, 'R' : self.resistance}

class Resistor(elm.twoterm.ResistorIEC):
    def __init__(self, R: float, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._resistance = R
        self._name = name
        self.label(self._name)

    @property
    def name(self) -> str:
        return self._name

    @property
    def resistance(self) -> float:
        return self._resistance

    @property
    def inductance(self) -> float:
        return 1/self._resistance

    def values(self) -> Dict[str, float]:
        return {'R' : self.resistance}

class Inductor(elm.twoterm.ResistorIEC):
    def __init__(self, G: float, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._inductance = G
        self._name = name
        self.label(self._name)

    @property
    def name(self) -> str:
        return self._name

    @property
    def resistance(self) -> float:
        return 1/self._inductance

    @property
    def inductance(self) -> float:
        return self._resistance

    def values(self) -> Dict[str, float]:
        return {'R' : self.resistance}

class Line(elm.lines.Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Ground(elm.Ground):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
def round_node(node: schemdraw.util.Point) -> schemdraw.util.Point:
    def local_round(x):
        return round(x, ndigits=2)
    return schemdraw.util.Point((local_round(node.x), local_round(node.y)))

def get_nodes(element: schemdraw.elements.Element2Term) -> Tuple[schemdraw.util.Point, schemdraw.util.Point]:
    return round_node(element.absanchors['start']), round_node(element.absanchors['end'])

def get_all_nodes(elements: List[schemdraw.elements.Element2Term]) -> Set[schemdraw.util.Point]:
    nodes = {round_node(e.absanchors['start']) for e in elements}
    nodes = nodes.union({round_node(e.absanchors['end']) for e in elements})
    return nodes

element_type = {
    RealCurrentSource : "real_current_source",
    Resistor : "resistor",
    Line : "line"
}

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

def get_unique_nodes(elements: List[schemdraw.elements.Element2Term]) -> Set[schemdraw.util.Point]:
    unique_nodes = get_all_nodes(elements)
    for node in get_all_nodes(elements):
        if node in unique_nodes:
            for n in get_identical_nodes(node, elements):
                unique_nodes.remove(n)
    return unique_nodes

def get_unique_node_mapping(elements: List[schemdraw.elements.Element2Term]) -> Dict[schemdraw.util.Point, schemdraw.util.Point]:
    unique_nodes = get_unique_nodes(elements)
    node_mapping = {}
    for n in get_all_nodes(elements):
        identical_nodes = get_identical_nodes(n, elements)
        current_unique_node = unique_nodes.intersection(identical_nodes)
        if len(current_unique_node) > 0:
            node_mapping.update({n: current_unique_node.pop()})
        else:
            node_mapping.update({n: n})
    return node_mapping

def get_two_term_elements(drawing: schemdraw.Drawing) -> List[schemdraw.elements.Element2Term]:
    return [e for e in drawing.elements if isinstance(e, schemdraw.elements.Element2Term)]

def parse_drawing(drawing: schemdraw.Drawing) -> List[Dict[str, Any]]:
    el = []
    unique_node_mapping = get_unique_node_mapping(get_two_term_elements(drawing))
    unique_nodes = list(get_unique_nodes(get_two_term_elements(drawing)))
    elements = [e for e in get_two_term_elements(drawing) if element_type[type(e)] != "line"]
    for e in elements:
        n1, n2 = get_nodes(e)
        d = {
            "type": element_type[type(e)],
            "id" : e.name,
            "N1" : unique_nodes.index(unique_node_mapping[n1]),
            "N2" : unique_nodes.index(unique_node_mapping[n2])
        }
        d.update(e.values())
        el.append(d)
    return el