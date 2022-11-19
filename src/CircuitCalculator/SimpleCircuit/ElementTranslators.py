import schemdraw
from typing import Callable, Type, TypeVar 
from . import Elements as elm
from .. import Network as ntw

SchemdrawElement = TypeVar('SchemdrawElement', bound=schemdraw.elements.Element)
SchemdrawElementTranslator = Callable[[SchemdrawElement, Callable[[schemdraw.util.Point], str]], tuple[ntw.Branch, str]]

def round_node(node: schemdraw.util.Point) -> schemdraw.util.Point:
    def local_round(x):
        return round(x, ndigits=2)
    return schemdraw.util.Point((local_round(node.x), local_round(node.y)))

def get_nodes(element: schemdraw.elements.Element) -> tuple[schemdraw.util.Point, schemdraw.util.Point]:
    return round_node(element.absanchors['start']), round_node(element.absanchors['end'])

def real_current_source_translator(element: elm.RealCurrentSource, node_mapper: Callable[[schemdraw.util.Point], str]) -> tuple[ntw.Branch, str]:
    n1, n2 = get_nodes(element)
    return ntw.Branch(node_mapper(n1), node_mapper(n2), ntw.real_current_source(element.I, element.R)), element.name

def resistor_translator(element: elm.Resistor, node_mapper: Callable[[schemdraw.util.Point], str]) -> tuple[ntw.Branch, str]:
    n1, n2 = get_nodes(element)
    return ntw.Branch(node_mapper(n1), node_mapper(n2), ntw.resistor(element.R)), element.name

def current_source_translator(element: elm.CurrentSource, node_mapper: Callable[[schemdraw.util.Point], str]) -> tuple[ntw.Branch, str]:
    n1, n2 = get_nodes(element)
    return ntw.Branch(node_mapper(n1), node_mapper(n2), ntw.current_source(element.I)), element.name

def real_voltage_source_translator(element: elm.RealVoltageSource, node_mapper: Callable[[schemdraw.util.Point], str]) -> tuple[ntw.Branch, str]:
    n1, n2 = get_nodes(element)
    return ntw.Branch(node_mapper(n2), node_mapper(n1), ntw.real_voltage_source(element.V, element.R)), element.name

def voltage_source_translator(element: elm.VoltageSource, node_mapper: Callable[[schemdraw.util.Point], str]) -> tuple[ntw.Branch, str]:
    n1, n2 = get_nodes(element)
    return ntw.Branch(node_mapper(n2), node_mapper(n1), ntw.voltage_source(element.V)), element.name

element_translator : dict[Type[schemdraw.elements.Element], SchemdrawElementTranslator] = {
    elm.RealCurrentSource : real_current_source_translator,
    elm.Resistor : resistor_translator,
    elm.CurrentSource: current_source_translator,
    elm.RealVoltageSource : real_voltage_source_translator,
    elm.VoltageSource: voltage_source_translator,
}

def translator_available(element: schemdraw.elements.Element) -> bool:
    return type(element) in element_translator.keys()