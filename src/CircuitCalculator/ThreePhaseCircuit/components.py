from __future__ import annotations

import cmath
from dataclasses import dataclass, field
from typing import Callable, Literal

from ..Circuit.Components.components import Component, complex_current_source, complex_voltage_source, impedance

Phase = Literal["a", "b", "c"]
PhaseFactory = Callable[[str, tuple[str, str]], Component]


class NodeMappingError(ValueError):
    ...


def _phase_shift(base_value: complex, phase: Phase) -> complex:
    angles: dict[Phase, float] = {
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
class ThreePhaseComponent:
    id: str
    nodes: tuple[str, ...]
    _expander: Callable[[str, tuple[str, ...], NodeExpander], list[Component]]

    def expand(self, expander: NodeExpander) -> list[Component]:
        return self._expander(self.id, self.nodes, expander)


def _line_phase_nodes(nodes: tuple[str, ...], expander: NodeExpander) -> tuple[tuple[str, str], tuple[str, str], tuple[str, str]]:
    if len(nodes) != 2:
        raise NodeMappingError("line topology expects nodes=(from_bus, to_bus).")
    n1, n2 = nodes
    return (
        (expander.phase_node(n1, "a"), expander.phase_node(n2, "a")),
        (expander.phase_node(n1, "b"), expander.phase_node(n2, "b")),
        (expander.phase_node(n1, "c"), expander.phase_node(n2, "c")),
    )


def _star_phase_nodes(nodes: tuple[str, ...], expander: NodeExpander) -> tuple[tuple[str, str], tuple[str, str], tuple[str, str]]:
    if len(nodes) != 2:
        raise NodeMappingError("star topology expects nodes=(phase_bus, neutral_bus).")
    phase_bus, neutral_bus = nodes
    neutral_node = expander.phase_node(neutral_bus, "n")
    return (
        (expander.phase_node(phase_bus, "a"), neutral_node),
        (expander.phase_node(phase_bus, "b"), neutral_node),
        (expander.phase_node(phase_bus, "c"), neutral_node),
    )


def _delta_phase_nodes(nodes: tuple[str, ...], expander: NodeExpander) -> tuple[tuple[str, str], tuple[str, str], tuple[str, str]]:
    if len(nodes) != 1:
        raise NodeMappingError("delta topology expects nodes=(phase_bus,).")
    phase_bus = nodes[0]
    a = expander.phase_node(phase_bus, "a")
    b = expander.phase_node(phase_bus, "b")
    c = expander.phase_node(phase_bus, "c")
    return ((a, b), (b, c), (c, a))


def _phase_nodes(topology: Literal["line", "star", "delta"], nodes: tuple[str, ...], expander: NodeExpander) -> tuple[tuple[str, str], tuple[str, str], tuple[str, str]]:
    if topology == "line":
        return _line_phase_nodes(nodes, expander)
    if topology == "star":
        return _star_phase_nodes(nodes, expander)
    return _delta_phase_nodes(nodes, expander)


def _expand_custom_component(
    topology: Literal["line", "star", "delta"],
    id: str,
    nodes: tuple[str, ...],
    phase_a: PhaseFactory,
    phase_b: PhaseFactory,
    phase_c: PhaseFactory,
) -> ThreePhaseComponent:
    def _expand(comp_id: str, comp_nodes: tuple[str, ...], expander: NodeExpander) -> list[Component]:
        node_pairs = _phase_nodes(topology, comp_nodes, expander)
        suffixes = ("a", "b", "c") if topology != "delta" else ("ab", "bc", "ca")
        factories = (phase_a, phase_b, phase_c)
        return [
            factory(f"{comp_id}.{suffix}", pair)
            for factory, suffix, pair in zip(factories, suffixes, node_pairs)
        ]

    return ThreePhaseComponent(id=id, nodes=nodes, _expander=_expand)


def three_phase_custom_component_line(
    id: str,
    nodes: tuple[str, ...],
    phase_a: PhaseFactory,
    phase_b: PhaseFactory,
    phase_c: PhaseFactory,
) -> ThreePhaseComponent:
    return _expand_custom_component("line", id, nodes, phase_a, phase_b, phase_c)


def three_phase_custom_component_star(
    id: str,
    nodes: tuple[str, ...],
    phase_a: PhaseFactory,
    phase_b: PhaseFactory,
    phase_c: PhaseFactory,
) -> ThreePhaseComponent:
    return _expand_custom_component("star", id, nodes, phase_a, phase_b, phase_c)


def three_phase_custom_component_delta(
    id: str,
    nodes: tuple[str, ...],
    phase_a: PhaseFactory,
    phase_b: PhaseFactory,
    phase_c: PhaseFactory,
) -> ThreePhaseComponent:
    return _expand_custom_component("delta", id, nodes, phase_a, phase_b, phase_c)


def three_phase_voltage_source_star(id: str, nodes: tuple[str, ...], V: complex, Z: complex = 0j) -> ThreePhaseComponent:
    suffix_phase: dict[str, Phase] = {"a": "a", "b": "b", "c": "c", "ab": "a", "bc": "b", "ca": "c"}

    def f(suffix: str) -> PhaseFactory:
        return lambda cid, pair: complex_voltage_source(id=cid, nodes=pair, V=_phase_shift(V, suffix_phase[suffix]), Z=Z)

    return three_phase_custom_component_star(id=id, nodes=nodes, phase_a=f("a"), phase_b=f("b"), phase_c=f("c"))


def three_phase_voltage_source_delta(id: str, nodes: tuple[str, ...], V: complex, Z: complex = 0j) -> ThreePhaseComponent:
    suffix_phase: dict[str, Phase] = {"a": "a", "b": "b", "c": "c", "ab": "a", "bc": "b", "ca": "c"}

    def f(suffix: str) -> PhaseFactory:
        return lambda cid, pair: complex_voltage_source(id=cid, nodes=pair, V=_phase_shift(V, suffix_phase[suffix]), Z=Z)

    return three_phase_custom_component_delta(id=id, nodes=nodes, phase_a=f("ab"), phase_b=f("bc"), phase_c=f("ca"))


def three_phase_current_source_star(id: str, nodes: tuple[str, ...], I: complex, Y: complex = 0j) -> ThreePhaseComponent:
    suffix_phase: dict[str, Phase] = {"a": "a", "b": "b", "c": "c", "ab": "a", "bc": "b", "ca": "c"}

    def f(suffix: str) -> PhaseFactory:
        return lambda cid, pair: complex_current_source(id=cid, nodes=pair, I=_phase_shift(I, suffix_phase[suffix]), Y=Y)

    return three_phase_custom_component_star(id=id, nodes=nodes, phase_a=f("a"), phase_b=f("b"), phase_c=f("c"))


def three_phase_current_source_delta(id: str, nodes: tuple[str, ...], I: complex, Y: complex = 0j) -> ThreePhaseComponent:
    suffix_phase: dict[str, Phase] = {"a": "a", "b": "b", "c": "c", "ab": "a", "bc": "b", "ca": "c"}

    def f(suffix: str) -> PhaseFactory:
        return lambda cid, pair: complex_current_source(id=cid, nodes=pair, I=_phase_shift(I, suffix_phase[suffix]), Y=Y)

    return three_phase_custom_component_delta(id=id, nodes=nodes, phase_a=f("ab"), phase_b=f("bc"), phase_c=f("ca"))


def three_phase_impedance_load_star(id: str, nodes: tuple[str, ...], Z: complex) -> ThreePhaseComponent:
    f: PhaseFactory = lambda cid, pair: impedance(id=cid, nodes=pair, Z=Z)
    return three_phase_custom_component_star(id=id, nodes=nodes, phase_a=f, phase_b=f, phase_c=f)


def three_phase_impedance_load_delta(id: str, nodes: tuple[str, ...], Z: complex) -> ThreePhaseComponent:
    f: PhaseFactory = lambda cid, pair: impedance(id=cid, nodes=pair, Z=Z)
    return three_phase_custom_component_delta(id=id, nodes=nodes, phase_a=f, phase_b=f, phase_c=f)
