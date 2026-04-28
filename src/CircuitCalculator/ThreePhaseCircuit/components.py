from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import cmath

from ..Circuit.Components.components import Component, complex_voltage_source, impedance


class NodeMappingError(ValueError):
    ...

def _phase_shift(base_value: complex, phase: str) -> complex:
    angles = {
        "a": 0.0,
        "b": -2 * cmath.pi / 3,
        "c": 2 * cmath.pi / 3,
    }
    return base_value * cmath.exp(1j * angles[phase])


@dataclass
class NodeExpander:
    """Expands single-line node labels into unique phase node labels."""

    suffixes: tuple[str, ...] = ("a", "b", "c", "n")
    _allocated: set[str] = field(default_factory=set, init=False)
    _phase_map: dict[tuple[str, str], str] = field(default_factory=dict, init=False)

    def _allocate(self, candidate: str) -> str:
        if candidate not in self._allocated:
            self._allocated.add(candidate)
            return candidate
        index = 2
        while f"{candidate}_{index}" in self._allocated:
            index += 1
        unique_name = f"{candidate}_{index}"
        self._allocated.add(unique_name)
        return unique_name

    def phase_node(self, node: str, phase: str) -> str:
        if phase not in self.suffixes:
            raise NodeMappingError(f"Unknown phase '{phase}'.")
        key = (node, phase)
        if key in self._phase_map:
            return self._phase_map[key]
        expanded = self._allocate(f"{node}.{phase}")
        self._phase_map[key] = expanded
        return expanded


@dataclass(frozen=True)
class ThreePhaseComponent(ABC):
    id: str
    nodes: tuple[str, ...]

    @abstractmethod
    def expand(self, expander: NodeExpander) -> list[Component]:
        ...


@dataclass(frozen=True)
class ThreePhaseVoltageSourceY(ThreePhaseComponent):
    V: complex
    Z: complex = 0j

    def expand(self, expander: NodeExpander) -> list[Component]:
        if len(self.nodes) != 2:
            raise NodeMappingError("ThreePhaseVoltageSourceY expects nodes=(phase_bus, neutral_bus).")
        phase_bus, neutral_bus = self.nodes
        neutral_node = expander.phase_node(neutral_bus, "n")
        return [
            complex_voltage_source(
                id=f"{self.id}.{phase}",
                nodes=(expander.phase_node(phase_bus, phase), neutral_node),
                V=_phase_shift(self.V, phase),
                Z=self.Z,
            )
            for phase in ("a", "b", "c")
        ]


@dataclass(frozen=True)
class ThreePhaseVoltageSourceDelta(ThreePhaseComponent):
    V: complex
    Z: complex = 0j

    def expand(self, expander: NodeExpander) -> list[Component]:
        if len(self.nodes) != 1:
            raise NodeMappingError("ThreePhaseVoltageSourceDelta expects nodes=(phase_bus,).")
        phase_bus = self.nodes[0]
        a = expander.phase_node(phase_bus, "a")
        b = expander.phase_node(phase_bus, "b")
        c = expander.phase_node(phase_bus, "c")
        return [
            complex_voltage_source(id=f"{self.id}.ab", nodes=(a, b), V=_phase_shift(self.V, "a"), Z=self.Z),
            complex_voltage_source(id=f"{self.id}.bc", nodes=(b, c), V=_phase_shift(self.V, "b"), Z=self.Z),
            complex_voltage_source(id=f"{self.id}.ca", nodes=(c, a), V=_phase_shift(self.V, "c"), Z=self.Z),
        ]


@dataclass(frozen=True)
class ThreePhaseLoadY(ThreePhaseComponent):
    Z: complex

    def expand(self, expander: NodeExpander) -> list[Component]:
        if len(self.nodes) != 2:
            raise NodeMappingError("ThreePhaseLoadY expects nodes=(phase_bus, neutral_bus).")
        phase_bus, neutral_bus = self.nodes
        neutral_node = expander.phase_node(neutral_bus, "n")
        return [
            impedance(id=f"{self.id}.{phase}", nodes=(expander.phase_node(phase_bus, phase), neutral_node), Z=self.Z)
            for phase in ("a", "b", "c")
        ]


@dataclass(frozen=True)
class ThreePhaseLoadDelta(ThreePhaseComponent):
    Z: complex

    def expand(self, expander: NodeExpander) -> list[Component]:
        if len(self.nodes) != 1:
            raise NodeMappingError("ThreePhaseLoadDelta expects nodes=(phase_bus,).")
        phase_bus = self.nodes[0]
        a = expander.phase_node(phase_bus, "a")
        b = expander.phase_node(phase_bus, "b")
        c = expander.phase_node(phase_bus, "c")
        return [
            impedance(id=f"{self.id}.ab", nodes=(a, b), Z=self.Z),
            impedance(id=f"{self.id}.bc", nodes=(b, c), Z=self.Z),
            impedance(id=f"{self.id}.ca", nodes=(c, a), Z=self.Z),
        ]
