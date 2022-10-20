from dataclasses import dataclass, field
from typing import Protocol, List, Dict, Callable, Any, Set
import functools
from numpy import inf, nan

class UnknownBranchResult(Exception): pass

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
    node1 : int
    node2 : int
    element : Element

@dataclass(frozen=True)
class Network:
    branch_list: List[Branch]

    @property
    def branches(self) -> List[Branch]:
        return self.branch_list

    @property
    def number_of_nodes(self) -> int:
        node1_set = {branch.node1 for branch in self.branches}
        node2_set = {branch.node2 for branch in self.branches}
        node_set = node1_set.union(node2_set)
        return max(node_set)+1

    def branches_connected_to(self, node: int) -> List[Branch]:
        connected_branches = [branch for branch in self.branches if branch.node1 == node or branch.node2 == node]
        connected_branches.sort(key=lambda x: x.node1 if x.node1!=node else x.node2)
        return connected_branches

    def nodes_connected_to(self, node: int) -> Set[int]:
        return {b.node1 if b.node1 != node else b.node2 for b in self.branches_connected_to(node=node)}

    def branches_between(self, node1: int, node2: int) -> List[Branch]:
        if node1 == node2: raise ValueError(f'Cannot determine branch between equal nodes {node1=} and {node2=}.')
        return [branch for branch in self.branches if set((branch.node1, branch.node2)) == set((node1, node2))]

def switch_network_nodes(network: Network, new_node: int, old_node: int=0) -> Network:
    def switch_node_indices(branch: Branch, i1: int, i2: int) -> Branch:
        node1, node2 = branch.node1, branch.node2
        if branch.node1 == i1: node1 = i2
        if branch.node1 == i2: node1 = i1
        if branch.node2 == i1: node2 = i2
        if branch.node2 == i2: node2 = i1
        return Branch(node1, node2, branch.element)
    return Network([switch_node_indices(b, new_node, old_node) for b in network.branches])

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
