from typing import Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
import numpy as np
import sympy as sp

symbolic = sp.core.symbol.Symbol

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
    def Z(self) -> complex | symbolic:
        """Impedance value of element"""
        ...
    @property
    def Y(self) -> complex | symbolic:
        """Admittance value of element"""
        ...
    @property
    def V(self) -> complex | symbolic:
        """Voltage value of element"""
        ...
    @property
    def I(self) -> complex | symbolic:
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
    @property
    def is_active(self) -> bool:
        """Check if element is active"""
        ...
    @property
    def is_short_circuit(self) -> bool:
        """Check if element behaves as a short circuit"""
        ... 
    @property
    def is_open_circuit(self) -> bool:
        """Check if element behaves as an open circuit"""
        ...

@dataclass(frozen=True)
class NumericNortenTheveninElement(ABC):
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

    @property
    def is_active(self) -> bool:
        return self.is_voltage_source or self.is_current_source

    @property
    def is_short_circuit(self) -> bool:
        return self.V == 0 and self.Z == 0

    @property
    def is_open_circuit(self) -> bool:
        return self.I == 0 and self.Y == 0

@dataclass(frozen=True)
class NortenElement(NumericNortenTheveninElement):
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
class TheveninElement(NumericNortenTheveninElement):
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

@dataclass(frozen=True)
class SymbolicNortenTheveninElement(ABC):
    name: str
    type: str

    @property
    @abstractmethod
    def Z(self) -> symbolic: ...

    @property
    @abstractmethod
    def Y(self) -> symbolic: ...

    @property
    @abstractmethod
    def V(self) -> symbolic: ...

    @property
    @abstractmethod
    def I(self) -> symbolic: ...

    @property
    def is_voltage_source(self) -> bool:
        return self.V != 0 and self.V != sp.nan

    @property
    def is_current_source(self) -> bool:
        return self.I != 0 and self.I != sp.nan

    @property
    def is_ideal_voltage_source(self) -> bool:
        return self.V != sp.nan and self.Z == 0

    @property
    def is_ideal_current_source(self) -> bool:
        return self.I != sp.nan and self.Y == 0

    @property
    def is_active(self) -> bool:
        return self.is_voltage_source or self.is_current_source

    @property
    def is_short_circuit(self) -> bool:
        return self.V == 0 and self.Z == 0

    @property
    def is_open_circuit(self) -> bool:
        return self.I == 0 and self.Y == 0

@dataclass(frozen=True)
class SymbolicNortenElement(SymbolicNortenTheveninElement):
    V : symbolic = sp.sympify(0)
    Z : symbolic = sp.sympify(0)

    @property
    def Y(self) -> symbolic:
        if self.Z == 0:
            return sp.sympify('oo')
        if abs(self.Z) == sp.oo:
            return sp.sympify(0)
        return 1/self.Z # type: ignore
    
    @property
    def I(self) -> symbolic:
        if self.Z == 0:
            return sp.nan
        if abs(self.V) == sp.oo and abs(self.Z) == sp.oo:
            return sp.nan
        if abs(self.Z) == sp.oo:
            return sp.sympify(0)
        return self.V/self.Z # type: ignore

@dataclass(frozen=True)
class SymbolicTheveninElement(SymbolicNortenTheveninElement):
    I : symbolic = sp.sympify(0)
    Y : symbolic = sp.sympify(0)

    @property
    def Z(self) -> symbolic:
        if self.Y == 0:
            return sp.sympify('oo')
        if abs(self.Y) == sp.oo:
            return sp.sympify(0)
        return 1/self.Y # type: ignore
    
    @property
    def V(self) -> symbolic:
        if self.Y == 0:
            return sp.nan
        if abs(self.I) == sp.oo and abs(self.Y) == sp.oo:
            return sp.nan
        if abs(self.Y) == sp.oo:
            return sp.sympify(0)
        return self.I/self.Y # type: ignore