from dataclasses import dataclass

from .network_components import Value


class ControlledSourceBase:
    @property
    def _control_factor(self) -> Value:
        raise NotImplementedError

    @property
    def is_voltage_source(self) -> bool:
        return False

    @property
    def is_current_source(self) -> bool:
        return False

    @property
    def is_ideal_voltage_source(self) -> bool:
        return False

    @property
    def is_ideal_current_source(self) -> bool:
        return False

    @property
    def is_controlled_source(self) -> bool:
        return True

    @property
    def is_controlled_current_source(self) -> bool:
        return False

    @property
    def is_controlled_voltage_source(self) -> bool:
        return False

    @property
    def is_voltage_controlled_current_source(self) -> bool:
        return False

    @property
    def is_current_controlled_current_source(self) -> bool:
        return False

    @property
    def is_voltage_controlled_voltage_source(self) -> bool:
        return False

    @property
    def is_current_controlled_voltage_source(self) -> bool:
        return False

    @property
    def is_active(self) -> bool:
        return self._control_factor != 0


class ControlledCurrentSourceBase(ControlledSourceBase):
    @property
    def is_controlled_current_source(self) -> bool:
        return True

    @property
    def is_controlled_voltage_source(self) -> bool:
        return False

    @property
    def is_short_circuit(self) -> bool:
        return False

    @property
    def is_open_circuit(self) -> bool:
        return self._control_factor == 0


class ControlledVoltageSourceBase(ControlledSourceBase):
    @property
    def is_controlled_current_source(self) -> bool:
        return False

    @property
    def is_controlled_voltage_source(self) -> bool:
        return True

    @property
    def is_short_circuit(self) -> bool:
        return self._control_factor == 0

    @property
    def is_open_circuit(self) -> bool:
        return False


@dataclass(frozen=True)
class VoltageControlledCurrentSource(ControlledCurrentSourceBase):
    name: str
    transconductance: Value
    control_node1: str
    control_node2: str
    type: str = 'voltage_controlled_current_source'

    @property
    def _control_factor(self) -> Value:
        return self.transconductance

    @property
    def is_voltage_controlled_current_source(self) -> bool:
        return True


@dataclass(frozen=True)
class CurrentControlledCurrentSource(ControlledCurrentSourceBase):
    name: str
    current_gain: Value
    control_branch: str
    type: str = 'current_controlled_current_source'

    @property
    def _control_factor(self) -> Value:
        return self.current_gain

    @property
    def is_current_controlled_current_source(self) -> bool:
        return True


@dataclass(frozen=True)
class VoltageControlledVoltageSource(ControlledVoltageSourceBase):
    name: str
    voltage_gain: Value
    control_node1: str
    control_node2: str
    type: str = 'voltage_controlled_voltage_source'

    @property
    def _control_factor(self) -> Value:
        return self.voltage_gain

    @property
    def is_voltage_controlled_voltage_source(self) -> bool:
        return True


@dataclass(frozen=True)
class CurrentControlledVoltageSource(ControlledVoltageSourceBase):
    name: str
    transresistance: Value
    control_branch: str
    type: str = 'current_controlled_voltage_source'

    @property
    def _control_factor(self) -> Value:
        return self.transresistance

    @property
    def is_current_controlled_voltage_source(self) -> bool:
        return True
