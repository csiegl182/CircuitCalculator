from . import Elements as elm
from ..Circuit import components as cct_cmp
from .SchemdrawTranslatorTypes import ElementTranslatorMap
from math import pi, inf


def resistor_translator(element: elm.Resistor, nodes: tuple[str, str]) -> cct_cmp.Resistor:
    return cct_cmp.Resistor(nodes=nodes, id=element.name, R=element.R)

def capacitor_translator(element: elm.Capacitor, nodes: tuple[str, str]) -> cct_cmp.Capacitor:
    return cct_cmp.Capacitor(nodes=nodes, id=element.name, C=element.C)

def inductance_translator(element: elm.Inductance, nodes: tuple[str, str]) -> cct_cmp.Inductance:
    return cct_cmp.Inductance(nodes=nodes, id=element.name, L=element.L)

def ground_translator(element: elm.Ground, nodes: tuple[str]) -> cct_cmp.Ground:
    return cct_cmp.Ground(nodes=nodes, id=element.name)

def dc_voltage_source_translator(element: elm.VoltageSource, nodes: tuple[str, str]) -> cct_cmp.VoltageSource:
    return cct_cmp.VoltageSource(
        nodes=nodes[::-1],
        id=element.name,
        V=element.V.real,
        w=0,
        phi=0
    )

def dc_current_source_translator(element: elm.CurrentSource, nodes: tuple[str, str]) -> cct_cmp.CurrentSource:
    return cct_cmp.CurrentSource(
        nodes=nodes[::-1],
        id=element.name,
        I=-element.I.real,
        w=0,
        phi=0
    )

def ac_voltage_source_translator(element: elm.ACVoltageSource, nodes: tuple[str, str]) -> cct_cmp.VoltageSource:
    return cct_cmp.VoltageSource(
        nodes=nodes[::-1],
        id=element.name,
        V=element.V,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def ac_current_source_translator(element: elm.ACCurrentSource, nodes: tuple[str, str]) -> cct_cmp.CurrentSource:
    return cct_cmp.CurrentSource(
        nodes=nodes,
        id=element.name,
        I=element.I,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def linear_current_source_translator(element: elm.RealCurrentSource, nodes: tuple[str, str]) -> cct_cmp.LinearCurrentSource:
    return cct_cmp.LinearCurrentSource(nodes=nodes, id=element.name, I=element.I.real, G=element.G)

def linear_voltage_source_translator(element: elm.RealVoltageSource, nodes: tuple[str, str]) -> cct_cmp.LinearVoltageSource:
    return cct_cmp.LinearVoltageSource(nodes=nodes, id=element.name, V=element.V.real, R=element.R)

def switch_translator(element: elm.Switch, nodes: tuple[str, str]) -> cct_cmp.Resistor | None:
    if element.state == element.state.OPEN:
        return cct_cmp.Resistor(nodes=nodes, id=element.name, R=inf)
    return cct_cmp.Resistor(nodes=nodes, id=element.name, R=1e-12)

def none_translator(*_) -> None:
    return None

circuit_translator_map : ElementTranslatorMap = {
    elm.Resistor : resistor_translator,
    elm.VoltageSource : dc_voltage_source_translator,
    elm.CurrentSource : dc_current_source_translator,
    elm.ACVoltageSource : ac_voltage_source_translator,
    elm.ACCurrentSource : ac_current_source_translator,
    elm.Capacitor : capacitor_translator,
    elm.Inductance : inductance_translator,
    elm.Ground : ground_translator,
    elm.ACVoltageSource : ac_voltage_source_translator,
    elm.Line: none_translator,
    elm.Node: none_translator,
    elm.LabelNode: none_translator,
    elm.RealCurrentSource: linear_current_source_translator,
    elm.RealVoltageSource: linear_voltage_source_translator,
    elm.Switch: switch_translator,
    elm.VoltageLabel: none_translator,
    elm.CurrentLabel: none_translator,
    elm.PowerLabel: none_translator,
}
