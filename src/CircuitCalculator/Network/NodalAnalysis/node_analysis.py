import numpy as np

from ..network import Network
from ..elements import is_ideal_voltage_source, is_current_source
from . import label_mapping as map
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

def node_admittance_matrix(network: Network, node_index_mapper: map.NetworkMapper = map.default_node_mapper) -> np.ndarray:
    def node_matrix_element(i_label:str, j_label:str) -> complex:
        if i_label == j_label:
            return admittance_connected_to(no_voltage_sources_network, i_label)
        return -admittance_between(no_voltage_sources_network, i_label, j_label)
    node_mapping = node_index_mapper(network)
    no_voltage_sources_network = Network(branches=[b for b in network.branches if not is_ideal_voltage_source(b.element)], node_zero_label=network.node_zero_label)
    Y = np.zeros((node_mapping.N, node_mapping.N), dtype=complex)
    for i_label, j_label in itertools.product(node_mapping, repeat=2):
        Y[node_mapping(i_label, j_label)] = node_matrix_element(i_label, j_label)
    return Y

def voltage_source_incidence_matrix(network: Network, node_mapper: map.NetworkMapper = map.default_node_mapper, source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper) -> np.ndarray:
    def voltage_source_direction(voltage_source: str, node: str) -> int:
        if network[voltage_source].node1 == node:
            return 1
        if network[voltage_source].node2 == node:
            return -1
        return 0
    node_index = node_mapper(network)
    vs_index = source_mapper(network)
    A = np.zeros((node_index.N, vs_index.N))
    for node, vs in itertools.product(node_index.keys, vs_index.keys):
        A[node_index[node], vs_index[vs]] = voltage_source_direction(vs, node)
    return A

def nodal_analysis_coefficient_matrix(network: Network, node_mapper: map.NetworkMapper = map.default_node_mapper, source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper) -> np.ndarray:
    Y = node_admittance_matrix(network, node_mapper)
    B = voltage_source_incidence_matrix(network, node_mapper, source_mapper)
    Z = np.zeros((B.shape[1], B.shape[1]))
    return np.vstack((np.hstack((Y, B)), np.hstack((B.T, Z))))

def source_incidence_matrix(network: Network, node_mapper: map.NetworkMapper = map.default_node_mapper, source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper) -> np.ndarray:
    node_index = node_mapper(network)
    cs_index = source_mapper(network)
    Q = np.zeros((node_index.N, cs_index.N))
    for cs in cs_index.keys:
        source_element = network[cs]
        if network.node_zero_label != source_element.node1:
            Q[node_index[source_element.node1]][cs_index[cs]] = -1
        if network.node_zero_label != network[cs].node2:
            Q[node_index[source_element.node2]][cs_index[cs]] = 1
    return Q

def current_source_vector(network: Network, source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper) -> np.ndarray:
    cs_index = map.filter(source_mapper(network), lambda x: is_current_source(network[x].element))
    return np.array([network[x].element.I for x in cs_index.keys])

def current_source_incidence_vector(network: Network, node_mapper: map.NetworkMapper = map.default_node_mapper, source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper) -> np.ndarray:
    Q = source_incidence_matrix(network, node_mapper=node_mapper, source_mapper=source_mapper)
    Is = current_source_vector(network, source_mapper=source_mapper)
    return Q@Is

def nodal_analysis_constants_vector(network: Network, node_mapper: map.NetworkMapper = map.default_node_mapper, current_source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper, voltage_source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper) -> np.ndarray:
    I = current_source_incidence_vector(network, node_mapper, current_source_mapper)

    vs_mapping = voltage_source_mapper(network)
    V = np.array([network[vs].element.V for vs in vs_mapping.keys])
    return np.hstack((I, V))

def open_circuit_impedance(network: Network, node1: str, node2: str, node_index_mapper: map.NetworkMapper = map.default_node_mapper) -> complex:
    if node1 == node2:
        return 0
    if any([is_ideal_voltage_source(b.element) for b in network.branches_between(node1, node2)]):
        return 0
    if network.is_zero_node(node1):
        node1, node2 = node2, node1
    network = trf.switch_ground_node(network=network, new_ground=node2)
    Y = node_admittance_matrix(network, node_index_mapper=node_index_mapper)
    Y = np.delete(Y, np.where(~Y.any(axis=0))[0], axis=1)
    Y = np.delete(Y, np.where(~Y.any(axis=1))[0], axis=0)
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

def calculate_node_voltages0(Y : np.ndarray, I : np.ndarray) -> np.ndarray:
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
