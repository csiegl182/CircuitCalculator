import numpy as np
import CircuitCalculator.ClassicNodalAnalysis as cna
from .Network import Branch, Network, SuperNodes, NetworkSolution, is_ideal_current_source, is_ideal_voltage_source, passive_network
from typing import Callable
import itertools

def admittance_connected_to(network: Network, node: str) -> complex:
    return sum(b.element.Y for b in network.branches_connected_to(node) if np.isfinite(b.element.Y))

def admittance_between(network: Network, node1: str, node2: str) -> complex:
    return sum([b.element.Y for b in network.branches_between(node1, node2) if np.isfinite(b.element.Y)])

NodeIndexMapper = Callable[[Network], dict[str, int]]

def alphabetic_mapper(network: Network) -> dict[str, int]:
    node_labels_without_zero = [label for label in sorted(network.node_labels) if label != network.zero_node_label] 
    return {k: v for v, k in enumerate(node_labels_without_zero)}

def create_node_matrix_from_network(network: Network, node_index_mapping: NodeIndexMapper = alphabetic_mapper) -> np.ndarray:
    super_nodes = SuperNodes(network)
    passive_net = passive_network(network)
    A = np.zeros((network.number_of_nodes-1, network.number_of_nodes-1), dtype=complex)
    def passive_node_pair(node1: str, node2: str) -> bool:
        return not super_nodes.is_active(node1) and not super_nodes.is_active(node2)
    node_mapping = node_index_mapping(network)
    for (i_label, i), (j_label, j) in itertools.product(node_mapping.items(), repeat=2):
        if passive_node_pair(i_label, j_label):
            if i_label == j_label:
                A[i, i] = admittance_connected_to(passive_net, i_label)
            else:
                A[i, j] = -admittance_between(passive_net, i_label, j_label)
        else:
            if i_label == j_label:
                A[i,i] = -np.sign(super_nodes.get_voltage(i_label))
            else:
                if not super_nodes.is_active(j_label):
                    if not super_nodes.belong_to_same(i_label, j_label):
                        A[i,j] = -admittance_between(network, i_label, j_label)
                    else:
                        A[i,j] = admittance_connected_to(network, i_label) - admittance_between(network, i_label, j_label)
                    
                    if super_nodes.is_reference(j_label):
                        A[i,j] -= admittance_between(network, i_label, super_nodes.get_active_node2(j_label))
                else:
                    if super_nodes.belong_to_same(i_label, j_label):
                        A[j,i] = np.sign(super_nodes.get_voltage(i_label))
    return A

def create_current_vector_from_network(network: Network, node_index_mapper: NodeIndexMapper = alphabetic_mapper) -> np.ndarray:
    super_nodes = SuperNodes(network)
    def voltage_to_next_passive_node(active_node: str) -> complex:
        V = 0+0j
        while super_nodes.is_active(active_node):
            V += super_nodes.get_voltage(active_node)
            active_node = super_nodes.get_counterpart(active_node)
        return V
    b = np.zeros(network.number_of_nodes-1, dtype=complex)
    node_mapping = node_index_mapper(network)
    active_node_labels = [l for l in node_mapping.keys() if super_nodes.is_active(l)]
    for i_label, i in node_mapping.items():
        current_sources = [b for b in network.branches_connected_to(i_label) if is_ideal_current_source(b.element)]
        b[i] += sum([-cs.element.I if cs.node1 == i_label else cs.element.I for cs in current_sources])
    for i_label, i in node_mapping.items():
        if super_nodes.is_active(i_label):
            b[i] -= voltage_to_next_passive_node(i_label)*admittance_connected_to(network, i_label)
            if super_nodes.is_active(super_nodes.get_counterpart(i_label)):
                b[i] += super_nodes.get_voltage(super_nodes.get_counterpart(i_label))*admittance_between(network, i_label, super_nodes.get_counterpart(i_label))
            else:
                connected_active_nodes = [n for n in network.nodes_connected_to(i_label) if super_nodes.is_active(n)]
                for cn in connected_active_nodes:
                    b[i] += voltage_to_next_passive_node(cn)*admittance_between(network, i_label, cn)
        else:
            b[i] += sum([voltage_to_next_passive_node(an)*admittance_between(network, i_label, an) for an in active_node_labels if super_nodes.get_counterpart(an) != i_label])
            if super_nodes.is_reference(i_label):
                b[i] -= voltage_to_next_passive_node(super_nodes.get_active_node2(i_label))*admittance_connected_to(network, super_nodes.get_active_node2(i_label))
                b[i] += voltage_to_next_passive_node(super_nodes.get_active_node2(i_label))*admittance_between(network, i_label, super_nodes.get_active_node2(i_label))
                connected_active_nodes = [n for n in network.nodes_connected_to(super_nodes.get_active_node2(i_label)) if super_nodes.is_active(n)]
                for cn in connected_active_nodes:
                    b[i] += voltage_to_next_passive_node(cn)*admittance_between(network, super_nodes.get_active_node2(i_label), cn)
    return b

class NodalAnalysisSolution:
    def __init__(self, network : Network, node_mapping: NodeIndexMapper = alphabetic_mapper) -> None:
        Y = create_node_matrix_from_network(network)
        I = create_current_vector_from_network(network)
        self._network = network
        self._solution_vector = cna.calculate_node_voltages(Y, I)
        self._node_type = SuperNodes(network)
        self._node_mapping = node_mapping(network)

    def _calculate_potential_of_active_node(self, node: str) -> complex:
        phi = 0+0j
        while self._node_type.is_active(node):
            phi += self._node_type.get_voltage(node)
            node = self._node_type.get_counterpart(node)
        if not self._network.is_zero_node(node):
            phi += self._solution_vector[self._node_mapping[node]]
        return phi

    def _calculate_potential_of_node(self, node: str) -> complex:
        if self._network.is_zero_node(node):
            return 0+0j
        elif not self._node_type.is_active(node):
            return self._solution_vector[self._node_mapping[node]]
        else:
            return self._calculate_potential_of_active_node(node)
    
    def get_voltage(self, branch: Branch) -> complex:
        phi1 = self._calculate_potential_of_node(branch.node1)
        phi2 = self._calculate_potential_of_node(branch.node2)
        return phi1-phi2

    def get_current(self, branch: Branch) -> complex:
        if is_ideal_voltage_source(branch.element):
            return self._solution_vector[self._node_mapping[self._node_type.get_active_node(branch.element)]]
        elif is_ideal_current_source(branch.element):
            return branch.element.I
        else:
            return self.get_voltage(branch)/branch.element.Z.real

def nodal_analysis_solver(network) -> NetworkSolution:
    return NodalAnalysisSolution(network)
