import numpy as np
import numpy.typing as npt
from dataclasses import dataclass, field
from abc import ABC
from ..SignalProcessing.periodic_functions import PeriodicFunction, HarmonicCoefficients, fourier_series, CosFunction
from typing import Type
    
@dataclass(frozen=True)
class Component(ABC):
    nodes : tuple[str]
    type : str
    id : str
    is_active: bool = field(default=False, init=False)
    w: float = field(default=0, init=False)

@dataclass(frozen=True)
class TwoPoleComponent(Component):
    nodes : tuple[str, str]

@dataclass(frozen=True)
class Resistor(TwoPoleComponent):
    R : float
    type : str = field(default='resistor', init=False)

@dataclass(frozen=True)
class Conductance(TwoPoleComponent):
    G : float
    type : str = field(default='conductance', init=False)

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
    is_active : bool = field(default=True, init=False)
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
    id : str = field(default='gnd')
    type : str = field(default='ground', init=False)
    nodes : tuple[str]