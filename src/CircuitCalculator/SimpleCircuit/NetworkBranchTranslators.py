from ..Network import network as ntw
from ..Network import elements as ntw_elm

from . import Elements as elm
from .SchemdrawTranslatorTypes import ElementTranslatorMap


def linear_current_source_translator(element: elm.RealCurrentSource, nodes: tuple[str, str]) -> ntw.Branch:
    return ntw.Branch(nodes[0], nodes[1], ntw_elm.linear_current_source(I=element.I, Y=1/element.R, name=element.name))

def resistor_translator(element: elm.Resistor, nodes: tuple[str, str]) -> ntw.Branch:
    return ntw.Branch(nodes[0], nodes[1], ntw_elm.resistor(R=element.R, name=element.name))

def impedance_translator(element: elm.Resistor, nodes: tuple[str, str]) -> ntw.Branch:
    return ntw.Branch(nodes[0], nodes[1], ntw_elm.impedance(Z=element.Z, name=element.name))

def current_source_translator(element: elm.CurrentSource, nodes: tuple[str, str]) -> ntw.Branch:
    return ntw.Branch(nodes[0], nodes[1], ntw_elm.current_source(I=element.I, name=element.name))

def linear_voltage_source_translator(element: elm.RealVoltageSource, nodes: tuple[str, str]) -> ntw.Branch:
    return ntw.Branch(nodes[0], nodes[1], ntw_elm.linear_voltage_source(V=-element.V, Z=element.R, name=element.name))

def voltage_source_translator(element: elm.VoltageSource, nodes: tuple[str, str]) -> ntw.Branch:
    return ntw.Branch(nodes[0], nodes[1], ntw_elm.voltage_source(V=-element.V, name=element.name))

def none_translator(*_) -> None:
    return None

network_translator_map : ElementTranslatorMap = {
    elm.Resistor : resistor_translator,
    elm.Impedance : impedance_translator,
    elm.CurrentSource: current_source_translator,
    elm.VoltageSource: voltage_source_translator,
    elm.RealCurrentSource: linear_current_source_translator,
    elm.RealVoltageSource: linear_voltage_source_translator,
    elm.Line: none_translator,
    elm.Node: none_translator,
    elm.LabelNode: none_translator,
    elm.Ground: none_translator,
}
