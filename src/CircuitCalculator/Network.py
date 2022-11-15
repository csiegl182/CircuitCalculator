from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Protocol, Set

from numpy import inf, nan


class UnknownBranchResult(Exception): pass

class FloatingGroundNode(Exception): pass

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
    I : complex = field(default=nan, init=False)
    U : complex = field(default=nan, init=False)
    active: bool = field(default=False, init=False)
    @property
    def Y(self) -> complex:
        try:
            return 1/self.Z
        except ZeroDivisionError:
            return inf

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
            return inf
    @property
    def U(self) -> complex:
        try:
            return self.I/self.Y
        except ZeroDivisionError:
            return nan

@dataclass(frozen=True)
class CurrentSource:
    Z : complex = field(default=inf, init=False)
    Y : complex = field(default=0, init=False)
    I : complex
    U : complex = field(default=nan, init=False)
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
            return inf
    @property
    def I(self) -> complex:
        try:
            return self.U/self.Z
        except ZeroDivisionError:
            return nan

@dataclass(frozen=True)
class VoltageSource:
    Z : complex = field(default=0, init=False)
    Y : complex = field(default=inf, init=False)
    U : complex
    I : complex = field(default=nan, init=False)
    active: bool = field(default=True, init=False)

def resistor(R : float, **_) -> Element:
    return Impedeance(Z=R)

def conductor(G : float, **_) -> Element:
    try:
        return Impedeance(Z=1/G)
    except ZeroDivisionError:
        return Impedeance(Z=inf)

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
    def node_labels(self) -> set[str]:
        node1_set = {branch.node1 for branch in self.branches}
        node2_set = {branch.node2 for branch in self.branches}
        return node1_set.union(node2_set)

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
        if node1 == node2: raise ValueError(f'Cannot determine branch between equal nodes {node1=} and {node2=}.')
        return [branch for branch in self.branches if set((branch.node1, branch.node2)) == set((node1, node2))]

def node_index_mapping(network: Network) -> dict[str, int]:
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

def switch_ground_node(network: Network, new_ground: str) -> Network:
    return Network(network.branches, new_ground)

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
