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

# def nodal_analysis_solution(network: Network, matrix_ops: mo.MatrixOperations = mo.NumPyMatrixOperations(), node_mapper: map.NetworkMapper = map.default_node_mapper, voltage_source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper, current_source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper) -> tuple[complex | symbolic, ...]:
#     A = nodal_analysis_coefficient_matrix(network, matrix_ops=matrix_ops, node_mapper=node_mapper, source_mapper=voltage_source_mapper)
#     b = nodal_analysis_constants_vector(network, matrix_ops=matrix_ops, node_mapper=node_mapper, current_source_mapper=current_source_mapper, voltage_source_mapper=voltage_source_mapper)
#     try:
#         return matrix_ops.solve(A, b)
#     except mo.MatrixInversionException:
#         return (float('nan'),) * len(b)

# def open_circuit_impedance(network: Network, node1: str, node2: str, matrix_ops: mo.MatrixOperations = mo.NumPyMatrixOperations(), node_index_mapper: map.NetworkMapper = map.default_node_mapper) -> complex | symbolic:
#     if node1 == node2:
#         return matrix_ops.elm(0).value
#     if any([b.element.is_ideal_voltage_source for b in network.branches_between(node1, node2)]):
#         return matrix_ops.elm(0).value
#     if network.is_zero_node(node1):
#         node1, node2 = node2, node1
#     network = trf.switch_ground_node(network=network, new_ground=node2)
#     Y = nodal_analysis_coefficient_matrix(network, matrix_ops=matrix_ops, node_mapper=node_index_mapper)
#     Y = matrix_ops.delete(Y, np.where(~matrix_ops.any_element(Y, axis=0))[0].tolist(), axis=1)
#     Y = matrix_ops.delete(Y, np.where(~matrix_ops.any_element(Y, axis=1))[0].tolist(), axis=0)
#     Z = matrix_ops.inv(Y)
#     i1 = node_index_mapper(network)[node1]
#     return Z.diagonal()[i1]

# def element_impedance(network: Network, element: str, matrix_ops: mo.MatrixOperations = mo.NumPyMatrixOperations(), node_index_mapper: map.NetworkMapper = map.default_node_mapper) -> complex | symbolic:
#     return open_circuit_impedance(
#         network=trf.remove_element(network, element),
#         node1=network[element].node1,
#         node2=network[element].node2,
#         matrix_ops=matrix_ops,
#         node_index_mapper=node_index_mapper
#     )

# def state_space_matrices(network: Network, c_values: Mapping[str, float | symbolic] = {}, l_values: Mapping[str, float | symbolic] = {}, matrix_ops: mo.MatrixOperations = mo.NumPyMatrixOperations(), node_mapper: map.NetworkMapper = map.default_node_mapper, current_source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper, voltage_source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper) -> tuple[mo.Matrix, mo.Matrix, mo.Matrix, mo.Matrix]:
#     def element_incidence_matrix(values: Mapping[str, float | symbolic]) -> np.ndarray:
#         node_mapping = node_mapper(network)
#         Delta = np.zeros((len(values), node_mapping.N))
#         for (k, value), (i_label) in itertools.product(enumerate(values), node_mapping):
#             if i_label == network[value].node1:
#                 Delta[k][node_mapping(i_label)] = +1
#             if i_label == network[value].node2:
#                 Delta[k][node_mapping(i_label)] = -1
#         return np.hstack((Delta, np.zeros((Delta.shape[0], voltage_source_mapper(network).N))))
#     def source_and_inductance_incidence_matrix(values: Mapping[str, float | symbolic]) -> tuple[np.ndarray, np.ndarray]:
#         voltage_source_mapping_all = voltage_source_mapper(network)
#         source_mapping_all = map.default_source_mapper(network)
#         Qi = source_incidence_matrix(network=network, node_mapper=node_mapper, source_mapper=current_source_mapper)
#         Q = np.zeros((voltage_source_mapping_all.N, voltage_source_mapping_all.N), dtype=int)
#         for i in voltage_source_mapping_all.values:
#             Q[i][i] = 1
#         Q = np.vstack((np.hstack( (Qi, np.zeros((Qi.shape[0], Q.shape[1]) ))),
#                     np.hstack( (np.zeros((Q.shape[0], Qi.shape[1])), Q) )))
#         QS = Q[:,[source_mapping_all[l] for l in source_mapping_all if l not in values]]
#         QL = Q[:,[source_mapping_all[l] for l in source_mapping_all if l in values]]
#         return QS, QL
#     def value_matrix(c_values: Mapping[str, float | symbolic], l_values: Mapping[str, float | symbolic]) -> np.ndarray:
#         return matrix_ops.vstack((
#             matrix_ops.hstack(( matrix_ops.diag([-C for C in c_values.values()]), matrix_ops.zeros((len(c_values), len(l_values))) )), # type: ignore
#             matrix_ops.hstack(( matrix_ops.zeros((len(l_values), len(c_values))), matrix_ops.diag([L for L in l_values.values()]) ))
#         ))

#     Delta = element_incidence_matrix(c_values)
#     A_tilde = nodal_analysis_coefficient_matrix(network, matrix_ops=matrix_ops, node_mapper=node_mapper, source_mapper=voltage_source_mapper)
#     QS, QL = source_and_inductance_incidence_matrix(l_values)
#     DQ = np.hstack((Delta.T, QL))
#     Lambda = value_matrix(c_values, l_values)
#     invLambda = matrix_ops.diag([1/L for L in matrix_ops.diag_vec(Lambda)]) # type: ignore

#     inv_A_tilde = matrix_ops.inv(A_tilde)
#     transformed_inv_A_tilde = DQ.T @ inv_A_tilde
#     sorted_A_tilde = matrix_ops.inv(transformed_inv_A_tilde @ DQ)

#     A = invLambda @ sorted_A_tilde
#     C = transformed_inv_A_tilde.T @ sorted_A_tilde
#     B = (-invLambda @ C.T) @ QS
#     D = (inv_A_tilde - transformed_inv_A_tilde.T @ C.T) @ QS

#     return A, B, C, D
