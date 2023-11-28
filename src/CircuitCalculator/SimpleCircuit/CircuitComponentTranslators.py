from . import Elements as elm
from ..Circuit import components as ccp
from ..SignalProcessing import periodic_functions
from .SchemdrawTranslatorTypes import ElementTranslatorMap
from math import pi, inf


def resistor_translator(element: elm.Resistor, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.resistor(id=element.name, nodes=nodes, R=element.R)

def impedance_translator(element: elm.Impedance, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.impedance(id=element.name, nodes=nodes, Z=element.Z)

def conductance_translator(element: elm.Conductance, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.conductance(nodes=nodes, id=element.name, G=element.G)

def capacitor_translator(element: elm.Capacitor, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.capacitor(nodes=nodes, id=element.name, C=element.C)

def inductance_translator(element: elm.Inductance, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.inductance(nodes=nodes, id=element.name, L=element.L)

def ground_translator(element: elm.Ground, nodes: tuple[str]) -> ccp.Component:
    return ccp.ground(nodes=nodes, id=element.name)

def dc_voltage_source_translator(element: elm.VoltageSource, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.dc_voltage_source(
        nodes=nodes if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        V=element.V.real if not element.is_reverse else -element.V.real
    )

def complex_voltage_source_translator(element: elm.ComplexVoltageSource, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.complex_voltage_source(
        nodes=nodes if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        V=element.V if not element.is_reverse else -element.V
    )

def dc_current_source_translator(element: elm.CurrentSource, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.dc_current_source(
        nodes=nodes if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        I=element.I.real if not element.is_reverse else -element.I.real
    )

def complex_current_source_translator(element: elm.ComplexCurrentSource, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.dc_current_source(
        nodes=nodes if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        I=element.I if not element.is_reverse else -element.I
    )

def ac_voltage_source_translator(element: elm.ACVoltageSource, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.ac_voltage_source(
        nodes=nodes if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        V=element.V if not element.is_reverse else -element.V,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def ac_current_source_translator(element: elm.ACCurrentSource, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.ac_current_source(
        nodes=nodes if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        I=element.I if not element.is_reverse else -element.I,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def rect_voltage_source_translator(element: elm.RectVoltageSource, nodes: tuple[str, str]) -> ccp.Component:
    from ..SignalProcessing.periodic_functions import RectFunction
    return ccp.periodic_voltage_source(
        nodes=(nodes[1], nodes[0]) if not element.is_reverse else nodes,
        id=element.name,
        wavetype=RectFunction.wavetype,
        V=element.V if not element.is_reverse else -element.V,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def rect_current_source_translator(element: elm.RectVoltageSource, nodes: tuple[str, str]) -> ccp.Component:
    from ..SignalProcessing.periodic_functions import RectFunction
    return ccp.periodic_current_source(
        nodes=(nodes[1], nodes[0]) if not element.is_reverse else nodes,
        id=element.name,
        wavetype=RectFunction.wavetype,
        I=element.I if not element.is_reverse else -element.I,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def linear_current_source_translator(element: elm.RealCurrentSource, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.dc_current_source(
        nodes=nodes if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        I=element.I.real if not element.is_reverse else -element.I.real,
        G=element.G
    )

def linear_voltage_source_translator(element: elm.RealVoltageSource, nodes: tuple[str, str]) -> ccp.Component:
    return ccp.dc_voltage_source(
        nodes=nodes if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        V=element.V.real if not element.is_reverse else -element.V.real,
        R=element.R
    )

def switch_translator(element: elm.Switch, nodes: tuple[str, str]) -> ccp.Component | None:
    if element.state == element.state.OPEN:
        return ccp.resistor(nodes=nodes, id=element.name, R=inf)
    return ccp.resistor(nodes=nodes, id=element.name, R=1e-12)

def none_translator(*_) -> None:
    return None

circuit_translator_map : ElementTranslatorMap = {
    elm.Resistor : resistor_translator,
    elm.Impedance : impedance_translator,
    elm.Conductance : conductance_translator,
    elm.VoltageSource : dc_voltage_source_translator,
    elm.ComplexVoltageSource : complex_voltage_source_translator,
    elm.CurrentSource : dc_current_source_translator,
    elm.ComplexCurrentSource : complex_current_source_translator,
    elm.ACVoltageSource : ac_voltage_source_translator,
    elm.ACCurrentSource : ac_current_source_translator,
    elm.RectVoltageSource : rect_voltage_source_translator,
    elm.RectCurrentSource : rect_current_source_translator,
    elm.Capacitor : capacitor_translator,
    elm.Inductance : inductance_translator,
    elm.Ground : ground_translator,
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
