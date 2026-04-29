from __future__ import annotations

from dataclasses import dataclass, field

from ..Circuit.circuit import Circuit
from .components import NodeExpander, ThreePhaseComponent


class AmbiguousThreePhaseComponentID(Exception):
    ...


@dataclass(frozen=True)
class ThreePhaseCircuit:
    components: list[ThreePhaseComponent]
    ground_node: str | None = field(default=None)

    def __post_init__(self) -> None:
        if any(component.id == "" for component in self.components):
            raise ValueError("Component ID must not be empty.")
        ids = [component.id for component in self.components]
        if len(set(ids)) != len(ids):
            raise AmbiguousThreePhaseComponentID("Component list contains multiple components with the same ID.")


def transform_three_phase_circuit(circuit: ThreePhaseCircuit) -> Circuit:
    expander = NodeExpander()
    components = [component for tp_component in circuit.components for component in tp_component.expand(expander)]

    ground_node = None
    if circuit.ground_node:
        ground_node = expander.phase_node(circuit.ground_node, "n")

    return Circuit(components=components, ground_node=ground_node)
