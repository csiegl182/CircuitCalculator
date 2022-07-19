from dataclasses import dataclass
from typing import Protocol, List, Dict, Callable, Any

class UnknownBranchResult(Exception): pass

class Element(Protocol):
    @property
    def Z(self) -> complex:
        """"Impedance of Branch"""
    @property
    def Y(self) -> complex:
        """"Impedance of Branch"""
    @property
    def I(self) -> complex:
        """"Impedance of Branch"""
    @property
    def U(self) -> complex:
        """"Impedance of Branch"""

@dataclass
class Impedeance:
    Z : complex
    
    @property
    def Y(self): return 1/self.Z
    @property
    def I(_): return 0
    @property
    def U(_): return None

@dataclass
class CurrentSource:
    Z : complex
    I : complex
    @property
    def Y(self): return 1/self.Z
    @property
    def U(self): return self.I*self.Z

def resistor(R : float, **_) -> Element:
    return Impedeance(Z=R)

def conductor(G : float, **_) -> Element:
    return Impedeance(Z=1/G)

def real_current_source(I : float, R : float, **_) -> Element:
    return CurrentSource(I=I, Z=R)

branch_types : Dict[str, Callable[..., Element]] = {
    "resistor" : resistor,
    "real_current_source" : real_current_source
}

@dataclass(frozen=True)
class Branch:
    node1 : int
    node2 : int
    element : Element

class Network:
    def __init__(self) -> None:
        self.branches : List[Branch] = []

    def add_branch(self, branch : Branch) -> None:
        self.branches.append(branch)
        
    def branches_connected_to_node(self, node) -> List[Branch]:
        connected_branches = [branch for branch in self.branches if branch.node1 == node or branch.node2 == node]
        connected_branches.sort(key=lambda x: x.node1 if x.node1!=node else x.node2)
        return connected_branches

    @property
    def number_of_nodes(self) -> int:
        node1_set = {branch.node1 for branch in self.branches}
        node2_set = {branch.node2 for branch in self.branches}
        node_set = node1_set.union(node2_set)
        return len(node_set)

class NetworkSolution(Protocol):
    def get_voltage(self, branch: Branch) -> float: pass

    def get_current(self, branch: Branch) -> float: pass

NetworkSolver = Callable[[Network], NetworkSolution]

def load_network(network_dict: List[Dict[str, Any]]) -> Network:
    network = Network()
    for branch in network_dict:
        n1 = branch.pop('N1')
        n2 = branch.pop('N2')
        element_factory = branch_types[branch.pop('type')]
        element = element_factory(**branch)
        network.add_branch(Branch(n1, n2, element))
    return network

def load_network_from_json(filename: str) -> Network:
    import json
    with open(filename, 'r') as json_file:
        network_dict = json.load(json_file)
    return load_network(network_dict)