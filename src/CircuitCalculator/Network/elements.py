from typing import Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
import numpy as np

class NortenTheveninElement(Protocol):
    @property
    def name(self) -> str:
        """Name of element"""
        ...
    @property
    def type(self) -> str:
        """Specific element type"""
        ...
    @property
    def Z(self) -> complex | str:
        """Impedance value of element"""
        ...
    @property
    def Y(self) -> complex | str:
        """Admittance value of element"""
        ...
    @property
    def V(self) -> complex | str:
        """Voltage value of element"""
        ...
    @property
    def I(self) -> complex | str:
        """Current value of element"""
        ...
    @property
    def is_voltage_source(self) -> bool:
        """Check if element behaves as a linear voltage source"""
        ...
    @property
    def is_current_source(self) -> bool:
        """Check if element behaves as a linear current source"""
        ...
    @property
    def is_ideal_voltage_source(self) -> bool:
        """Check if element behaves as an ideal voltage source"""
        ...
    @property
    def is_ideal_current_source(self) -> bool:
        """Check if element behaves as an ideal current source"""
        ...

@dataclass(frozen=True)
class NummericNortenTheveninElement(ABC):
    name: str
    type: str

    @property
    @abstractmethod
    def Z(self) -> complex: ...

    @property
    @abstractmethod
    def Y(self) -> complex: ...

    @property
    @abstractmethod
    def V(self) -> complex: ...

    @property
    @abstractmethod
    def I(self) -> complex: ...

    @property
    def is_voltage_source(self) -> bool:
        return np.abs(self.V) > 0

    @property
    def is_current_source(self) -> bool:
        return np.abs(self.I) > 0

    @property
    def is_ideal_voltage_source(self) -> bool:
        return np.abs(self.V) >= 0 and self.Z==0

    @property
    def is_ideal_current_source(self) -> bool:
        return np.abs(self.I) >= 0 and self.Y==0

@dataclass(frozen=True)
class NortenElement(NummericNortenTheveninElement):
    V : complex = 0
    Z : complex = 0

    @property
    def Y(self) -> complex:
        try:
            return 1/self.Z
        except ZeroDivisionError:
            return np.inf

    @property
    def I(self) -> complex:
        try:
            return complex(self.V)/self.Z
        except ZeroDivisionError:
            return np.nan

@dataclass(frozen=True)
class TheveninElement(NummericNortenTheveninElement):
    I : complex = 0
    Y : complex = 0

    @property
    def Z(self) -> complex:
        try:
            return 1/self.Y
        except ZeroDivisionError:
            return np.inf

    @property
    def V(self) -> complex:
        try:
            return complex(self.I)/self.Y
        except ZeroDivisionError:
            return np.nan

dataclass(frozen=True)
class SymbolicNortenTheveninElement(ABC):
    name : str
    type : str

    @property
    @abstractmethod
    def Z(self) -> str: ...

    @property
    @abstractmethod
    def Y(self) -> str: ...

    @property
    @abstractmethod
    def V(self) -> str: ...

    @property
    @abstractmethod
    def I(self) -> str: ...

    @property
    def is_voltage_source(self) -> bool:
        return self.V != '0'

    @property
    def is_current_source(self) -> bool:
        return self.I != '0'

    @property
    def is_ideal_voltage_source(self) -> bool:
        return self.V != 'nan' and self.Z == '0'

    @property
    def is_ideal_current_source(self) -> bool:
        return self.I != 'nan' and self.Y == '0'

@dataclass(frozen=True)
class SymbolicNortenElement(SymbolicNortenTheveninElement):
    V : str = '0'
    Z : str = '0'

    @property
    def Y(self) -> str:
        if self.Z == '0':
            return 'oo'
        return f'1/{self.Z}'
    
    @property
    def I(self) -> str:
        if self.Z == '0':
            return 'nan'
        return f'{self.V}/{self.Z}'

@dataclass(frozen=True)
class SymbolicTheveninElement(SymbolicNortenTheveninElement):
    I : str = '0'
    Y : str = '0'

    @property
    def Z(self) -> str:
        if self.Y == '0':
            return 'oo'
        return f'1/{self.Y}'
    
    @property
    def V(self) -> str:
        if self.Y == '0':
            return 'nan'
        return f'{self.I}/{self.Y}'

def impedance(name : str, Z : complex) -> NortenTheveninElement:
    return NortenElement(Z=Z, V=0, name=name, type='impedance')

def admittance(name : str, Y : complex) -> NortenTheveninElement:
    return TheveninElement(Y=Y, I=0, name=name, type='admittance')

def resistor(name : str, R : float) -> NortenTheveninElement:
    return NortenElement(Z=R, V=0, name=name, type='resistor')

def conductor(name : str, G : float) -> NortenTheveninElement:
    return TheveninElement(Y=G, I=0, name=name, type='conductor')

def load(name : str, P : float, V_ref: float = -1, I_ref: float = -1, Q : float = 0) -> NortenTheveninElement:
    if V_ref < 0 and I_ref < 0:
        raise AttributeError('A reference voltage or reference current has to be defined for a load.')
    if V_ref > 0 and I_ref > 0:
        raise AttributeError('You can only define a reference voltage or a reference current for a load.')
    if V_ref == 0 and I_ref < 0:
        raise ValueError('Reference voltage must be greater than zero.')
    if I_ref <= 0 and V_ref < 0:
        raise ValueError('Reference current must be greater than zero.')
    if V_ref > 0:
        return TheveninElement(Y=complex(P, Q)/V_ref**2, I=0, name=name, type='load')
    return NortenElement(Z=complex(P, Q)/I_ref**2, V=0, name=name, type='load')

def voltage_source(name : str, V : complex, Z : complex = 0) -> NortenTheveninElement:
    return NortenElement(V=V, Z=Z, name=name, type='voltage_source')

def current_source(name : str, I : complex, Y : complex = 0) -> NortenTheveninElement:
    return TheveninElement(I=I, Y=Y, name=name, type='current_source')

def open_circuit(name : str) -> NortenTheveninElement:
    return TheveninElement(I=0, Y=0, name=name, type='open_circuit')

def short_circuit(name : str) -> NortenTheveninElement:
    return NortenElement(V=0, Z=0, name=name, type='short_circuit')

## TODO: IS THIS NEEDED?

def is_active(element: NortenTheveninElement) -> bool:
    return element.is_voltage_source or element.is_current_source

def is_short_circuit(element: NortenTheveninElement) -> bool:
    return element.V == 0 and element.Z == 0

def is_open_circuit(element: NortenTheveninElement) -> bool:
    return element.I == 0 and element.Y == 0

def impedance_value(R : float = 0.0, X : float = 0.0, absZ : float = -1.0, phi : float = 0.0, degree : bool = False) -> complex:
    if degree:
        phi *= np.pi/180
    if absZ > 0:
        return complex(absZ*np.cos(phi), absZ*np.sin(phi))
    return complex(R, X)

def admittance_value(G : float = 0.0, B : float = 0.0, absY : float = -1.0, phi : float = 0.0, degree : bool = False) -> complex:
    if degree:
        phi *= np.pi/180
    if absY > 0:
        return complex(absY*np.cos(phi), absY*np.sin(phi))
    return complex(G, B)

def complex_value(X : float, phi : float = 0.0, rms: bool = False, deg: bool = False) -> complex:
    if rms:
        X *= np.sqrt(2)
    if deg:
        phi = np.radians(phi)
    if not np.isfinite(X):
        return complex(np.inf, 0)
    return X*complex(np.cos(phi), np.sin(phi))