import numpy as np
import CircuitCalculator.ClassicNodalAnalysis as cna
from .Network import Branch, Element, Network, node_index_mapping, NetworkSolution

class AmbiguousElectricalPotential(Exception): pass

def is_ideal_voltage_source(branch: Branch) -> bool:
    return branch.element.active and branch.element.Z==0 and np.isfinite(branch.element.U)

def is_ideal_current_source(branch: Branch) -> bool:
    return branch.element.active and branch.element.Y==0 and np.isfinite(branch.element.I)

def ideal_voltage_sources(network: Network) -> list[Branch]:
    return [b for b in network.branches if is_ideal_voltage_source(b)]

def passive_elements(network: Network) -> list[Branch]:
    return [b for b in network.branches if not b.element.active]

class NodeTypes:
    def __init__(self, network: Network) -> None:
        self.voltage_sources: list[Element] = []
        self.active_nodes : list[str] = []
        self.counterparts: list[str] = []
        self.voltages: list[complex] = []
        for voltage_source in ideal_voltage_sources(network):
            node, other_node = voltage_source.node1, voltage_source.node2
            if network.is_zero_node(node) or node in self.active_nodes:
                node, other_node = other_node, node
            if network.is_zero_node(node) or node in self.active_nodes:
                raise AmbiguousElectricalPotential
            self.voltage_sources.append(voltage_source.element)
            self.active_nodes.append(node)
            self.counterparts.append(other_node)
            V = voltage_source.element.U if node == voltage_source.node1 else -voltage_source.element.U
            self.voltages.append(V)

    def is_active(self, node: str) -> bool:
        return node in self.active_nodes
    
    def is_passive(self, node: str) -> bool:
        return not self.is_active(node)

    def get_active_node(self, voltage_source: Element) -> str:
        return self.active_nodes[self.voltage_sources.index(voltage_source)]

    def get_active_node_and_counterpart(self, voltage_source: Element) -> tuple[str, str]:
        active_node = self.active_nodes[self.voltage_sources.index(voltage_source)]
        counterpart = self.counterparts[self.active_nodes.index(active_node)]
        return (active_node, counterpart)

    def get_counterpart(self, active_node: str) -> str:
        return self.counterparts[self.active_nodes.index(active_node)]

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
            
def create_node_matrix_from_network(network: Network) -> np.ndarray:
    def branch_parallel_to_voltage_source(branch: Branch) -> bool:
        n1, n2 = branch.node1, branch.node2
        return any([is_ideal_voltage_source(b) for b in network.branches_between(n1, n2)])
    node_type = NodeTypes(network)
    node_mapping = node_index_mapping(network)
    A = np.zeros((network.number_of_nodes-1, network.number_of_nodes-1), dtype=complex)
    passive_non_parallel_elements = [b for b in passive_elements(network) if not branch_parallel_to_voltage_source(b)]
    for b in passive_non_parallel_elements:
        n1, n2 = b.node1, b.node2
        i1, i2 = map(lambda n: node_mapping[n], (n1, n2))
        if network.is_zero_node(n1) or node_type.is_active(n2):
            n1, n2 = n2, n1
            i1, i2 = i2, i1
        if node_type.is_passive(n1):
            A[i1-1,i1-1] += b.element.Y
        if not network.is_zero_node(n2):
            A[i2-1,i2-1] += b.element.Y
        if node_type.is_active(n1):
            cp = node_type.get_counterpart(n1)
            if not network.is_zero_node(cp) and node_type.is_passive(cp):
                A[i1-1, node_mapping[cp]-1] += b.element.Y
                if not network.is_zero_node(n2):
                    A[i2-1, node_mapping[cp]-1] -= b.element.Y
        else:
            if not network.is_zero_node(n2):
                A[i2-1, i1-1] -= b.element.Y
        if node_type.is_active(n2):
            cp = node_type.get_counterpart(n2)
            if not network.is_zero_node(cp) and node_type.is_passive(cp):
                A[i2-1, node_mapping[cp]-1] += b.element.Y
                A[i1-1, node_mapping[cp]-1] -= b.element.Y
        else:
            if not network.is_zero_node(n2):
                A[i1-1, i2-1] -= b.element.Y
    for vs in ideal_voltage_sources(network):
        n1, n2 = node_type.get_active_node_and_counterpart(vs.element)
        i1, i2 = map(lambda n: node_mapping[n], (n1, n2))
        A[i1-1, i1-1] = -1 if n1 == vs.node1 else +1
        if not network.is_zero_node(n2):
            A[i2-1, i1-1] = +1 if n1 == vs.node1 else -1
    return A

def create_current_vector_from_network(network: Network) -> np.ndarray:
    def full_admittance_between(node1: str, node2: str) -> complex:
        return sum(b.element.Y for b in network.branches_between(node1=node1, node2=node2) if np.isfinite(b.element.Y))
    def full_admittance_connected_to(node: str) -> complex:
        return sum(b.element.Y for b in network.branches_connected_to(node) if np.isfinite(b.element.Y))
    def voltage_to_next_passive_node(node: str) -> complex:
        V = 0+0j
        while node_type.is_active(node):
            V += node_type.get_voltage(node)
            node = node_type.get_counterpart(node)
        return V
    node_type = NodeTypes(network)
    node_mapping = node_index_mapping(network)
    b = np.zeros(network.number_of_nodes-1, dtype=complex)
    current_sources = [b for b in network.branches if is_ideal_current_source(b)]
    for cs in current_sources:
        i1, i2 = node_mapping[cs.node1], node_mapping[cs.node2]
        if i1 > 0:
            b[i1-1] += -cs.element.I
        if i2 > 0:
            b[i2-1] += cs.element.I
    for vs in ideal_voltage_sources(network):
        sn = node_type.get_active_node(vs.element)
        b[node_mapping[sn]-1] += -voltage_to_next_passive_node(sn)*full_admittance_connected_to(sn)
        connected_nodes = [n for n in network.nodes_connected_to(sn) if not network.is_zero_node(n)]
        for cn in connected_nodes:
            b[node_mapping[cn]-1] += voltage_to_next_passive_node(sn)*full_admittance_between(sn, cn)
    return b

class NodalAnalysisSolution:
    def __init__(self, network : Network) -> None:
        Y = create_node_matrix_from_network(network)
        I = create_current_vector_from_network(network)
        self._network = network
        self._solution_vector = cna.calculate_node_voltages(Y, I)
        self._node_type = NodeTypes(network)
        self._node_mapping = node_index_mapping(network)

    def _calculate_potential_of_active_node(self, node: str) -> complex:
        phi = 0+0j
        while self._node_type.is_active(node):
            phi += self._node_type.get_voltage(node)
            node = self._node_type.get_counterpart(node)
        if not self._network.is_zero_node(node):
            phi += self._solution_vector[self._node_mapping[node]-1]
        return phi

    def _calculate_potential_of_node(self, node: str) -> complex:
        if self._network.is_zero_node(node):
            return 0+0j
        elif self._node_type.is_passive(node):
            return self._solution_vector[self._node_mapping[node]-1]
        else:
            return self._calculate_potential_of_active_node(node)
    
    def get_voltage(self, branch: Branch) -> complex:
        phi1 = self._calculate_potential_of_node(branch.node1)
        phi2 = self._calculate_potential_of_node(branch.node2)
        return phi1-phi2

    def get_current(self, branch: Branch) -> complex:
        if is_ideal_voltage_source(branch):
            return self._solution_vector[self._node_mapping[self._node_type.get_active_node(branch.element)]-1]
        elif is_ideal_current_source(branch):
            return branch.element.I
        else:
            return self.get_voltage(branch)/branch.element.Z.real

def nodal_analysis_solver(network) -> NetworkSolution:
    return NodalAnalysisSolution(network)
