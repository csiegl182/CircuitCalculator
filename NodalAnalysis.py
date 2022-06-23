from dataclasses import dataclass
from typing import Protocol, List
import numpy as np

class DimensionError(Exception): pass

def calculate_node_voltages(Y : np.ndarray, I : np.ndarray) -> np.ndarray:
    if Y.ndim != 2:
        raise DimensionError('dim error')
    if I.ndim != 1:
        raise DimensionError('dim error')
    m, n = Y.shape
    if n != m:
        raise DimensionError('dim error')
    return np.linalg.solve(Y, I)

def create_node_admittance_matrix(zero_node_admittances, *node_admittances) ->  np.ndarray:
    if [len(y_vec) for y_vec in node_admittances] != list(range(1, len(zero_node_admittances)))[::-1]:
        raise DimensionError('dim error')
        
    Y = np.diag(zero_node_admittances)
    for n, admittances in enumerate(node_admittances):
        Y[n,n] += np.sum(admittances)
        for m, y in enumerate(admittances):
            Y[n+m+1,n+m+1] += y
            Y[n+m+1, n] = -y
    Y += np.tril(Y,-1).T

    return Y


def calculate_branch_voltage(V_node : np.ndarray, node1 : int, node2 : int) -> float:
    if node1 < 0 or node2 < 0:
        raise DimensionError('dim error')
    try:
        V1 = 0 if node1 == 0 else V_node[node1-1]
        V2 = 0 if node2 == 0 else V_node[node2-1]
    except IndexError:
        raise DimensionError('dim error')
    return V1 - V2

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
class Branch:
    node1 : int
    node2 : int
    element : Element

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

def resistor(R : float) -> Element:
    return Impedeance(Z=R)

def conductor(G : float) -> Element:
    return Impedeance(Z=1/G)

def real_current_source(I : float, R : float) -> Element:
    return CurrentSource(I=I, Z=R)

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

def create_node_admittance_matrix_from_network(network : Network) -> np.ndarray:
    zero_node_admittances = [1/branch.element.Z for branch in network.branches_connected_to_node(0)]
    node_admittances = []
    for i in range(1, network.number_of_nodes-1):
        node_admittances += [[1/branch.element.Z for branch in network.branches_connected_to_node(i) if branch.node1 > i or branch.node2 > i]]
    return create_node_admittance_matrix(zero_node_admittances, *node_admittances)
    
def create_current_vector_from_network(network : Network) -> np.ndarray:
    I = np.zeros(network.number_of_nodes-1)
    for i in range(1, network.number_of_nodes):
        current_sources = [branch for branch in network.branches_connected_to_node(i) if type(branch.element) == CurrentSource]
        if len(current_sources) > 0:
            I[i-1] = sum([cs.element.I if cs.node1 == i else -cs.element.I for cs in current_sources])
        else:
            I[i-1] = 0

    return I