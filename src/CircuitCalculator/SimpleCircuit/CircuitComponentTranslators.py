from . import Elements as elm
from ..Circuit.Components import components as cp
from .SchemdrawTranslatorTypes import ElementTranslatorMap
from math import pi, inf


def resistor_translator(element: elm.Resistor, nodes: tuple[str, ...]) -> cp.Component:
    return cp.resistor(id=element.name, nodes=(nodes[0], nodes[1]), R=element.R)

def impedance_translator(element: elm.Impedance, nodes: tuple[str, ...]) -> cp.Component:
    return cp.impedance(id=element.name, nodes=(nodes[0], nodes[1]), Z=element.Z)

def conductance_translator(element: elm.Conductance, nodes: tuple[str, ...]) -> cp.Component:
    return cp.conductance(nodes=(nodes[0], nodes[1]), id=element.name, G=element.G)

def capacitor_translator(element: elm.Capacitor, nodes: tuple[str, ...]) -> cp.Component:
    return cp.capacitor(nodes=(nodes[0], nodes[1]), id=element.name, C=element.C)

def inductance_translator(element: elm.Inductance, nodes: tuple[str, ...]) -> cp.Component:
    return cp.inductance(nodes=(nodes[0], nodes[1]), id=element.name, L=element.L)

def lamp_translator(element: elm.Lamp, nodes: tuple[str, ...]) -> cp.Component:
    return cp.lamp(nodes=(nodes[0], nodes[1]), id=element.name, P=element.P_ref, V_ref=element.V_ref)

def dc_voltage_source_translator(element: elm.VoltageSource, nodes: tuple[str, ...]) -> cp.Component:
    return cp.dc_voltage_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        V=element.V.real if not element.is_reverse else -element.V.real
    )

def complex_voltage_source_translator(element: elm.ComplexVoltageSource, nodes: tuple[str, ...]) -> cp.Component:
    return cp.complex_voltage_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        V=element.V if not element.is_reverse else -element.V
    )

def dc_current_source_translator(element: elm.CurrentSource, nodes: tuple[str, ...]) -> cp.Component:
    return cp.dc_current_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        I=element.I.real if not element.is_reverse else -element.I.real
    )

def complex_current_source_translator(element: elm.ComplexCurrentSource, nodes: tuple[str, ...]) -> cp.Component:
    return cp.complex_current_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        I=element.I if not element.is_reverse else -element.I
    )

def ac_voltage_source_translator(element: elm.ACVoltageSource, nodes: tuple[str, ...]) -> cp.Component:
    return cp.ac_voltage_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        V=element.V if not element.is_reverse else -element.V,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def ac_current_source_translator(element: elm.ACCurrentSource, nodes: tuple[str, ...]) -> cp.Component:
    return cp.ac_current_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        I=element.I if not element.is_reverse else -element.I,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def rect_voltage_source_translator(element: elm.RectVoltageSource, nodes: tuple[str, ...]) -> cp.Component:
    from ..SignalProcessing.periodic_functions import RectFunction
    return cp.periodic_voltage_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        wavetype=RectFunction.wavetype,
        V=element.V if not element.is_reverse else -element.V,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def rect_current_source_translator(element: elm.RectCurrentSource, nodes: tuple[str, ...]) -> cp.Component:
    from ..SignalProcessing.periodic_functions import RectFunction
    return cp.periodic_current_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        wavetype=RectFunction.wavetype,
        I=element.I if not element.is_reverse else -element.I,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def tri_voltage_source_translator(element: elm.TriangleVoltageSource, nodes: tuple[str, ...]) -> cp.Component:
    from ..SignalProcessing.periodic_functions import TriFunction
    return cp.periodic_voltage_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        wavetype=TriFunction.wavetype,
        V=element.V if not element.is_reverse else -element.V,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def tri_current_source_translator(element: elm.TriangleCurrentSource, nodes: tuple[str, ...]) -> cp.Component:
    from ..SignalProcessing.periodic_functions import TriFunction
    return cp.periodic_current_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        wavetype=TriFunction.wavetype,
        I=element.I if not element.is_reverse else -element.I,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def saw_voltage_source_translator(element: elm.SawtoothVoltageSource, nodes: tuple[str, ...]) -> cp.Component:
    from ..SignalProcessing.periodic_functions import SawFunction
    return cp.periodic_voltage_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        wavetype=SawFunction.wavetype,
        V=element.V if not element.is_reverse else -element.V,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def saw_current_source_translator(element: elm.SawtoothCurrentSource, nodes: tuple[str, ...]) -> cp.Component:
    from ..SignalProcessing.periodic_functions import SawFunction
    return cp.periodic_current_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        wavetype=SawFunction.wavetype,
        I=element.I if not element.is_reverse else -element.I,
        w=element.w,
        phi=element.phi*pi/180 if element.deg else element.phi
    )

def linear_current_source_translator(element: elm.RealCurrentSource, nodes: tuple[str, ...]) -> cp.Component:
    return cp.dc_current_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        I=element.I.real if not element.is_reverse else -element.I.real,
        G=element.G
    )

def linear_voltage_source_translator(element: elm.RealVoltageSource, nodes: tuple[str, ...]) -> cp.Component:
    return cp.dc_voltage_source(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
        V=element.V.real if not element.is_reverse else -element.V.real,
        R=element.R
    )

def short_circuit_translator(element: elm.LabeledLine, nodes: tuple[str, ...]) -> cp.Component:
    return cp.short_circuit(
        nodes=(nodes[0], nodes[1]) if not element.is_reverse else (nodes[1], nodes[0]),
        id=element.name,
    )

def switch_translator(element: elm.Switch, nodes: tuple[str, ...]) -> cp.Component | None:
    if element.state == element.state.OPEN:
        return cp.resistor(nodes=(nodes[0], nodes[1]), id=element.name, R=inf)
    return cp.resistor(nodes=(nodes[0], nodes[1]), id=element.name, R=1e-12)

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
    elm.TriangleVoltageSource : tri_voltage_source_translator,
    elm.TriangleCurrentSource : tri_current_source_translator,
    elm.SawtoothVoltageSource : saw_voltage_source_translator,
    elm.SawtoothCurrentSource : saw_current_source_translator,
    elm.Capacitor : capacitor_translator,
    elm.Inductance : inductance_translator,
    elm.Lamp : lamp_translator,
    elm.Ground : none_translator,
    elm.Line: none_translator,
    elm.LabeledLine: short_circuit_translator,
    elm.Node: none_translator,
    elm.LabelNode: none_translator,
    elm.RealCurrentSource: linear_current_source_translator,
    elm.RealVoltageSource: linear_voltage_source_translator,
    elm.Switch: switch_translator,
    elm.VoltageLabel: none_translator,
    elm.CurrentLabel: none_translator,
    elm.PowerLabel: none_translator,
    elm.Element: none_translator,
}
