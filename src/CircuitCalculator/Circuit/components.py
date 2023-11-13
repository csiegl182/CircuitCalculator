import numpy as np
import numpy.typing as npt
from dataclasses import dataclass, field
from abc import ABC
from ..SignalProcessing.periodic_functions import PeriodicFunction, HarmonicCoefficients, fourier_series, CosFunction, ConstantFunction
from typing import Type, Any

@dataclass(frozen=True)
class Component:
    type : str
    nodes : tuple[str, ...] = field(default=('0',))
    id : str = field(default='0')
    value: dict[str, float | str] = field(default_factory=dict)
    is_active: bool = field(default=False, init=False)
    w: float= field(default=0, init=False)

def resistor(id: str, nodes: tuple[str, str], R: float) -> Component:
    return Component(
        type='resistor',
        id=id,
        value={'R': R},
        nodes=nodes
        )

def conductance(id: str, nodes: tuple[str, str], G: float) -> Component:
    return Component(
        type='conductance',
        id=id,
        value={'G': G},
        nodes=nodes
        )

def capacitor(id: str, nodes: tuple[str, str], C: float) -> Component:
    return Component(
        type='capacitor',
        id=id,
        value={'C': C},
        nodes=nodes
    )

def inductance(id: str, nodes: tuple[str, str], L: float) -> Component:
    return Component(
        type='inductance',
        id=id,
        value={'L': L},
        nodes=nodes
    )

def impedance(id: str, nodes: tuple[str, str], Z: complex) -> Component:
    return Component(
        type='impedance',
        id=id,
        value={'R': Z.real, 'X': Z.imag},
        nodes=nodes
        )

def admittance(id: str, nodes: tuple[str, str], Y: complex) -> Component:
    return Component(
        type='admittance',
        id=id,
        value={'G': Y.real, 'B': Y.imag},
        nodes=nodes
        )

def dc_voltage_source(id: str, nodes: tuple[str, str], V: float, R: float = 0) -> Component:
    return Component(
        type='dc_voltage_source',
        id=id,
        value={'V': V, 'R': R, 'w': 0, 'phi': 0},
        nodes=nodes
        )

def ac_voltage_source(id: str, nodes: tuple[str, str], V: float, R: float = 0, w: float = 0, phi: float = 0) -> Component:
    return Component(
        type='ac_voltage_source',
        id=id,
        value={'V': V, 'R': R, 'w': w, 'phi': phi},
        nodes=nodes
        )

def complex_voltage_source(id: str, nodes: tuple[str, str], V: complex, Z: complex = 0) -> Component:
    return Component(
        type='complex_voltage_source',
        id=id,
        value={'V_real': V.real, 'V_imag': V.imag, 'R': Z.real, 'X': Z.imag},
        nodes=nodes
        )

# TODO: weird definition
def periodic_voltage_source(id: str, nodes: tuple[str, str], periodic_function: PeriodicFunction = ConstantFunction(), R: float = 0) -> Component:
    return Component(
        type='periodic_voltage_source',
        id=id,
        value={'wavetype': periodic_function.wavetype,
               'V': periodic_function.amplitude,
               'w': 2*np.pi/periodic_function.period,
               'phi': periodic_function.phase,
               'R': R},
        nodes=nodes
        )

def dc_current_source(id: str, nodes: tuple[str, str], I: float, G: float = 0) -> Component:
    return Component(
        type='dc_current_source',
        id=id,
        value={'I': I, 'G': G, 'w': 0, 'phi': 0},
        nodes=nodes
        )

def ac_current_source(id: str, nodes: tuple[str, str], I: float, G: float = 0, w: float = 0, phi: float = 0) -> Component:
    return Component(
        type='ac_current_source',
        id=id,
        value={'I': I, 'G': G, 'w': w, 'phi': phi},
        nodes=nodes
        )

def complex_current_source(id: str, nodes: tuple[str, str], I: complex, Y: complex = 0) -> Component:
    return Component(
        type='complex_current_source',
        id=id,
        value={'I_real': I.real, 'I_imag': I.imag, 'G': Y.real, 'B': Y.imag},
        nodes=nodes
        )

def periodic_current_source(id: str, nodes: tuple[str, str], periodic_function: PeriodicFunction = ConstantFunction(), G: float = 0) -> Component:
    return Component(
        type='periodic_current_source',
        id=id,
        value={'wavetype': periodic_function.wavetype,
               'I': periodic_function.amplitude,
               'w': 2*np.pi/periodic_function.period,
               'phi': periodic_function.phase,
               'G': G},
        nodes=nodes
        )

def ground(id: str='gnd', nodes: tuple[str]=('0',)) -> Component:
    return Component(
        type='ground',
        id=id,
        nodes=nodes
    )

def is_active(component: Component) -> bool:
    if 'w' in component.value.keys():
        return True
    return False

def periodic_function(component: Component) -> PeriodicFunction: #TODO Exception path
    ...

@dataclass(frozen=True)
class TwoPoleComponent(Component):
    nodes : tuple[str, str]

@dataclass(frozen=True)
class Resistor(TwoPoleComponent):
    @property
    def R(self) -> float:
        return self.value.real
    type : str = field(default='resistor', init=False)

@dataclass(frozen=True)
class Conductance(TwoPoleComponent):
    @property
    def G(self) -> float:
        return self.value.real
    type : str = field(default='conductance', init=False)

@dataclass(frozen=True)
class Capacitor(TwoPoleComponent):
    C : float = 0
    type : str = field(default='capacitor', init=False)

@dataclass(frozen=True)
class Inductance(TwoPoleComponent):
    L : float = 0
    type : str = field(default='inductance', init=False)

@dataclass(frozen=True)
class Source(TwoPoleComponent):
    is_active : bool = field(default=True, init=False)
    w : float = field(default=0.0)
    phi : float = field(default=0.0)

@dataclass(frozen=True)
class CurrentSource(Source):
    @property
    def I(self) -> float:
        return self.value.real
    type : str = field(default='current_source', init=False)

@dataclass(frozen=True)
class VoltageSource(Source):
    @property
    def V(self) -> float:
        return self.value.real
    type : str = field(default='voltage_source', init=False)

@dataclass(frozen=True)
class LinearCurrentSource(CurrentSource):
    G : float = field(default=0.0)
    type : str = field(default='linear_current_source', init=False)

@dataclass(frozen=True)
class LinearVoltageSource(VoltageSource):
    R : float = field(default=0.0)
    type : str = field(default='linear_voltage_source', init=False)

@dataclass(frozen=True)
class PeriodicVoltageSource(VoltageSource):
    wavetype : Type[PeriodicFunction] = field(default=CosFunction)

    @property
    def time_properties(self) -> PeriodicFunction:
        return self.wavetype(period=2*np.pi/self.w, amplitude=self.V, phase=self.phi)

    @property
    def frequency_properties(self) -> HarmonicCoefficients:
        return fourier_series(self.time_properties)

    def frequency_components(self, w_max: float) -> npt.NDArray[np.double]:
        n_max = np.floor(w_max/self.w)
        return np.array([self.w*n for n in np.arange(n_max)])

@dataclass(frozen=True)
class PeriodicCurrentSource(CurrentSource):
    wavetype : Type[PeriodicFunction] = field(default=CosFunction)

    @property
    def time_properties(self) -> PeriodicFunction:
        return self.wavetype(period=2*np.pi/self.w, amplitude=self.I, phase=self.phi)

    @property
    def frequency_properties(self) -> HarmonicCoefficients:
        return fourier_series(self.time_properties)

    def frequency_components(self, w_max: float) -> npt.NDArray[np.double]:
        n_max = np.floor(w_max/self.w)
        return np.array([self.w*n for n in np.arange(n_max)])

@dataclass(frozen=True)
class Ground(Component):
    nodes : tuple[str]
    id : str = field(default='gnd')
    type : str = field(default='ground', init=False)
