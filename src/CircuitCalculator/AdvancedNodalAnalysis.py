import CircuitCalculator.ClassicNodalAnalysis as cna
import numpy as np
from .Network import Network, Branch, NetworkSolution, Element
from typing import Dict, List

class AmbiguousElectricalPotential(Exception): pass

def is_ideal_voltage_source(branch: Branch) -> bool:
    return branch.element.active and branch.element.Z==0 and np.isfinite(branch.element.U)

def is_ideal_current_source(branch: Branch) -> bool:
    return branch.element.active and branch.element.Y==0 and np.isfinite(branch.element.I)

def ideal_voltage_sources(network: Network) -> List[Branch]:
    return [b for b in network.branches if is_ideal_voltage_source(b)]

def passive_elements(network: Network) -> List[Branch]:
    return [b for b in network.branches if not b.element.active]

def remove_ideal_voltage_sources(network: Network) -> Network:
    return Network([b for b in network.branches if not is_ideal_voltage_source(b)])

class Supernodes:
    def __init__(self, network: Network) -> None:
        self.voltage_sources: List[Element] = []
        self.supernodes : List[int] = []
        self.counterparts: List[int] = []
        for voltage_source in ideal_voltage_sources(network):
            node = voltage_source.node1
            other_node = voltage_source.node2
            if node == 0 or node in self.supernodes:
                node = voltage_source.node2
                other_node = voltage_source.node1
            if node == 0 or node in self.supernodes:
                raise AmbiguousElectricalPotential
            self.voltage_sources.append(voltage_source.element)
            self.supernodes.append(node)
            self.counterparts.append(other_node)

    def is_supernode(self, node: int) -> bool:
        return node in self.supernodes

    def is_active(self, node: int) -> bool:
        return node in self.supernodes
    
    def is_passive(self, node: int) -> bool:
        return not self.is_supernode(node)

    def is_counterpart(self, node: int) -> bool:
        return node in self.counterparts

    def get_supernode(self, voltage_source: Element) -> int:
        return self.supernodes[self.voltage_sources.index(voltage_source)]

    def get_counterpart(self, supernode: int) -> int:
        return self.counterparts[self.supernodes.index(supernode)]
        
def get_supernodes(network: Network) -> Dict[int, Branch]:
    supernodes : Dict[int, Branch] = {}
    for vs in ideal_voltage_sources(network):
        node = vs.node1
        if node == 0 or node in supernodes.keys():
            node = vs.node2
        if node == 0 or node in supernodes.keys():
            raise AmbiguousElectricalPotential
        supernodes.update({node: vs})
    return supernodes

def get_supernode_counterparts(network: Network) -> Dict[int, Branch]:
    counterparts = {}
    for sn, b in get_supernodes(network).items():
        if b.node1 == sn and b.node2 not in get_supernodes(network).keys():
            counterparts.update({b.node2: b})
        if b.node2 == sn and b.node1 not in get_supernodes(network).keys():
            counterparts.update({b.node1: b})
    counterparts.pop(0, None)
    return counterparts

def get_non_supernodes(network: Network) -> List[int]:
    return list(set(range(1, network.number_of_nodes)).difference(get_supernodes(network).keys()))

def is_zero_node(node: int) -> bool:
    return node == 0

def create_node_matrix_from_network(network: Network) -> np.ndarray:
    def branch_parallel_to_voltage_source(branch: Branch) -> bool:
        n1, n2 = branch.node1, branch.node2
        return any([is_ideal_voltage_source(b) for b in network.branches_between(n1, n2)])
    supernodes = Supernodes(network)
    A = np.zeros((network.number_of_nodes-1, network.number_of_nodes-1))
    passive_non_parallel_elements = [b for b in passive_elements(network) if not branch_parallel_to_voltage_source(b)]
    for b in passive_non_parallel_elements:
        i, j = b.node1, b.node2
        if is_zero_node(i) or supernodes.is_active(j):
            i, j = j, i
        if supernodes.is_passive(i):
            A[i-1,i-1] += b.element.Y
        if not is_zero_node(j):
            A[j-1,j-1] += b.element.Y
            if supernodes.is_active(i):
                k = supernodes.get_counterpart(i)
                if not is_zero_node(k) and supernodes.is_passive(k):
                    A[i-1, k-1] += b.element.Y
                    A[j-1, k-1] -= b.element.Y
            else:
                A[j-1, i-1] -= b.element.Y
            if supernodes.is_active(j):
                k = supernodes.get_counterpart(j)
                if not is_zero_node(k) and supernodes.is_passive(k):
                    A[j-1, k-1] += b.element.Y
                    A[i-1, k-1] -= b.element.Y
            else:
                A[i-1, j-1] -= b.element.Y
    for vs in ideal_voltage_sources(network):
        i = supernodes.get_supernode(vs.element)
        j = supernodes.get_counterpart(i)
        A[i-1, i-1] = -1 if i == vs.node1 else +1
        if not is_zero_node(j):
            A[j-1, i-1] = +1 if i == vs.node1 else -1
    return A

def create_node_matrix_from_network3(network: Network) -> np.ndarray:
    def fill_supernode_part(Y: np.ndarray) -> np.ndarray:
        for super_node, b in get_supernodes(network).items():
            sign = np.sign(b.element.U)
            opposite_node = b.node1
            if super_node == b.node1: # voltage arrow points out of super node
                sign *= -1
                opposite_node = b.node2
            Y[super_node-1, super_node-1] = sign
            if opposite_node > 0:
                Y[opposite_node-1, super_node-1] = -sign
        return Y
    def fill_non_supernode_part(Y: np.ndarray) -> np.ndarray:
        def branch_parallel_to_voltage_source(branch: Branch) -> bool:
            n1, n2 = branch.node1, branch.node2
            return any([is_ideal_voltage_source(b) for b in network.branches_between(n1, n2)])
        def is_supernode(node: int) -> bool:
            return node in get_supernodes(network).keys()
        def get_supernode_counterpart(supernode: int) -> int:
            sn = get_supernodes(network)[supernode]
            if supernode == sn.node1:
                return sn.node2
            else:
                return sn.node2
        valid_branches = [b for b in network.branches if not is_ideal_voltage_source(b) and not branch_parallel_to_voltage_source(b)]
        for b in valid_branches:
            i1, i2 = b.node1-1, b.node2-1
            if b.node1 > 0:
                Y[i1, i1] += b.element.Y
            if b.node2 > 0:
                Y[i2, i2] += b.element.Y
            if b.node1 > 0 and b.node2 > 0:
                if not is_supernode(b.node2):
                    Y[i1, i2] += -b.element.Y
                else:
                    cp = get_supernode_counterpart(b.node2)
                    if cp > 0 and not is_supernode(cp):
                        Y[i2, cp-1] += b.element.Y
                        Y[i1, cp-1] += -b.element.Y
                if not is_supernode(b.node1):
                    Y[i2, i1] += -b.element.Y
                else:
                    cp = get_supernode_counterpart(b.node1)
                    if cp > 0 and not is_supernode(cp):
                        Y[i1, cp-1] += b.element.Y
                        Y[i2, cp-1] += -b.element.Y
        return Y
    Y = np.zeros((network.number_of_nodes-1, network.number_of_nodes-1))
    Y = fill_non_supernode_part(Y)
    Y = fill_supernode_part(Y)
    return Y

def signed_voltage(branch: Branch, node: int) -> complex:
    if branch.node1 == node:
        return -branch.element.U
    else:
        return +branch.element.U

def create_current_vector_from_network2(network: Network) -> np.ndarray:
    def full_admittance_between(node1: int, node2: int) -> complex:
        return sum(b.element.Y for b in network.branches_between(node1=node1, node2=node2) if np.isfinite(b.element.Y))
    def full_admittance_connected_to(node: int) -> complex:
        return sum(b.element.Y for b in network.branches_connected_to(node) if np.isfinite(b.element.Y))
    network2 = remove_ideal_voltage_sources(network)
    I = np.zeros(network2.number_of_nodes-1)
    for i in range(1, network2.number_of_nodes):
        current_sources = [branch for branch in network2.branches_connected_to(node=i) if branch.element.active]
        if len(current_sources) > 0:
            I[i-1] = sum([cs.element.I if cs.node2 == i else -cs.element.I for cs in current_sources])
        else:
            I[i-1] = 0

    voltage_sources = ideal_voltage_sources(network)
    if len(voltage_sources.branches) == 0:
        return I
    for sn, vs in get_supernodes(network).items():
        I[sn-1] += full_admittance_connected_to(sn)*signed_voltage(vs, sn)
    for node in range(1,network.number_of_nodes):
        for connected_supernode in network.nodes_connected_to(node).intersection(get_supernodes(network)):
            I[node-1] += full_admittance_between(node, connected_supernode)*-signed_voltage(get_supernodes(network)[connected_supernode], connected_supernode)
    return I

def create_current_vector_from_network(network: Network) -> np.ndarray:
    def full_admittance_between(node1: int, node2: int) -> complex:
        return sum(b.element.Y for b in network.branches_between(node1=node1, node2=node2) if np.isfinite(b.element.Y))
    def full_admittance_connected_to(node: int) -> complex:
        return sum(b.element.Y for b in network.branches_connected_to(node) if np.isfinite(b.element.Y))
    def is_supernode(node: int) -> bool:
        return node in get_supernodes(network).keys()
    def get_supernode_counterpart(supernode: int) -> int:
        sn = get_supernodes(network)[supernode]
        if supernode == sn.node1:
            return sn.node2
        else:
            return sn.node1
    def voltage_to_next_passive_node(node: int) -> complex:
        V = 0+0j
        while is_supernode(node):
            V += get_supernodes(network)[node].element.U
            node = get_supernode_counterpart(node)
        return V
    I = np.zeros(network.number_of_nodes-1)
    current_sources = [b for b in network.branches if is_ideal_current_source(b)]
    for cs in current_sources:
        if cs.node1 > 0:
            I[cs.node1-1] += -cs.element.I
        if cs.node2 > 0:
            I[cs.node2-1] += cs.element.I
    for sn, vs in get_supernodes(network).items():
        sign_phi = +1
        if sn == vs.node2:
            sign_phi = -1
        I[sn-1] += -sign_phi*voltage_to_next_passive_node(sn)*full_admittance_connected_to(sn)
        for connected_node in network.nodes_connected_to(sn):
            if connected_node > 0:
                I[connected_node-1] += sign_phi*voltage_to_next_passive_node(sn)*full_admittance_between(sn, connected_node)
    return I

class NodalAnalysisSolution:
    def __init__(self, network : Network) -> None:
        Y = create_node_matrix_from_network(network)
        I = create_current_vector_from_network(network)
        self.solution_vector = cna.calculate_node_voltages(Y, I)
        self.super_nodes = get_supernodes(network)
        self.node_potentials = np.copy(self.solution_vector)
        for i, b in self.super_nodes.items():
            if i == b.node1:
                if b.node2 == 0:
                    self.node_potentials[i-1] = b.element.U
                else:
                    self.node_potentials[i-1] = b.element.U + self.node_potentials[b.node2-1]
            else:
                if b.node1 == 0:
                    self.node_potentials[i-1] = -b.element.U
                else:
                    self.node_potentials[i-1] = -b.element.U + self.node_potentials[b.node1-1]
    
    def get_voltage(self, branch: Branch) -> complex:
        return cna.calculate_branch_voltage(self.node_potentials, branch.node1, branch.node2)

    def get_current(self, branch: Branch) -> complex:
        if is_ideal_voltage_source(branch):
            sn = list(self.super_nodes.keys())[list(self.super_nodes.values()).index(branch)]
            return self.solution_vector[sn-1]
        elif is_ideal_current_source(branch):
            return branch.element.I
        else:
            return self.get_voltage(branch)/branch.element.Z.real

def nodal_analysis_solver(network) -> NetworkSolution:
    return NodalAnalysisSolution(network)
