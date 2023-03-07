from schemdraw import elements, util
from typing import Callable, Type, TypeVar 
from . import Elements as elm
from ..Network.network import Branch
from ..Network import elements as network_elmements

SchemdrawElement = TypeVar('SchemdrawElement', bound=elements.Element)
SchemdrawElementTranslator = Callable[[SchemdrawElement, Callable[[util.Point], str]], Branch]

def round_node(node: util.Point) -> util.Point:
    def local_round(x):
        return round(x, ndigits=2)
    return util.Point((local_round(node.x), local_round(node.y)))

def get_nodes(element: elements.Element, n1_label='start', n2_label='end') -> tuple[util.Point, util.Point]:
    return round_node(element.absanchors[n1_label]), round_node(element.absanchors[n2_label])

def linear_current_source_translator(element: elm.RealCurrentSource, node_mapper: Callable[[util.Point], str]) -> Branch:
    n1, n2 = get_nodes(element)
    return Branch(node_mapper(n1), node_mapper(n2), network_elmements.linear_current_source(I=element.I, Y=1/element.R, name=element.name))

def resistor_translator(element: elm.Resistor, node_mapper: Callable[[util.Point], str]) -> Branch:
    n1, n2 = get_nodes(element)
    return Branch(node_mapper(n1), node_mapper(n2), network_elmements.resistor(R=element.R, name=element.name))

def current_source_translator(element: elm.CurrentSource, node_mapper: Callable[[util.Point], str]) -> Branch:
    n1, n2 = get_nodes(element)
    return Branch(node_mapper(n1), node_mapper(n2), network_elmements.current_source(I=element.I, name=element.name))

def linear_voltage_source_translator(element: elm.RealVoltageSource, node_mapper: Callable[[util.Point], str]) -> Branch:
    n1, n2 = get_nodes(element)
    return Branch(node_mapper(n1), node_mapper(n2), network_elmements.linear_voltage_source(U=element.V, Z=element.R, name=element.name))

def voltage_source_translator(element: elm.VoltageSource, node_mapper: Callable[[util.Point], str]) -> Branch:
    n1, n2 = get_nodes(element)
    return Branch(node_mapper(n2), node_mapper(n1), network_elmements.voltage_source(U=element.V, name=element.name))

element_translator : dict[Type[elements.Element], SchemdrawElementTranslator] = {
    elm.Resistor : resistor_translator,
    elm.CurrentSource: current_source_translator,
    elm.VoltageSource: voltage_source_translator,
    elm.RealCurrentSource: linear_current_source_translator,
    elm.RealVoltageSource: linear_voltage_source_translator
}

def translator_available(element: elements.Element) -> bool:
    return type(element) in element_translator.keys()