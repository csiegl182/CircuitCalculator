from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Protocol, Set
import numpy as np

class UnknownBranchResult(Exception): pass

class FloatingGroundNode(Exception): pass

class AmbiguousElectricalPotential(Exception): pass

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

branch_types : Dict[str, Callable[..., Element]] = {
    "resistor" : resistor,
    "real_current_source" : real_current_source,
    "current_source" : current_source,
    "real_voltage_source" : real_voltage_source,
    "voltage_source" : voltage_source,
}

@dataclass(frozen=True)
class Branch:
    node1 : str
    node2 : str
    element : Element

@dataclass(frozen=True)
class Network:
    branches: List[Branch]
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

    def node_label(self, node_index: int) -> str: # deprecated?
        if node_index == 0:
            return self.zero_node_label
        labels = self.node_labels
        labels.remove(self.zero_node_label)
        return labels[node_index-1]
    
    def node_index(self, node_label: str) -> int: # deprecated?
        if node_label == self.zero_node_label:
            return 0
        labels = self.node_labels
        labels.remove(self.zero_node_label)
        return labels.index(node_label)+1

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

def is_ideal_voltage_source(element: Element) -> bool:
    return element.active and element.Z==0 and np.isfinite(element.U)

def is_ideal_current_source(element: Element) -> bool:
    return element.active and element.Y==0 and np.isfinite(element.I)

def ideal_voltage_sources(network: Network) -> list[Branch]:
    return [b for b in network.branches if is_ideal_voltage_source(b.element)]

def ideal_current_sources(network: Network) -> list[Branch]:
    return [b for b in network.branches if is_ideal_current_source(b.element)]

def passive_elements(network: Network) -> list[Branch]:
    return [b for b in network.branches if not b.element.active]

def switch_ground_node(network: Network, new_ground: str) -> Network:
    return Network(network.branches, new_ground)

def remove_ideal_current_sources(network: Network, keep: list[Element] = []) -> Network:
    return Network([b for b in network.branches if not is_ideal_current_source(b.element) or b.element in keep], zero_node_label=network.zero_node_label)

def remove_ideal_voltage_sources(network: Network, keep: list[Element] = []) -> Network:
    branches = network.branches
    super_nodes = SuperNodes(network)
    voltage_sources = [b.element for b in network.branches if is_ideal_voltage_source(b.element)]
    voltage_sources = [vs for vs in voltage_sources if vs not in keep]
    short_circuit_nodes = [super_nodes.get_active_node_and_counterpart(vs) for vs in voltage_sources]
    for an, rn in short_circuit_nodes:
        branches = [Branch(rn, b.node2, b.element) if b.node1 == an else b for b in branches]
        branches = [Branch(b.node1, rn, b.element) if b.node2 == an else b for b in branches]
        branches = [b for b in branches if b.node1 != b.node2]
    return Network(branches, zero_node_label=network.zero_node_label)

def passive_network(network: Network, keep: list[Element] = []) -> Network:
    return remove_ideal_voltage_sources(remove_ideal_current_sources(network, keep=keep), keep=keep)

@dataclass(frozen=True)
class SuperNode:
    reference_node: str
    active_node: str
    voltage: complex
    voltage_source: Element

class SuperNodes:
    def __init__(self, network: Network) -> None:
        self._super_nodes : list[SuperNode] = []
        self.voltage_sources: list[Element] = []
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

    def is_super_node(self, node: str) -> bool:
        return self.is_active(node) or self.is_reference(node)

    def belong_to_same(self, active_node: str, reference_node: str) -> bool:
        if self.is_active(active_node):
            if self.is_reference(reference_node):
                return self.get_counterpart(active_node) == reference_node
        return False

    def get_active_node(self, voltage_source: Element) -> str:
        return self.active_nodes[self.voltage_sources.index(voltage_source)]

    def get_active_node_and_counterpart(self, voltage_source: Element) -> tuple[str, str]:
        active_node = self.active_nodes[self.voltage_sources.index(voltage_source)]
        counterpart = self.reference_nodes[self.active_nodes.index(active_node)]
        return (active_node, counterpart)

    def get_counterpart(self, active_node: str) -> str:
        return self.reference_nodes[self.active_nodes.index(active_node)]

    def get_active_node2(self, reference_node: str) ->str:
        return self.active_nodes[self.reference_nodes.index(reference_node)]

    def get_voltage(self, active_node: str) -> complex:
        return self.voltages[self.active_nodes.index(active_node)]

    def voltage_source_between(self, node1: str, node2: str) -> bool:
        if self.is_active(node1):
            if self.get_counterpart(node1) == node2:
                return True
        if self.is_active(node2):
            if self.get_counterpart(node2) == node1:
                return True
        return False

    def get_voltage_source(self, active_node: str) -> Element:
        return self._super_nodes[self.active_nodes.index(active_node)].voltage_source

class NetworkSolution(Protocol):
    def get_voltage(self, branch: Branch) -> complex: pass

    def get_current(self, branch: Branch) -> complex: pass

NetworkSolver = Callable[[Network], NetworkSolution]

def load_network(network_dict: List[Dict[str, Any]]) -> Network:
    branches = []
    for branch in network_dict:
        n1 = branch.pop('N1')
        n2 = branch.pop('N2')
        element_factory = branch_types[branch.pop('type')]
        element = element_factory(**branch)
        branches.append(Branch(n1, n2, element))
    return Network(branches)

def load_network_from_json(filename: str) -> Network:
    import json
    with open(filename, 'r') as json_file:
        network_dict = json.load(json_file)
    return load_network(network_dict)
