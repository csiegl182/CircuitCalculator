from . import Elements as elm
from ..Network.network import Branch
from ..Network import elements as network_elmements

from .SchemdrawTranslatorTypes import ElementTranslatorMap


def linear_current_source_translator(element: elm.RealCurrentSource, nodes: tuple[str, str]) -> Branch:
    return Branch(nodes[0], nodes[1], network_elmements.linear_current_source(I=element.I, Y=1/element.R, name=element.name))

def resistor_translator(element: elm.Resistor, nodes: tuple[str, str]) -> Branch:
    return Branch(nodes[0], nodes[1], network_elmements.resistor(R=element.R, name=element.name))

def impedance_translator(element: elm.Resistor, nodes: tuple[str, str]) -> Branch:
    return Branch(nodes[0], nodes[1], network_elmements.impedance(Z=element.Z, name=element.name))

def current_source_translator(element: elm.CurrentSource, nodes: tuple[str, str]) -> Branch:
    return Branch(nodes[0], nodes[1], network_elmements.current_source(I=element.I, name=element.name))

def linear_voltage_source_translator(element: elm.RealVoltageSource, nodes: tuple[str, str]) -> Branch:
    return Branch(nodes[0], nodes[1], network_elmements.linear_voltage_source(U=element.V, Z=element.R, name=element.name))

def voltage_source_translator(element: elm.VoltageSource, nodes: tuple[str, str]) -> Branch:
    return Branch(nodes[0], nodes[1], network_elmements.voltage_source(U=-element.V, name=element.name))

network_translator_map : ElementTranslatorMap = {
    elm.Resistor : resistor_translator,
    elm.Impedance : impedance_translator,
    elm.CurrentSource: current_source_translator,
    elm.VoltageSource: voltage_source_translator,
    elm.RealCurrentSource: linear_current_source_translator,
    elm.RealVoltageSource: linear_voltage_source_translator
}
