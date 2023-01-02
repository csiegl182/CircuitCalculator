from . import elements as elm
from dataclasses import dataclass
from typing import Callable, Protocol
import numpy as np

class UnknownBranchResult(Exception): pass

class FloatingGroundNode(Exception): pass

class AmbiguousElectricalPotential(Exception): pass

@dataclass(frozen=True)
class Branch:
    node1 : str
    node2 : str
    element : elm.Element

@dataclass(frozen=True)
class Network:
    branches: list[Branch]
    zero_node_label: str = '0'

    def __post_init__(self):
        if self.zero_node_label not in self.node_labels:
            raise FloatingGroundNode

    @property
    def node_labels(self) -> list[str]:
        node1_set = {branch.node1 for branch in self.branches}
        node2_set = {branch.node2 for branch in self.branches}
        return sorted(list(node1_set.union(node2_set)))

    @property
    def number_of_nodes(self) -> int:
        return len(self.node_labels)

    def is_zero_node(self, node: str) -> bool:
        return node == self.zero_node_label

    def branches_connected_to(self, node: str) -> list[Branch]:
        connected_branches = [branch for branch in self.branches if branch.node1 == node or branch.node2 == node]
        connected_branches.sort(key=lambda x: x.node1 if x.node1!=node else x.node2)
        return connected_branches

    def nodes_connected_to(self, node: str) -> set[str]:
        return {b.node1 if b.node1 != node else b.node2 for b in self.branches_connected_to(node=node)}

    def branches_between(self, node1: str, node2: str) -> list[Branch]:
        return [branch for branch in self.branches if set((branch.node1, branch.node2)) == set((node1, node2))]

def node_index_mapping(network: Network) -> dict[str, int]: # deprecated?
    node_mapping = {network.zero_node_label: 0}
    next_node_index = 1
    for b in network.branches:
        if b.node1 not in node_mapping.keys():
            node_mapping.update({b.node1 : next_node_index})
            next_node_index += 1
        if b.node2 not in node_mapping.keys():
            node_mapping.update({b.node2 : next_node_index})
            next_node_index += 1
    return node_mapping

def ideal_voltage_sources(network: Network) -> list[Branch]:
    return [b for b in network.branches if elm.is_ideal_voltage_source(b.element)]

def ideal_current_sources(network: Network) -> list[Branch]:
    return [b for b in network.branches if elm.is_ideal_current_source(b.element)]

def passive_elements(network: Network) -> list[Branch]:
    return [b for b in network.branches if not b.element.active]

@dataclass(frozen=True)
class SuperNode:
    reference_node: str
    active_node: str
    voltage: complex
    voltage_source: elm.Element

class SuperNodes:
    def __init__(self, network: Network) -> None:
        self._super_nodes : list[SuperNode] = []
        self.voltage_sources: list[elm.Element] = []
        for voltage_source in ideal_voltage_sources(network):
            node, other_node = voltage_source.node1, voltage_source.node2
            if network.is_zero_node(node) or node in self.active_nodes:
                node, other_node = other_node, node
            if network.is_zero_node(node) or node in self.active_nodes:
                raise AmbiguousElectricalPotential
            self.voltage_sources.append(voltage_source.element)
            self._super_nodes.append(
                SuperNode(
                    reference_node=other_node,
                    active_node=node,
                    voltage=voltage_source.element.U if node == voltage_source.node1 else -voltage_source.element.U,
                    voltage_source=voltage_source.element
                )
            )

    @property
    def active_nodes(self) -> list[str]:
        return [sn.active_node for sn in self._super_nodes]

    @property
    def reference_nodes(self) -> list[str]:
        return [sn.reference_node for sn in self._super_nodes]

    @property
    def voltages(self) -> list[complex]:
        return [sn.voltage for sn in self._super_nodes]

    def is_active(self, node: str) -> bool:
        return node in self.active_nodes
    
    def is_reference(self, node: str) -> bool:
        return node in self.reference_nodes

    def belong_to_same(self, active_node: str, reference_node: str) -> bool:
        if self.is_active(active_node):
            if self.is_reference(reference_node):
                return self.get_reference_node(active_node) == reference_node
        return False

    def get_active_node(self, reference_node: str) -> str:
        return self.active_nodes[self.reference_nodes.index(reference_node)]

    def get_reference_node(self, active_node: str) -> str:
        return self.reference_nodes[self.active_nodes.index(active_node)]

    def get_voltage(self, active_node: str) -> complex:
        return self.voltages[self.active_nodes.index(active_node)]

    def sign(self, active_node: str) -> int:
        return np.sign(self.voltages[self.active_nodes.index(active_node)])

    def voltage_to_next_reference(self, active_node: str) -> complex:
        V = 0+0j
        while self.is_active(active_node):
            V += self.voltages[self.active_nodes.index(active_node)]
            active_node = self.get_reference_node(active_node)
        return V

    def next_reference(self, active_node: str) -> str:
        while self.is_active(active_node):
            active_node = self.get_reference_node(active_node)
        return active_node

class NetworkSolution(Protocol):
    def get_voltage(self, branch: Branch) -> complex: pass

    def get_current(self, branch: Branch) -> complex: pass

NetworkSolver = Callable[[Network], NetworkSolution]