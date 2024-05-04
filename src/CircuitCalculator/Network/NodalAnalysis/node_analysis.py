import numpy as np

from ..network import Network
from ..elements import is_ideal_voltage_source, is_current_source
from .supernodes import SuperNodes, voltage_to_next_reference
from . import labelmapper as map
from .. import transformers as trf
import itertools

class DimensionError(Exception):
    ...

def admittance_connected_to(network: Network, node: str) -> complex:
    return sum(b.element.Y for b in network.branches_connected_to(node) if np.isfinite(b.element.Y))

def admittance_between(network: Network, node1: str, node2: str) -> complex:
    return sum([b.element.Y for b in network.branches_between(node1, node2) if np.isfinite(b.element.Y)])

def connected_nodes(network: Network, node: str) -> list[str]:
    return [b.node1 if b.node1 != node else b.node2 for b in network.branches_connected_to(node)]

def create_node_matrix_from_network(network: Network, node_index_mapper: map.NetworkMapper = map.default_node_mapper) -> np.ndarray:
    def node_matrix_element(i_label:str, j_label:str) -> complex:
        if i_label == j_label:
            return admittance_connected_to(passive_net, i_label)
        return -admittance_between(passive_net, i_label, j_label)
    passive_net = trf.passive_network(network)
    node_mapping = node_index_mapper(network)
    Y = np.zeros((node_mapping.N, node_mapping.N), dtype=complex)
    for i_label, j_label in itertools.product(node_mapping, repeat=2):
        Y[node_mapping(i_label, j_label)] = node_matrix_element(i_label, j_label)
    return Y

def create_current_vector_from_network(network: Network, node_index_mapper: map.NetworkMapper = map.default_node_mapper) -> np.ndarray:
    super_nodes = SuperNodes(network)
    node_mapping = node_index_mapper(network)
    reference_node_mapping = map.filter_mapping(node_mapping, super_nodes.is_reference)
    b = np.zeros(node_mapping.N, dtype=complex)
    def current_sources(node: str) -> complex:
        current_sources = [b for b in network.branches_connected_to(node) if is_current_source(b.element)]
        return sum([-cs.element.I if cs.node1 == node else cs.element.I for cs in current_sources])
    def currents_of_connected_active_nodes(node: str) -> complex:
        connected_active_nodes = {n for n in connected_nodes(network, node) if super_nodes.is_active(n)}
        connected_active_nodes = {n for n in connected_active_nodes if not super_nodes.belong_to_same(n, node)}
        return sum([voltage_to_next_reference(network, super_nodes, cn)*admittance_between(network, cn, node) for cn in connected_active_nodes])
    def currents_of_belonging_voltage_sources(reference_node: str) -> complex:
        an = super_nodes.active_node(reference_node)
        connected_admittances_without_parallel_one = admittance_connected_to(network, an)-admittance_between(network, an, reference_node)
        return -voltage_to_next_reference(network, super_nodes, an)*connected_admittances_without_parallel_one
    for label in node_mapping:
        b[node_mapping(label)] = current_sources(label)
        b[node_mapping(label)] += currents_of_connected_active_nodes(label)
    for label in reference_node_mapping:
        b[node_mapping(label)] += current_sources(super_nodes.active_node(label))
        b[node_mapping(label)] += currents_of_connected_active_nodes(super_nodes.active_node(label))
        b[node_mapping(label)] += currents_of_belonging_voltage_sources(label)
    return b
        
def create_source_incidence_matrix_from_network(network: Network, node_index_mapper: map.NetworkMapper = map.default_node_mapper, source_index_mapper: map.NetworkMapper = map.default_source_mapper) -> np.ndarray:
    def current_source_coefficient(source: str, node: str) -> int:
        if network[source].node1 == node:
            return -1
        if network[source].node2 == node:
            return +1
        return 0
    def admittance_to_active_node(network: Network, vs_label: str, node: str) -> complex:
        n1, n2 = network[vs_label].node1, network[vs_label].node2
        if n1 in super_nodes.active_nodes and n2 != node:
            return admittance_between(network, n1, node)
        if n2 in super_nodes.active_nodes and n1 != node:
            return -admittance_between(network, n2, node)
        return 0
    def admittance_of_active_node_without_parallel(network: Network, vs_label: str, node: str) -> complex:
        n1, n2 = network[vs_label].node1, network[vs_label].node2
        if node == n1:
            return admittance_connected_to(network, n2)-admittance_between(network, n1, n2)
        if node == n2:
            return -(admittance_connected_to(network, n1)-admittance_between(network, n1, n2))
        return 0
    def incidence_entry(node: str, source: str) -> complex:
        source_element = network[source].element
        if is_current_source(source_element):
            return current_source_coefficient(source, node)
        if is_ideal_voltage_source(network[source].element):
            vs_network = trf.passive_network(network=network, keep=[source_element])
            return admittance_to_active_node(vs_network, source, node)+admittance_of_active_node_without_parallel(vs_network, source, node)
        return 0
    super_nodes = SuperNodes(network)
    node_mapping = node_index_mapper(network)
    source_mapping = source_index_mapper(network)
    Q = np.zeros((node_mapping.N, source_mapping.N))
    for n_label, s_label in itertools.product(node_mapping, source_mapping):
        Q[node_mapping(n_label)][source_mapping(s_label)] = incidence_entry(n_label, s_label)
    return Q

def open_circuit_impedance(network: Network, node1: str, node2: str, node_index_mapper: map.NetworkMapper = map.default_node_mapper) -> complex:
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

def element_impedance(network: Network, element: str, node_index_mapper: map.NetworkMapper = map.default_node_mapper) -> complex:
    return open_circuit_impedance(
        network=trf.remove_element(network, element),
        node1=network[element].node1,
        node2=network[element].node2,
        node_index_mapper=node_index_mapper
    )

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
