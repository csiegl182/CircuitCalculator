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
        return self.V != '0' and self.V != 'nan'

    @property
    def is_current_source(self) -> bool:
        return self.I != '0' and self.I != 'nan'

    @property
    def is_ideal_voltage_source(self) -> bool:
        return self.V != 'nan' and self.Z == '0'

    @property
    def is_ideal_current_source(self) -> bool:
        return self.I != 'nan' and self.Y == '0'

    @property
    def is_active(self) -> bool:
        return self.is_voltage_source or self.is_current_source

    @property
    def is_short_circuit(self) -> bool:
        return self.V == '0' and self.Z == '0'

    @property
    def is_open_circuit(self) -> bool:
        return self.I == '0' and self.Y == '0'

@dataclass(frozen=True)
class SymbolicNortenElement(SymbolicNortenTheveninElement):
    V : str = '0'
    Z : str = '0'

    @property
    def Y(self) -> str:
        if self.Z == '0':
            return 'oo'
        if self.Z == 'oo':
            return '0'
        return f'1/{self.Z}'
    
    @property
    def I(self) -> str:
        if self.Z == '0':
            return 'nan'
        if self.V == 'oo' and self.Z == 'oo':
            return 'nan'
        if self.Z == 'oo':
            return '0'
        if self.V == '0':
            return '0'
        return f'{self.V}/{self.Z}'

@dataclass(frozen=True)
class SymbolicTheveninElement(SymbolicNortenTheveninElement):
    I : str = '0'
    Y : str = '0'

    @property
    def Z(self) -> str:
        if self.Y == '0':
            return 'oo'
        if self.Y == 'oo':
            return '0'
        return f'1/{self.Y}'
    
    @property
    def V(self) -> str:
        if self.Y == '0':
            return 'nan'
        if self.I == 'oo' and self.Y == 'oo':
            return 'nan'
        if self.Y == 'oo':
            return '0'
        if self.I == '0':
            return '0'
        return f'{self.I}/{self.Y}'