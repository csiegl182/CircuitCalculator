from typing import Protocol
from dataclasses import dataclass, field
import numpy as np

class Element(Protocol):
    @property
    def Z(self) -> complex:
        """Impedance of Branch"""
    @property
    def Y(self) -> complex:
        """Admittance of Branch"""
    @property
    def I(self) -> complex:
        """Current of Branch"""
    @property
    def U(self) -> complex:
        """Voltage of Branch"""
    @property
    def active(self) -> bool:
        """Whether or not the branch is active"""

@dataclass(frozen=True)
class Impedeance:
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
class RealCurrentSource:
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
    Z : complex = field(default=np.inf, init=False)
    Y : complex = field(default=0, init=False)
    I : complex
    U : complex = field(default=np.nan, init=False)
    active: bool = field(default=True, init=False)

@dataclass(frozen=True)
class RealVoltageSource:
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
    Z : complex = field(default=0, init=False)
    Y : complex = field(default=np.inf, init=False)
    U : complex
    I : complex = field(default=np.nan, init=False)
    active: bool = field(default=True, init=False)

def resistor(R : float, **_) -> Element:
    return Impedeance(Z=R)

def conductor(G : float, **_) -> Element:
    try:
        return Impedeance(Z=1/G)
    except ZeroDivisionError:
        return Impedeance(Z=np.inf)

def real_current_source(I : float, R : float, **_) -> Element:
    return RealCurrentSource(I=I, Z=R)

def current_source(I : float, **_) -> Element:
    return CurrentSource(I=I)

def real_voltage_source(U : float, R : float, **_) -> Element:
    return RealVoltageSource(U=U, Z=R)

def voltage_source(U : float, **_) -> Element:
    return VoltageSource(U=U)

def is_current_source(element: Element) -> bool:
    return element.active and np.isfinite(element.I)

def is_ideal_voltage_source(element: Element) -> bool:
    return element.active and element.Z==0 and np.isfinite(element.U)

def is_ideal_current_source(element: Element) -> bool:
    return element.active and element.Y==0 and np.isfinite(element.I)