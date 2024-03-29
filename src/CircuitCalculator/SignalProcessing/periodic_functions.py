from typing import Protocol, Type
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

@dataclass
class ConstantFunction:
    period: float = 0
    amplitude: float = 1
    phase: float = 0
    wavetype: str = 'const'

    @property
    def time_function(self) -> TimeDomainFunction:
        return lambda t: self.amplitude*np.ones(t.shape)

@dataclass
class ConstFunctionHarmonics:
    amplitude0: float = 1
    phase0: float = 0

    def amplitude(self, n: int) -> float:
        if n < 0:
            raise ValueError('Fourier index must be positive.')
        if n == 0:
            return self.amplitude0
        return 0

    def phase(self, n: int) -> float:
        if n < 0:
            raise ValueError('Fourier index must be positive.')
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

@dataclass
class CosFunctionHarmonics:
    amplitude0: float
    phase0: float

    def amplitude(self, n: int) -> float:
        if n < 0:
            raise ValueError('Fourier index must be positive.')
        if n == 1:
            return self.amplitude0
        return 0

    def phase(self, n: int) -> float:
        if n < 0:
            raise ValueError('Fourier index must be positive.')
        if n == 1:
            return self.phase0
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

@dataclass
class RectFunctionHarmonics:
    amplitude0: float
    phase0: float

    def amplitude(self, n: int) -> float:
        if n < 0:
            raise ValueError('Fourier index must be positive.')
        if n%2 == 0:
            return 0
        return 4/n/np.pi*self.amplitude0

    def phase(self, n: int) -> float:
        if n < 0:
            raise ValueError('Fourier index must be positive.')
        if n%2 == 0:
            return 0
        return n*self.phase0-np.pi/2

fourier_series_mapping: dict[Type[PeriodicFunction], Type[HarmonicCoefficients]] = {
    CosFunction: CosFunctionHarmonics,
    RectFunction: RectFunctionHarmonics
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