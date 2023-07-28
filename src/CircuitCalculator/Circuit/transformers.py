import numpy as np
from ..Network import elements as elm
from ..Network import network as ntw
from typing import Callable, Type, TypeVar
from . import components as cmp

CircuitComponent = TypeVar("CircuitComponent", bound=cmp.Component)
CircuitComponentTranslator = Callable[[CircuitComponent, float, float], ntw.Branch]

def resistor(resistor: cmp.Resistor, *_) -> ntw.Branch:
    return ntw.Branch(resistor.nodes[0], resistor.nodes[1], elm.resistor(resistor.id, resistor.R))

def capacitor(capacitor: cmp.Capacitor, w: float = 0, *_) -> ntw.Branch:
    return ntw.Branch(
        capacitor.nodes[0],
        capacitor.nodes[1],
        elm.admittance(capacitor.id, elm.admittance_value(B=w*capacitor.C)))

def inductance(inductance: cmp.Inductance, w: float = 0, *_) -> ntw.Branch:
    return ntw.Branch(
        inductance.nodes[0],
        inductance.nodes[1],
        elm.impedance(inductance.id, elm.impedance_value(X=w*inductance.L))
    )

def current_source(current_source: cmp.CurrentSource, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    element = elm.current_source(current_source.id, elm.complex_value(current_source.I, 0))
    if np.abs(w-current_source.w) > w_resolution:
        element = elm.open_circuit(current_source.id)
    return ntw.Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element
    )

def voltage_source(voltage_source: cmp.VoltageSource, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    element = elm.voltage_source(voltage_source.id, elm.complex_value(voltage_source.V, voltage_source.phi))
    if np.abs(w-voltage_source.w) > w_resolution:
        element = elm.short_cicruit(voltage_source.id)
    return ntw.Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element)

def periodic_voltage_source(source: cmp.PeriodicVoltageSource, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    n = np.round(w/source.w)
    delta_n = np.abs(w/source.w - n)
    if delta_n > w_resolution/source.w:
        return ntw.Branch(
            source.nodes[0],
            source.nodes[1],
            elm.short_cicruit(source.id))
    single_frequency_source = cmp.VoltageSource(
        nodes=source.nodes,
        id=source.id,
        w=w,
        phi=source.frequency_properties.phase(n),
        V=source.frequency_properties.amplitude(n)
    )
    return voltage_source(single_frequency_source, w, w_resolution)

def periodic_current_source(source: cmp.PeriodicCurrentSource, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    n = np.round(w/source.w)
    delta_n = np.abs(w/source.w - n)
    if delta_n > w_resolution/source.w:
        return ntw.Branch(
            source.nodes[0],
            source.nodes[1],
            elm.open_circuit(source.id))
    single_frequency_source = cmp.CurrentSource(
        nodes=source.nodes,
        id=source.id,
        w=w,
        phi=source.frequency_properties.phase(n),
        I=source.frequency_properties.amplitude(n)
    )
    return current_source(single_frequency_source, w, w_resolution)

def linear_current_source(current_source: cmp.LinearCurrentSource, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    element = elm.linear_current_source(current_source.id, elm.complex_value(current_source.I, 0), elm.complex_value(current_source.G, 0))
    if np.abs(w-current_source.w) > w_resolution:
        element = elm.open_circuit(current_source.id)
    return ntw.Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element)

def linear_voltage_source(voltage_source: cmp.LinearVoltageSource, w: float = 0, w_resolution: float = 1e-3) -> ntw.Branch:
    element = elm.linear_voltage_source(voltage_source.id, elm.complex_value(voltage_source.V, 0), elm.complex_value(voltage_source.R, 0))
    if np.abs(w-voltage_source.w) > w_resolution:
        element = elm.short_cicruit(voltage_source.id)
    return ntw.Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element
    )

transformers : dict[Type[cmp.Component], CircuitComponentTranslator] = {
    cmp.Resistor : resistor,
    cmp.Capacitor : capacitor,
    cmp.Inductance : inductance,
    cmp.CurrentSource : current_source,
    cmp.VoltageSource : voltage_source,
    cmp.LinearCurrentSource : linear_current_source,
    cmp.LinearVoltageSource : linear_voltage_source,
    cmp.PeriodicVoltageSource : periodic_voltage_source,
    cmp.PeriodicCurrentSource : periodic_current_source,
}