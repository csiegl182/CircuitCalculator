from . import Elements as elm
from ..Circuit import components
from .SchemdrawTranslatorTypes import ElementTranslatorMap
import numpy as np


def resistor_translator(element: elm.Resistor, nodes: tuple[str, str]) -> components.Resistor:
    return components.Resistor(nodes=nodes, id=element.name, R=element.R)

def current_source_translator(element: elm.CurrentSource, nodes: tuple[str, str]) -> components.CurrentSource:
    return components.CurrentSource(nodes=nodes, id=element.name, I=element.I)

def voltage_source_translator(element: elm.VoltageSource, nodes: tuple[str, str]) -> components.VoltageSource:
    return components.VoltageSource(nodes=nodes, id=element.name, V=element.V)

def capacitor_translator(element: elm.Capacitor, nodes: tuple[str, str]) -> components.Capacitor:
    return components.Capacitor(nodes=nodes, id=element.name, C=element.C)

def inductance_translator(element: elm.Inductance, nodes: tuple[str, str]) -> components.Inductance:
    return components.Inductance(nodes=nodes, id=element.name, L=element.L)

def ground_translator(element: elm.Ground, nodes: tuple[str]) -> components.Ground:
    return components.Ground(nodes=nodes, id=element.name)

def ac_voltage_source_translator(element: elm.ACVoltageSource, nodes: tuple[str, str]) -> components.VoltageSource:
    return components.VoltageSource(
        nodes=nodes,
        id=element.name,
        V=element.V,
        w=element.w,
        phi=element.phi*np.pi/180 if element.deg else element.phi
    )

circuit_translator_map : ElementTranslatorMap = {
    elm.Resistor : resistor_translator,
    elm.CurrentSource : current_source_translator,
    elm.VoltageSource : voltage_source_translator,
    elm.Capacitor : capacitor_translator,
    elm.Inductance : inductance_translator,
    elm.Ground : ground_translator,
    elm.ACVoltageSource : ac_voltage_source_translator,
}
