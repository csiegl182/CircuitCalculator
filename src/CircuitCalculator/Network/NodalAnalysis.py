import numpy as np
from .network import Network
from .elements import is_ideal_current_source, is_ideal_voltage_source, is_current_source
from .transformers import passive_network
from .supernodes import SuperNodes
from . import labelmapper as map
from .solution import NetworkSolution
import itertools

class DimensionError(Exception):
    ...

def admittance_connected_to(network: Network, node: str) -> complex:
    return sum(b.element.Y for b in network.branches_connected_to(node) if np.isfinite(b.element.Y))

def admittance_between(network: Network, node1: str, node2: str) -> complex:
    return sum([b.element.Y for b in network.branches_between(node1, node2) if np.isfinite(b.element.Y)])

def connected_nodes(network: Network, node: str) -> list[str]:
    return [b.node1 if b.node1 != node else b.node2 for b in network.branches_connected_to(node)]

def create_node_matrix_from_network(network: Network, node_index_mapper: map.NodeIndexMapper = map.default) -> np.ndarray:
    def node_matrix_element(i_label:str, j_label:str) -> complex:
        if i_label == j_label:
            return admittance_connected_to(passive_net, i_label)
        return -admittance_between(passive_net, i_label, j_label)
    passive_net = passive_network(network)
    node_mapping = node_index_mapper(network)
    A = np.zeros((len(node_mapping), len(node_mapping)), dtype=complex)
    for (i_label, i), (j_label, j) in itertools.product(node_mapping.items(), repeat=2):
        A[i, j] = node_matrix_element(i_label, j_label)
    return A

def create_current_vector_from_network(network: Network, node_index_mapper: map.NodeIndexMapper = map.default) -> np.ndarray:
    super_nodes = SuperNodes(network)
    node_mapping = node_index_mapper(network)
    reference_node_mapping = {n: i for n, i in node_mapping.items() if super_nodes.is_reference(n)}
    b = np.zeros(len(node_mapping), dtype=complex)
    def current_sources(node: str) -> complex:
        current_sources = [b for b in network.branches_connected_to(node) if is_current_source(b.element)]
        return sum([-cs.element.I if cs.node1 == node else cs.element.I for cs in current_sources])
    def currents_of_connected_active_nodes(node: str) -> complex:
        connected_active_nodes = [n for n in connected_nodes(network, node) if super_nodes.is_active(n)]
        connected_active_nodes = [n for n in connected_active_nodes if not super_nodes.belong_to_same(n, node)]
        return sum([super_nodes.voltage_to_next_reference(cn)*admittance_between(network, cn, node) for cn in connected_active_nodes])
    def currents_of_belonging_voltage_sources(reference_node: str) -> complex:
        an = super_nodes.get_active_node(reference_node)
        connected_admittances_without_parallel_one = admittance_connected_to(network, an)-admittance_between(network, an, reference_node)
        return -super_nodes.voltage_to_next_reference(an)*connected_admittances_without_parallel_one
    for i_label, i in node_mapping.items():
        b[i] = current_sources(i_label)
        b[i] += currents_of_connected_active_nodes(i_label)
    for ref_label, i in reference_node_mapping.items():
        b[i] += current_sources(super_nodes.get_active_node(ref_label))
        b[i] += currents_of_connected_active_nodes(super_nodes.get_active_node(ref_label))
        b[i] += currents_of_belonging_voltage_sources(ref_label)
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
        self._super_nodes = SuperNodes(network)
        self._node_mapping = node_mapper(network)
        try:
            self._solution_vector = calculate_node_voltages(Y, I)
        except np.linalg.LinAlgError:
            self._solution_vector = np.zeros(np.size(I))

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
            other_branches = [branch for branch in self._network.branches_connected_to(self._network[branch_id].node1) if branch.id != branch_id]
            node_currents = [+self.get_current(branch.id) if branch.node1==self._network[branch_id].node1 else -self.get_current(branch.id) for branch in other_branches]
            return -sum(node_currents)
        return self.get_voltage(branch_id)/branch_element.Z

    def get_power(self, branch_id: str) -> complex:
        return self.get_voltage(branch_id)*self.get_current(branch_id).conjugate()

def nodal_analysis_solver(network: Network) -> NetworkSolution:
    return NodalAnalysisSolution(network)
