from typing import Protocol
from dataclasses import dataclass
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
    def Z(self) -> complex:
        """Impedance value of element"""
        ...
    @property
    def Y(self) -> complex:
        """Admittance value of element"""
        ...
    @property
    def V(self) -> complex:
        """Voltage value of element"""
        ...
    @property
    def I(self) -> complex:
        """Current value of element"""
        ...

@dataclass(frozen=True)
class NortenElement:
    name : str
    type : str
    Z : complex
    V : complex

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
class TheveninElement:
    name : str
    type : str
    Y : complex
    I : complex

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

def complex_value(X : float, phi : float = 0.0, rms: bool = False, deg: bool = False):
    if rms:
        X *= np.sqrt(2)
    if deg:
        phi = np.radians(phi)
    if not np.isfinite(X):
        return complex(np.inf, 0)
    return X*complex(np.cos(phi), np.sin(phi))

def is_voltage_source(element: NortenTheveninElement) -> bool:
    return np.abs(element.V) > 0

def is_current_source(element: NortenTheveninElement) -> bool:
    return np.abs(element.I) > 0

def is_ideal_voltage_source(element: NortenTheveninElement) -> bool:
    return np.abs(element.V) >= 0 and element.Z==0

def is_ideal_current_source(element: NortenTheveninElement) -> bool:
    return np.abs(element.I) >= 0 and element.Y==0

def is_active(element: NortenTheveninElement) -> bool:
    return is_voltage_source(element) or is_current_source(element)

def is_short_circuit(element: NortenTheveninElement) -> bool:
    return element.V == 0 and element.Z == 0

def is_open_circuit(element: NortenTheveninElement) -> bool:
    return element.I == 0 and element.Y == 0

