import numpy as np
from .network import Network
from .elements import is_ideal_current_source, is_ideal_voltage_source, is_current_source, is_voltage_source
from .supernodes import SuperNodes
from . import labelmapper as map
from . import transformers as trf
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
    passive_net = trf.passive_network(network)
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
        connected_active_nodes = {n for n in connected_nodes(network, node) if super_nodes.is_active(n)}
        connected_active_nodes = {n for n in connected_active_nodes if not super_nodes.belong_to_same(n, node)}
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
        
def open_circuit_impedance(network: Network, node1: str, node2: str, node_index_mapper: map.NodeIndexMapper = map.default) -> complex:
    if node1 == node2:
        return 0
    if any([is_ideal_voltage_source(b.element) for b in network.branches_between(node1, node2)]):
        return 0
    if network.is_zero_node(node1):
        node1, node2 = node2, node1
    network = trf.switch_ground_node(network=network, new_ground=node2)
    network = trf.passive_network(network)
    Y = create_node_matrix_from_network(network, node_index_mapper=node_index_mapper)
    Z = np.linalg.inv(Y)
    i1 = node_index_mapper(network)[node1]
    return Z[i1][i1]

def element_impedance(network: Network, element: str, node_index_mapper: map.NodeIndexMapper = map.default) -> complex:
    return open_circuit_impedance(
        network=trf.remove_element(network, element),
        node1=network[element].node1,
        node2=network[element].node2,
        node_index_mapper=node_index_mapper
    )

def open_circuit_voltage(network: Network, node1: str, node2: str) -> complex:
    if node1 == node2:
        return 0
    solution = NodalAnalysisSolution(network)
    phi1 = solution.get_potential(node=node1)
    phi2 = solution.get_potential(node=node2)
    return phi1-phi2

def short_circuit_current(network: Network, node1: str, node2: str) -> complex:
    Z = open_circuit_impedance(network, node1, node2)
    V = open_circuit_voltage(network, node1, node2)
    return V/Z

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

    def _select_active_node(self, branch_id: str) -> str:
        branch = self._network[branch_id]
        if self._super_nodes.is_active(branch.node1):
            return branch.node1
        return branch.node2

    def get_potential(self, node: str) -> complex:
        V_active = 0+0j
        if self._super_nodes.is_active(node):
            V_active = self._super_nodes.voltage_to_next_reference(node)
            node = self._super_nodes.next_reference(node)
        if self._network.is_zero_node(node):
            return V_active
        return self._solution_vector[self._node_mapping[node]] + V_active
    
    def get_voltage(self, branch_id: str) -> complex:
        phi1 = self.get_potential(self._network[branch_id].node1)
        phi2 = self.get_potential(self._network[branch_id].node2)
        return phi1-phi2

    def get_current(self, branch_id: str) -> complex:
        branch = self._network[branch_id]
        if is_ideal_current_source(branch.element):
            return branch.element.I
        if is_ideal_voltage_source(branch.element):
            Z = element_impedance(self._network, branch_id)
            I_branch_element = -branch.element.V/Z
            I_other_elements = short_circuit_current(
                trf.remove_element(self._network, branch_id),
                branch.node1,
                branch.node2)
            return  I_branch_element+I_other_elements
        if is_voltage_source(branch.element):
            return -(self.get_voltage(branch_id)+branch.element.V)/branch.element.Z
        return self.get_voltage(branch_id)/branch.element.Z

    def get_power(self, branch_id: str) -> complex:
        return self.get_voltage(branch_id)*self.get_current(branch_id).conjugate()

def nodal_analysis_solver(network: Network) -> NetworkSolution:
    return NodalAnalysisSolution(network)
