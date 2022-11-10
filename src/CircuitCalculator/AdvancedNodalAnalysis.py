import CircuitCalculator.ClassicNodalAnalysis as cna
import numpy as np
from .Network import Network, Branch, NetworkSolution, Element
from typing import List

class AmbiguousElectricalPotential(Exception): pass

def is_ideal_voltage_source(branch: Branch) -> bool:
    return branch.element.active and branch.element.Z==0 and np.isfinite(branch.element.U)

def is_ideal_current_source(branch: Branch) -> bool:
    return branch.element.active and branch.element.Y==0 and np.isfinite(branch.element.I)

def ideal_voltage_sources(network: Network) -> List[Branch]:
    return [b for b in network.branches if is_ideal_voltage_source(b)]

def passive_elements(network: Network) -> List[Branch]:
    return [b for b in network.branches if not b.element.active]

class NodeTypes:
    def __init__(self, network: Network) -> None:
        self.voltage_sources: List[Element] = []
        self.active_nodes : List[int] = []
        self.counterparts: List[int] = []
        self.voltages: List[complex] = []
        for voltage_source in ideal_voltage_sources(network):
            node, other_node = voltage_source.node1, voltage_source.node2
            if node == 0 or node in self.active_nodes:
                node, other_node = other_node, node
            if node == 0 or node in self.active_nodes:
                raise AmbiguousElectricalPotential
            self.voltage_sources.append(voltage_source.element)
            self.active_nodes.append(node)
            self.counterparts.append(other_node)
            V = voltage_source.element.U if node == voltage_source.node1 else -voltage_source.element.U
            self.voltages.append(V)

    def is_active(self, node: int) -> bool:
        return node in self.active_nodes
    
    def is_passive(self, node: int) -> bool:
        return not self.is_active(node)

    def get_active_node(self, voltage_source: Element) -> int:
        return self.active_nodes[self.voltage_sources.index(voltage_source)]

    def get_counterpart(self, supernode: int) -> int:
        return self.counterparts[self.active_nodes.index(supernode)]

    def get_voltage(self, active_node: int) -> complex:
        return self.voltages[self.active_nodes.index(active_node)]

    def voltage_defined_between(self, node1: int, node2: int) -> bool:
        if self.is_active(node1):
            if self.get_counterpart(node1) == node2:
                return True
        if self.is_active(node2):
            if self.get_counterpart(node2) == node1:
                return True
        return False

def is_zero_node(node: int) -> bool:
    return node == 0

def create_node_matrix_from_network(network: Network) -> np.ndarray:
    def branch_parallel_to_voltage_source(branch: Branch) -> bool:
        n1, n2 = branch.node1, branch.node2
        return any([is_ideal_voltage_source(b) for b in network.branches_between(n1, n2)])
    supernodes = NodeTypes(network)
    A = np.zeros((network.number_of_nodes-1, network.number_of_nodes-1), dtype=complex)
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
        i = supernodes.get_active_node(vs.element)
        j = supernodes.get_counterpart(i)
        A[i-1, i-1] = -1 if i == vs.node1 else +1
        if not is_zero_node(j):
            A[j-1, i-1] = +1 if i == vs.node1 else -1
    return A

def create_current_vector_from_network(network: Network) -> np.ndarray:
    def full_admittance_between(node1: int, node2: int) -> complex:
        return sum(b.element.Y for b in network.branches_between(node1=node1, node2=node2) if np.isfinite(b.element.Y))
    def full_admittance_connected_to(node: int) -> complex:
        return sum(b.element.Y for b in network.branches_connected_to(node) if np.isfinite(b.element.Y))
    def voltage_to_next_passive_node(node: int) -> complex:
        V = 0+0j
        while nodes.is_active(node):
            V += nodes.get_voltage(node)
            node = nodes.get_counterpart(node)
        return V
    nodes = NodeTypes(network)
    b = np.zeros(network.number_of_nodes-1, dtype=complex)
    current_sources = [b for b in network.branches if is_ideal_current_source(b)]
    for cs in current_sources:
        if cs.node1 > 0:
            b[cs.node1-1] += -cs.element.I
        if cs.node2 > 0:
            b[cs.node2-1] += cs.element.I
    for vs in ideal_voltage_sources(network):
        sn = nodes.get_active_node(vs.element)
        b[sn-1] += -voltage_to_next_passive_node(sn)*full_admittance_connected_to(sn)
        connected_nodes = [n for n in network.nodes_connected_to(sn) if n > 0]
        for cn in connected_nodes:
            b[cn-1] += voltage_to_next_passive_node(sn)*full_admittance_between(sn, cn)
    return b

class NodalAnalysisSolution:
    def __init__(self, network : Network) -> None:
        Y = create_node_matrix_from_network(network)
        I = create_current_vector_from_network(network)
        self.solution_vector = cna.calculate_node_voltages(Y, I)
        self.nodes = NodeTypes(network)

    def _calculate_potential_of_active_node(self, node: int) -> complex:
        phi = 0+0j
        while self.nodes.is_active(node):
            phi += self.nodes.get_voltage(node)
            node = self.nodes.get_counterpart(node)
        if not is_zero_node(node):
            phi += self.solution_vector[node-1]
        return phi

    def _calculate_potential_of_node(self, node: int) -> complex:
        if is_zero_node(node):
            return 0+0j
        elif self.nodes.is_passive(node):
            return self.solution_vector[node-1]
        else:
            return self._calculate_potential_of_active_node(node)
    
    def get_voltage(self, branch: Branch) -> complex:
        phi1 = self._calculate_potential_of_node(branch.node1)
        phi2 = self._calculate_potential_of_node(branch.node2)
        return phi1-phi2

    def get_current(self, branch: Branch) -> complex:
        if is_ideal_voltage_source(branch):
            return self.solution_vector[self.nodes.get_active_node(branch.element)-1]
        elif is_ideal_current_source(branch):
            return branch.element.I
        else:
            return self.get_voltage(branch)/branch.element.Z.real

def nodal_analysis_solver(network) -> NetworkSolution:
    return NodalAnalysisSolution(network)
