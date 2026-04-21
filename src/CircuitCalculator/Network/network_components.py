from typing import Protocol

import sympy as sp

symbolic = sp.core.symbol.Symbol
Value = complex | symbolic


class NetworkComponent(Protocol):
    @property
    def name(self) -> str:
        """Name of element"""
        ...

    @property
    def type(self) -> str:
        """Specific element type"""
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
    def is_controlled_source(self) -> bool:
        """Check if element behaves as a controlled source"""
        ...

    @property
    def is_controlled_current_source(self) -> bool:
        """Check if element output is a controlled current"""
        ...

    @property
    def is_controlled_voltage_source(self) -> bool:
        """Check if element output is a controlled voltage"""
        ...

    @property
    def is_voltage_controlled_current_source(self) -> bool:
        """Check if element behaves as a voltage controlled current source"""
        ...

    @property
    def is_current_controlled_current_source(self) -> bool:
        """Check if element behaves as a current controlled current source"""
        ...

    @property
    def is_voltage_controlled_voltage_source(self) -> bool:
        """Check if element behaves as a voltage controlled voltage source"""
        ...

    @property
    def is_current_controlled_voltage_source(self) -> bool:
        """Check if element behaves as a current controlled voltage source"""
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


class TwoTerminalComponent(NetworkComponent):
    """Network component connected by one branch."""


class NortenTheveninElement(TwoTerminalComponent):
    @property
    def Z(self) -> Value:
        """Impedance value of element"""
        ...

    @property
    def Y(self) -> Value:
        """Admittance value of element"""
        ...

    @property
    def V(self) -> Value:
        """Voltage value of element"""
        ...

    @property
    def I(self) -> Value:
        """Current value of element"""
        ...


class ControlledSource(TwoTerminalComponent):
    """Source whose output is controlled by another network quantity."""


class VoltageControlledCurrentSourceElement(ControlledSource):
    transconductance: Value
    control_node1: str
    control_node2: str


class CurrentControlledCurrentSourceElement(ControlledSource):
    current_gain: Value
    control_branch: str


class VoltageControlledVoltageSourceElement(ControlledSource):
    voltage_gain: Value
    control_node1: str
    control_node2: str


class CurrentControlledVoltageSourceElement(ControlledSource):
    transresistance: Value
    control_branch: str
