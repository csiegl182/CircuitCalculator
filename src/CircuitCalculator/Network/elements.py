from typing import Protocol
from dataclasses import dataclass, field
import numpy as np

class Element(Protocol):
    @property
    def name(self) -> str:
        """ID of element"""
    @property
    def Z(self) -> complex:
        """Impedance value of element"""
    @property
    def Y(self) -> complex:
        """Admittance value of element"""
    @property
    def I(self) -> complex:
        """Current value of element"""
    @property
    def U(self) -> complex:
        """Voltage value of element"""
    @property
    def active(self) -> bool:
        """Whether or not the element is active"""

@dataclass(frozen=True)
class Impedance:
    name : str
    Z : complex
    I : complex = field(default=np.nan, init=False)
    U : complex = field(default=np.nan, init=False)
    active: bool = field(default=False, init=False)
    @property
    def Y(self) -> complex:
        try:
            return 1/self.Z
        except ZeroDivisionError:
            return np.inf

@dataclass(frozen=True)
class LinearCurrentSource:
    name : str
    Z : complex
    I : complex
    active: bool = field(default=True, init=False)
    @property
    def Y(self) -> complex:
        try:
            return 1/self.Z
        except ZeroDivisionError:
            return np.inf
    @property
    def U(self) -> complex:
        try:
            return self.I/self.Y
        except ZeroDivisionError:
            return np.nan

@dataclass(frozen=True)
class CurrentSource:
    name : str
    Z : complex = field(default=np.inf, init=False)
    Y : complex = field(default=0, init=False)
    I : complex
    U : complex = field(default=np.nan, init=False)
    active: bool = field(default=True, init=False)

@dataclass(frozen=True)
class LinearVoltageSource:
    name : str
    Z : complex
    U : complex
    active: bool = field(default=True, init=False)
    @property
    def Y(self) -> complex:
        try:
            return 1/self.Z
        except ZeroDivisionError:
            return np.inf
    @property
    def I(self) -> complex:
        try:
            return self.U/self.Z
        except ZeroDivisionError:
            return np.nan

@dataclass(frozen=True)
class VoltageSource:
    name : str
    Z : complex = field(default=0, init=False)
    Y : complex = field(default=np.inf, init=False)
    U : complex
    I : complex = field(default=np.nan, init=False)
    active: bool = field(default=True, init=False)

def resistor(name : str, R : float, **_) -> Element:
    return Impedance(Z=R, name=name)

def conductor(name : str, G : float, **_) -> Element:
    try:
        return Impedance(Z=1/G, name=name)
    except ZeroDivisionError:
        return Impedance(Z=np.inf, name=name)

def impedance(name : str, R : float = 0.0, X : float = 0.0, absZ : float = -1.0, phi : float = 0.0, degree : bool = False, **_) -> Element:
    if degree:
        phi *= np.pi/180
    if absZ > 0:
        return Impedance(Z=complex(absZ*np.cos(phi), absZ*np.sin(phi)), name=name)
    return Impedance(Z=complex(R, X), name=name)

def linear_current_source(name : str, I : float, R : float, **_) -> Element:
    return LinearCurrentSource(I=I, Z=R, name=name)

def current_source(name : str, I : float, **_) -> Element:
    return CurrentSource(I=I, name=name)

def linear_voltage_source(name : str, U : float, R : float, **_) -> Element:
    return LinearVoltageSource(U=U, Z=R, name=name)

def voltage_source(name : str, U : float, **_) -> Element:
    return VoltageSource(U=U, name=name)

def is_current_source(element: Element) -> bool:
    return element.active and np.isfinite(element.I)

def is_ideal_voltage_source(element: Element) -> bool:
    return element.active and element.Z==0 and np.isfinite(element.U)

def is_ideal_current_source(element: Element) -> bool:
    return element.active and element.Y==0 and np.isfinite(element.I)