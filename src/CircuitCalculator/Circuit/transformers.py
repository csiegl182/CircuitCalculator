import numpy as np
from ..Network import elements
from ..Network.network import Branch
from typing import Callable, Type, TypeVar
from . import components as cmp

CircuitComponent = TypeVar("CircuitComponent", bound=cmp.Component)
CircuitComponentTranslator = Callable[[CircuitComponent, float, float], Branch]

def resistor(resistor: cmp.Resistor, *_) -> Branch:
    return Branch(resistor.nodes[0], resistor.nodes[1], elements.resistor(resistor.id, resistor.R))

def capacitor(capacitor: cmp.Capacitor, w: float = 0, *_) -> Branch:
    return Branch(
        capacitor.nodes[0],
        capacitor.nodes[1],
        elements.admittance(capacitor.id, elements.admittance_value(B=w*capacitor.C)))

def inductance(inductance: cmp.Inductance, w: float = 0, *_) -> Branch:
    return Branch(
        inductance.nodes[0],
        inductance.nodes[1],
        elements.impedance(inductance.id, elements.impedance_value(X=w*inductance.L))
    )

def current_source(current_source: cmp.CurrentSource, w: float = 0, w_resolution: float = 1e-3) -> Branch:
    element = elements.current_source(current_source.id, elements.complex_value(current_source.I, 0))
    if np.abs(w-current_source.w) > w_resolution:
        element = elements.open_circuit(current_source.id)
    return Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element
    )

def voltage_source(voltage_source: cmp.VoltageSource, w: float = 0, w_resolution: float = 1e-3) -> Branch:
    element = elements.voltage_source(voltage_source.id, elements.complex_value(voltage_source.V, 0))
    if np.abs(w-voltage_source.w) > w_resolution:
        element = elements.short_cicruit(voltage_source.id)
    return Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element
    )

transformers : dict[Type[cmp.Component], CircuitComponentTranslator] = {
    cmp.Resistor : resistor,
    cmp.Capacitor : capacitor,
    cmp.Inductance : inductance,
    cmp.CurrentSource : current_source,
    cmp.VoltageSource : voltage_source
}