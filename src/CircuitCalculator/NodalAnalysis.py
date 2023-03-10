import numpy as np
from .Network.network import Network
from .Network.elements import is_ideal_current_source, is_ideal_voltage_source, is_current_source
from .Network.transformers import passive_network
from .Network.supernodes import SuperNodes
from .Network import labelmapper as map
from .Network.solution import NetworkSolution
import itertools

class DimensionError(Exception): pass

def admittance_connected_to(network: Network, node: str) -> complex:
    return sum(b.element.Y for b in network.branches_connected_to(node) if np.isfinite(b.element.Y))

def admittance_between(network: Network, node1: str, node2: str) -> complex:
    return sum([b.element.Y for b in network.branches_between(node1, node2) if np.isfinite(b.element.Y)])

def create_node_matrix_from_network(network: Network, node_index_mapper: map.NodeIndexMapper = map.default) -> np.ndarray:
    super_nodes = SuperNodes(network)
    passive_net = passive_network(network)
    node_mapping = node_index_mapper(network)
    A = np.zeros((network.number_of_nodes-1, network.number_of_nodes-1), dtype=complex)
    def passive_node_pair(node1: str, node2: str) -> bool:
        return not super_nodes.is_active(node1) and not super_nodes.is_active(node2)
    def both_active(node1: str, node2: str) -> bool:
        return super_nodes.is_active(node1) and super_nodes.is_active(node2)
    def passive_matrix_element(node1: str, node2: str) -> complex:
        if node1 == node2:
            return admittance_connected_to(passive_net, node1)
        else:
            return -admittance_between(passive_net, node1, node2)
    def non_active_j_label() -> complex:
        Aij = -admittance_between(network, i_label, j_label)
        if super_nodes.is_reference(j_label):
            Aij -= admittance_between(network, i_label, super_nodes.get_active_node(j_label))
        if super_nodes.belong_to_same(i_label, j_label):
            Aij += admittance_connected_to(network, i_label)
        return Aij
    def matrix_element(i_label: str, j_label: str) -> complex:
        if passive_node_pair(i_label, j_label):
            return passive_matrix_element(i_label, j_label)
        if i_label == j_label:
            return -super_nodes.sign(i_label)
        if both_active(i_label, j_label) and super_nodes.belong_to_same(j_label, i_label):
            return super_nodes.sign(j_label)
        if not super_nodes.is_active(j_label):
            return non_active_j_label()
        return 0+0j
    for (i_label, i), (j_label, j) in itertools.product(node_mapping.items(), repeat=2):
        A[i, j] = matrix_element(i_label, j_label)
    return A

def create_current_vector_from_network(network: Network, node_index_mapper: map.NodeIndexMapper = map.default) -> np.ndarray:
    super_nodes = SuperNodes(network)
    b = np.zeros(network.number_of_nodes-1, dtype=complex)
    node_mapping = node_index_mapper(network)
    active_node_labels = [l for l in node_mapping.keys() if super_nodes.is_active(l)]
    def current_sources(node: str) -> complex:
        current_sources = [b for b in network.branches_connected_to(node) if is_current_source(b.element)]
        return sum([-cs.element.I if cs.node1 == node else cs.element.I for cs in current_sources])
    def connected_active_nodes(active_node: str) -> list[str]:
        return [n for n in network.nodes_connected_to(active_node) if super_nodes.is_active(n)]
    def active_node_current(active_node: str) -> complex:
        I_connected_admittances = super_nodes.voltage_to_next_reference(active_node)*admittance_connected_to(network, active_node)
        reference_node = super_nodes.get_reference_node(active_node)
        if super_nodes.is_active(reference_node):
            I_parallel_admittance = super_nodes.voltage_to_next_reference(reference_node)*admittance_between(network, active_node, reference_node)
            return I_parallel_admittance-I_connected_admittances
        return sum([super_nodes.voltage_to_next_reference(cn)*admittance_between(network, active_node, cn) for cn in connected_active_nodes(active_node)])-I_connected_admittances
    def passive_node_current(passive_node: str) -> complex:
        I_parallel_admittances = sum([super_nodes.voltage_to_next_reference(an)*admittance_between(network, an, passive_node) for an in active_node_labels if super_nodes.get_reference_node(an) != passive_node])
        if super_nodes.is_reference(passive_node):
            active_node = super_nodes.get_active_node(passive_node)
            I_connected_admittances = super_nodes.voltage_to_next_reference(active_node)*admittance_connected_to(network, active_node)
            I_parallel_to_active_nodes = sum([super_nodes.voltage_to_next_reference(cn)*admittance_between(network, active_node, cn) for cn in connected_active_nodes(active_node)])
            I_parallel_to_passive_nodes = super_nodes.voltage_to_next_reference(active_node)*admittance_between(network, active_node, passive_node)
            return I_parallel_admittances+I_parallel_to_active_nodes+I_parallel_to_passive_nodes-I_connected_admittances
        return I_parallel_admittances
    def current_of_voltage_sources(node: str) -> complex:
        if super_nodes.is_active(node):
            return active_node_current(node)
        return passive_node_current(node)
    for i_label, i in node_mapping.items():
        b[i] = current_sources(i_label) + current_of_voltage_sources(i_label)
    return b

def calculate_node_voltages(Y : np.ndarray, I : np.ndarray) -> np.ndarray:
    if np.any(np.logical_not(np.isfinite(Y))):
        raise ValueError
    if np.any(np.logical_not(np.isfinite(I))):
        raise ValueError
    if Y.ndim != 2:
        raise DimensionError('dim error')
    if I.ndim != 1:
        raise DimensionError('dim error')
    m, n = Y.shape
    if n != m:
        raise DimensionError('dim error')
    return np.linalg.solve(Y, I)

class NodalAnalysisSolution:
    def __init__(self, network : Network, node_mapper: map.NodeIndexMapper = map.default) -> None:
        Y = create_node_matrix_from_network(network, node_index_mapper=node_mapper)
        I = create_current_vector_from_network(network, node_index_mapper=node_mapper)
        self._network = network
        self._solution_vector = calculate_node_voltages(Y, I)
        self._super_nodes = SuperNodes(network)
        self._node_mapping = node_mapper(network)

    def _calculate_potential_of_node(self, node: str) -> complex:
        V_active = 0+0j
        if self._super_nodes.is_active(node):
            V_active = self._super_nodes.voltage_to_next_reference(node)
            node = self._super_nodes.next_reference(node)
        if self._network.is_zero_node(node):
            return V_active
        return self._solution_vector[self._node_mapping[node]] + V_active

    def _select_active_node(self, branch_id: str) -> str:
        branch = self._network[branch_id]
        if self._super_nodes.is_active(branch.node1):
            return branch.node1
        return branch.node2
    
    def get_voltage(self, branch_id: str) -> complex:
        phi1 = self._calculate_potential_of_node(self._network[branch_id].node1)
        phi2 = self._calculate_potential_of_node(self._network[branch_id].node2)
        return phi1-phi2

    def get_current(self, branch_id: str) -> complex:
        branch_element = self._network[branch_id].element
        if is_ideal_current_source(branch_element):
            return branch_element.I
        if is_ideal_voltage_source(branch_element):
            return self._solution_vector[self._node_mapping[self._select_active_node(branch_id)]]
        return self.get_voltage(branch_id)/branch_element.Z

def nodal_analysis_solver(network) -> NetworkSolution:
    return NodalAnalysisSolution(network)
