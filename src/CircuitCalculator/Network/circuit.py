import numpy as np
from dataclasses import dataclass, field
from . import elements
from .network import Branch, Network
from typing import Callable, Type, TypeVar
from abc import ABC
    
@dataclass(frozen=True)
class Component(ABC):
    nodes : tuple[str]
    type : str
    id : str

@dataclass(frozen=True)
class TwoPoleComponent(Component):
    nodes : tuple[str, str]

@dataclass(frozen=True)
class Resistor(TwoPoleComponent):
    R : float
    type : str = field(default='resistor', init=False)

@dataclass(frozen=True)
class Capacitor(TwoPoleComponent):
    C : float
    type : str = field(default='capacitor', init=False)

@dataclass(frozen=True)
class Inductance(TwoPoleComponent):
    L : float
    type : str = field(default='inductance', init=False)

@dataclass(frozen=True)
class Source(TwoPoleComponent):
    w : float = field(default=0.0)
    phi : float = field(default=0.0)

@dataclass(frozen=True)
class CurrentSource(Source):
    I : float = field(default=0.0)
    type : str = field(default='current_source', init=False)

@dataclass(frozen=True)
class VoltageSource(Source):
    V : float = field(default=0.0)
    type : str = field(default='voltage_source', init=False)

@dataclass(frozen=True)
class Ground(Component):
    id : str = field(default='gnd')
    type : str = field(default='ground', init=False)
    nodes : tuple[str]

def transform_resistor(resistor: Resistor, *_) -> Branch:
    return Branch(resistor.nodes[0], resistor.nodes[1], elements.resistor(resistor.id, resistor.R))

def transform_capacitor(capacitor: Capacitor, w: float = 0, *_) -> Branch:
    return Branch(
        capacitor.nodes[0],
        capacitor.nodes[1],
        elements.admittance(capacitor.id, elements.admittance_value(B=w*capacitor.C)))

def transform_inductance(inductance: Inductance, w: float = 0, *_) -> Branch:
    return Branch(
        inductance.nodes[0],
        inductance.nodes[1],
        elements.impedance(inductance.id, elements.impedance_value(X=w*inductance.L))
    )

def transform_current_source(current_source: CurrentSource, w: float = 0, w_resolution: float = 1e-3) -> Branch:
    element = elements.current_source(current_source.id, elements.complex_value(current_source.I, 0))
    if np.abs(w-current_source.w) > w_resolution:
        element = elements.open_circuit(current_source.id)
    return Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element
    )

def transform_voltage_source(voltage_source: VoltageSource, w: float = 0, w_resolution: float = 1e-3) -> Branch:
    element = elements.voltage_source(voltage_source.id, elements.complex_value(voltage_source.V, 0))
    if np.abs(w-voltage_source.w) > w_resolution:
        element = elements.short_cicruit(voltage_source.id)
    return Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element
    )

CircuitComponent = TypeVar("CircuitComponent", bound=Component)
CircuitComponentTranslator = Callable[[CircuitComponent, float, float], Branch]

transformers : dict[Type[Component], CircuitComponentTranslator] = {
    Resistor : transform_resistor,
    Capacitor : transform_capacitor,
    Inductance : transform_inductance,
    CurrentSource : transform_current_source,
    VoltageSource : transform_voltage_source
}

Circuit = list[Component]

def transform(circuit: Circuit, w: float = 0, w_resolution: float = 1e-3) -> Network:
    ground_nodes = [component for component in circuit if component.type == 'ground']
    return Network(
        [transformers[type(component)](component, w, w_resolution) for component in circuit if type(component) in transformers.keys()],
        zero_node_label=ground_nodes[0].nodes[0]
    )