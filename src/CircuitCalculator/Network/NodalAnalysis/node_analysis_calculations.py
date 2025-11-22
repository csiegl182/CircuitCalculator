import numpy as np
import itertools
from typing import Any, Callable
from ..network import Network
from . import matrix_operations as mo
from .. import transformers as trf
from .label_mapping import NetworkLabelMappings

class DimensionError(Exception):
    ...

def admittance_connected_to(network: Network, node: str, me: Callable[[Any], mo.MatrixElement]) -> complex:
    return sum([e.value for e in [me(b.element.Y) for b in network.branches_connected_to(node)] if e.isfinite])

def admittance_between(network: Network, node1: str, node2: str, me: Callable[[Any], mo.MatrixElement]) -> complex:
    return sum([e.value for e in [me(b.element.Y) for b in network.branches_between(node1, node2)] if e.isfinite])

def node_admittance_matrix(network: Network, matrix_ops: mo.MatrixOperations, label_mappings: NetworkLabelMappings) -> mo.Matrix:
    def node_matrix_element(i_label:str, j_label:str) -> complex:
        if i_label == j_label:
            return admittance_connected_to(passive_network, i_label, matrix_ops.elm)
        return -admittance_between(passive_network, i_label, j_label, matrix_ops.elm)
    node_mapping = label_mappings.node_mapper(network)
    passive_network = trf.remove_active_elements(network)
    Y = matrix_ops.zeros((node_mapping.N, node_mapping.N))
    for i_label, j_label in itertools.product(node_mapping, repeat=2):
        Y[node_mapping(i_label, j_label)] = node_matrix_element(i_label, j_label)
    return Y

def voltage_source_incidence_matrix(network: Network, matrix_ops: mo.MatrixOperations, label_mappings: NetworkLabelMappings) -> mo.Matrix:
    def voltage_source_direction(voltage_source: str, node: str) -> int:
        if network[voltage_source].node1 == node:
            return 1
        if network[voltage_source].node2 == node:
            return -1
        return 0
    node_index = label_mappings.node_mapper(network)
    A = matrix_ops.zeros((node_index.N, label_mappings.voltage_source_mapping.N))
    for node, vs in itertools.product(node_index.keys, label_mappings.voltage_source_mapping.keys):
        A[node_index[node], label_mappings.voltage_source_mapping[vs]] = voltage_source_direction(vs, node)
    return A

def nodal_analysis_coefficient_matrix(network: Network, matrix_ops: mo.MatrixOperations, label_mappings: NetworkLabelMappings) -> mo.Matrix:
    Y = node_admittance_matrix(network, matrix_ops, label_mappings)
    B = voltage_source_incidence_matrix(network, matrix_ops, label_mappings)
    Z = matrix_ops.zeros((B.shape[1], B.shape[1]))
    return matrix_ops.vstack((matrix_ops.hstack((Y, B)), matrix_ops.hstack((B.T, Z))))

def source_incidence_matrix(network: Network, label_mappings: NetworkLabelMappings) -> np.ndarray:
    node_index = label_mappings.node_mapper(network)
    cs_index = label_mappings.current_source_mapper(network)
    Q = np.zeros((node_index.N, cs_index.N))
    for cs in cs_index.keys:
        source_element = network[cs]
        if network.reference_node_label != source_element.node1:
            Q[node_index[source_element.node1]][cs_index[cs]] = -1
        if network.reference_node_label != network[cs].node2:
            Q[node_index[source_element.node2]][cs_index[cs]] = 1
    return Q

def current_source_vector(network: Network, matrix_ops: mo.MatrixOperations, label_mappings: NetworkLabelMappings) -> mo.Matrix:
    cs_index = label_mappings.current_source_mapping.filter_keys(lambda x: network[x].element.is_current_source)
    return matrix_ops.column_vector([network[x].element.I for x in cs_index.keys])

def current_source_incidence_vector(network: Network, matrix_ops: mo.MatrixOperations, label_mappings: NetworkLabelMappings) -> np.ndarray:
    Q = source_incidence_matrix(network, label_mappings)
    Is = current_source_vector(network, matrix_ops, label_mappings)
    return Q@Is

def nodal_analysis_constants_vector(network: Network, matrix_ops: mo.MatrixOperations, label_mappings: NetworkLabelMappings) -> mo.Matrix:
    I = current_source_incidence_vector(network, matrix_ops, label_mappings)
    V = matrix_ops.column_vector([network[vs].element.V for vs in label_mappings.voltage_source_mapping.keys])
    return matrix_ops.vstack((I, V))