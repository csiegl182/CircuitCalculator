from typing import Protocol, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from .types import TimeDomainFunction
import numpy as np

class UnknownWavetype(Exception):
    ...

class TransformationError(Exception):
    ...

@dataclass
class PeriodicFunction(Protocol):
    period: float
    amplitude: float
    phase: float
    wavetype: str = ''

    @property
    def time_function(self) -> TimeDomainFunction:
        ...

PeriodicFunctionList = list[Type[PeriodicFunction]]

@dataclass
class HarmonicCoefficients(Protocol):
    amplitude0: float
    phase0: float

    def amplitude(self, n: int) -> float:
        ...

    def phase(self, n: int) -> float:
        ...

    def real(self, n: int) -> float:
        ...
    
    def imag(self, n: int) -> float:
        ...

    def c(self, n: int) -> complex:
        ...

@dataclass
class AbstractHarmonicCoefficients(ABC):
    amplitude0: float = 1
    phase0: float = 0

    def amplitude(self, n: int) -> float:
        if n < 0:
            raise ValueError('Fourier index must be positive.')
        return self._amplitude_coefficient(n)

    def phase(self, n: int) -> float:
        if n < 0:
            raise ValueError('Fourier index must be positive.')
        return self._phase_coefficient(n)

    def real(self, n: int) -> float:
        return self.amplitude(n)*np.cos(self.phase(n))
    
    def imag(self, n: int) -> float:
        return self.amplitude(n)*np.sin(self.phase(n))

    def c(self, n: int) -> complex:
        if n < 0:
            return self.amplitude(-n)/2*np.exp(1j*self.phase(-n))
        return self.amplitude(n)/2*np.exp(-1j*self.phase(n))

    @abstractmethod
    def _amplitude_coefficient(self, n: int) -> float:
        ...

    @abstractmethod
    def _phase_coefficient(self, n: int) -> float:
        ...

@dataclass
class ConstantFunction:
    period: float = field(default=0)
    amplitude: float = field(default=1)
    phase: float = field(default=0)
    wavetype: str = 'const'

    @property
    def time_function(self) -> TimeDomainFunction:
        return lambda t: self.amplitude*np.ones(t.shape)

class ConstFunctionHarmonics(AbstractHarmonicCoefficients):
    def _amplitude_coefficient(self, n: int) -> float:
        if n == 0:
            return self.amplitude0
        return 0

    def _phase_coefficient(self, _: int) -> float:
        return 0

@dataclass
class CosFunction:
    period: float
    amplitude: float
    phase: float = field(default=0)
    wavetype: str = 'cos'

    @property
    def time_function(self) -> TimeDomainFunction:
        return lambda t: self.amplitude*np.cos(2*np.pi/self.period*t + self.phase)

class CosFunctionHarmonics(AbstractHarmonicCoefficients):
    def _amplitude_coefficient(self, n: int) -> float:
        if n == 1:
            return self.amplitude0
        return 0

    def _phase_coefficient(self, n: int) -> float:
        if n == 1:
            return -self.phase0
        return 0

@dataclass
class SinFunction:
    period: float
    amplitude: float
    phase: float = field(default=0)
    wavetype: str = 'sin'

    @property
    def time_function(self) -> TimeDomainFunction:
        return lambda t: self.amplitude*np.sin(2*np.pi/self.period*t + self.phase)

class SinFunctionHarmonics(AbstractHarmonicCoefficients):
    def _amplitude_coefficient(self, n: int) -> float:
        if n == 1:
            return self.amplitude0
        return 0

    def _phase_coefficient(self, n: int) -> float:
        if n == 1:
            return np.pi/2-self.phase0
        return 0

@dataclass
class RectFunction:
    period: float
    amplitude: float
    phase: float
    wavetype: str = 'rect'

    @property
    def time_function(self) -> TimeDomainFunction:
        t0 = self.phase/2/np.pi*self.period
        return np.vectorize(lambda t: self.amplitude if (t+t0) % self.period < self.period/2 else -self.amplitude)

class RectFunctionHarmonics(AbstractHarmonicCoefficients):
    def _amplitude_coefficient(self, n: int) -> float:
        if n%2 == 0:
            return 0
        return 4/n/np.pi*self.amplitude0

    def _phase_coefficient(self, n: int) -> float:
        if n%2 == 0:
            return 0
        return np.pi/2-n*self.phase0

@dataclass
class TriFunction:
    period: float
    amplitude: float
    phase: float
    wavetype: str = 'tri'

    @property
    def time_function(self) -> TimeDomainFunction:
        t0 = self.phase/2/np.pi*self.period
        mod = lambda t: np.mod(t, self.period)
        return np.vectorize(lambda t: self.amplitude*(1-4/self.period*mod(t+t0)) if mod(t+t0) < self.period/2 else self.amplitude*(-3+4/self.period*(mod(t+t0))))

class TriFunctionHarmonics(AbstractHarmonicCoefficients):
    def _amplitude_coefficient(self, n: int) -> float:
        if n%2 == 0:
            return 0
        return 8/n/n/np.pi/np.pi*self.amplitude0

    def _phase_coefficient(self, n: int) -> float:
        if n%2 == 0:
            return 0
        return -n*self.phase0

@dataclass
class SawFunction:
    period: float
    amplitude: float
    phase: float
    wavetype: str = 'saw'

    @property
    def time_function(self) -> TimeDomainFunction:
        t0 = self.phase/2/np.pi*self.period
        mod = lambda t: np.mod(t, self.period)
        return np.vectorize(lambda t: self.amplitude*(2/self.period*mod(t+t0)-1))

class SawFunctionHarmonics(AbstractHarmonicCoefficients):
    def _amplitude_coefficient(self, n: int) -> float:
        if n == 0:
            return 0
        return -2/n/np.pi*self.amplitude0

    def _phase_coefficient(self, n: int) -> float:
        if n == 0:
            return 0
        return np.pi/2-n*self.phase0

fourier_series_mapping: dict[Type[PeriodicFunction], Type[HarmonicCoefficients]] = {
    ConstantFunction: ConstFunctionHarmonics,
    CosFunction: CosFunctionHarmonics,
    SinFunction: SinFunctionHarmonics,
    RectFunction: RectFunctionHarmonics,
    TriFunction: TriFunctionHarmonics,
    SawFunction: SawFunctionHarmonics,
}

periodic_functions : PeriodicFunctionList = list(fourier_series_mapping.keys())

def fourier_series(time_function: PeriodicFunction) -> HarmonicCoefficients:
    try:
        return fourier_series_mapping[type(time_function)](amplitude0=time_function.amplitude, phase0=time_function.phase)
    except KeyError:
        raise TransformationError(f'No fourier coefficents found for time function of type {type(time_function).__name__}')

def periodic_function(wavetype: str) -> Type[PeriodicFunction]:
    try:
        return [pf for pf in periodic_functions if pf.wavetype == wavetype][0]
    except IndexError:
        raise UnknownWavetype(f'Periodic function of type {wavetype} is unknown.')