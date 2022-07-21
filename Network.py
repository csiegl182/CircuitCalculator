from dataclasses import dataclass, field
from typing import Protocol, List, Dict, Callable, Any
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
    def Y(self) -> complex: return 1/self.Z

@dataclass(frozen=True)
class RealCurrentSource:
    Z : complex
    I : complex
    active: bool = field(default=True, init=False)
    @property
    def Y(self) -> complex: return 1/self.Z
    @property
    def U(self) -> complex: return self.I*self.Z

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
    def Y(self) -> complex: return 1/self.Z
    @property
    def I(self) -> complex: return self.U/self.Z

def resistor(R : float, **_) -> Element:
    return Impedeance(Z=R)

def conductor(G : float, **_) -> Element:
    return Impedeance(Z=1/G)

def real_current_source(I : float, R : float, **_) -> Element:
    return RealCurrentSource(I=I, Z=R)

def current_source(I : float, **_) -> Element:
    return CurrentSource(I=I)

def real_voltage_source(U : float, R : float, **_) -> Element:
    return RealVoltageSource(U=U, Z=R)

branch_types : Dict[str, Callable[..., Element]] = {
    "resistor" : resistor,
    "real_current_source" : real_current_source,
    "current_source" : current_source,
    "real_voltage_source" : real_voltage_source,
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
        return len(node_set)

    def branches_connected_to(self, node: int) -> List[Branch]:
        connected_branches = [branch for branch in self.branches if branch.node1 == node or branch.node2 == node]
        connected_branches.sort(key=lambda x: x.node1 if x.node1!=node else x.node2)
        return connected_branches

    def branches_between(self, node1: int, node2: int) -> List[Branch]:
        return [branch for branch in self.branches if branch.node1 == node1 and branch.node2 == node2]

class NetworkReducedParallel(Network):
    @property
    def branches(self) -> List[Branch]:
        reduced_branch_list = self.branch_list
        for branch in self.branch_list:
            if branch in reduced_branch_list:
                parallel_branches = [b for b in reduced_branch_list if b.node1 == branch.node1 and b.node2 == branch.node2]
                reduced_branch_list = [b for b in reduced_branch_list if b not in parallel_branches]
                reduced_branch = functools.reduce(lambda b1, b2 :  self._reduce_parallel(b1, b2), parallel_branches)
                reduced_branch_list.append(reduced_branch)
        return reduced_branch_list

    def _reduce_parallel(_, branch1: Branch, branch2: Branch) -> Branch:
        if type(branch1.element) == RealCurrentSource or type(branch2.element) == RealCurrentSource:
            if type(branch1.element) == RealCurrentSource:
                I = branch1.element.I
            else:
                I= branch2.element.I
            return Branch(branch1.node1, branch1.node2, real_current_source(I=I.real, R=1/(1/branch1.element.Z.real + 1/branch2.element.Z.real)))
        else:
            return Branch(branch1.node1, branch1.node2, resistor(R=1/(1/branch1.element.Z.real + 1/branch2.element.Z.real)))

class NetworkSolution(Protocol):
    def get_voltage(self, branch: Branch) -> float: pass

    def get_current(self, branch: Branch) -> float: pass

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
