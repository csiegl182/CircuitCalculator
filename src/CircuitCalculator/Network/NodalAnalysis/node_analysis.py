import numpy as np
import itertools
from typing import Mapping
from ..network import Network
from . import matrix_operations as mo
from .matrix_operations import symbolic
from .. import transformers as trf
from .label_mapping import LabelMappingsFactory, default_label_mappings_factory
from .node_analysis_calculations import nodal_analysis_coefficient_matrix, nodal_analysis_constants_vector, source_incidence_matrix

def nodal_analysis_solution(network: Network, matrix_ops: mo.MatrixOperations = mo.NumPyMatrixOperations(), label_mappings_factory: LabelMappingsFactory = default_label_mappings_factory) -> tuple[complex | symbolic, ...]:
    label_mappings = label_mappings_factory(network)
    A = nodal_analysis_coefficient_matrix(network, matrix_ops=matrix_ops, label_mappings=label_mappings)
    b = nodal_analysis_constants_vector(network, matrix_ops=matrix_ops, label_mappings=label_mappings)
    try:
        return matrix_ops.solve(A, b)
    except mo.MatrixInversionException:
        return (float('nan'),) * len(b)

def open_circuit_impedance(network: Network, node1: str, node2: str, matrix_ops: mo.MatrixOperations = mo.NumPyMatrixOperations(), label_mappings_factory: LabelMappingsFactory = default_label_mappings_factory) -> complex | symbolic:
    if node1 == node2:
        return matrix_ops.elm(0).value
    if any([b.element.is_ideal_voltage_source for b in network.branches_between(node1, node2)]):
        return matrix_ops.elm(0).value
    if network.is_zero_node(node1):
        node1, node2 = node2, node1
    network = trf.switch_ground_node(network=network, new_ground=node2)
    label_mappings = label_mappings_factory(network)
    Y = nodal_analysis_coefficient_matrix(network, matrix_ops=matrix_ops, label_mappings=label_mappings)
    Y = matrix_ops.delete(Y, np.where(~matrix_ops.any_element(Y, axis=0))[0].tolist(), axis=1)
    Y = matrix_ops.delete(Y, np.where(~matrix_ops.any_element(Y, axis=1))[0].tolist(), axis=0)
    Z = matrix_ops.inv(Y)
    i1 = label_mappings.node_mapping[node1]
    return Z.diagonal()[i1]

def element_impedance(network: Network, element: str, matrix_ops: mo.MatrixOperations = mo.NumPyMatrixOperations(), label_mappings_factory: LabelMappingsFactory = default_label_mappings_factory) -> complex | symbolic:
    return open_circuit_impedance(
        network=trf.remove_element(network, element),
        node1=network[element].node1,
        node2=network[element].node2,
        matrix_ops=matrix_ops,
        label_mappings_factory=label_mappings_factory
    )

def state_space_matrices(network: Network, c_values: Mapping[str, float | symbolic] = {}, l_values: Mapping[str, float | symbolic] = {}, matrix_ops: mo.MatrixOperations = mo.NumPyMatrixOperations(), label_mappings_factory: LabelMappingsFactory = default_label_mappings_factory) -> tuple[mo.Matrix, mo.Matrix, mo.Matrix, mo.Matrix]:
    label_mappings = label_mappings_factory(network)
    def element_incidence_matrix(values: Mapping[str, float | symbolic]) -> np.ndarray:
        Delta = np.zeros((len(values), label_mappings.node_mapping.N))
        for (k, value), (i_label) in itertools.product(enumerate(values), label_mappings.node_mapping):
            if i_label == network[value].node1:
                Delta[k][label_mappings.node_mapping(i_label)] = +1
            if i_label == network[value].node2:
                Delta[k][label_mappings.node_mapping(i_label)] = -1
        return np.hstack((Delta, np.zeros((Delta.shape[0], label_mappings.voltage_source_mapper(network).N))))
    def source_and_inductance_incidence_matrix(values: Mapping[str, float | symbolic]) -> tuple[np.ndarray, np.ndarray]:
        Qi = source_incidence_matrix(network=network, label_mappings=label_mappings)
        Q = np.zeros((label_mappings.voltage_source_mapping.N, label_mappings.voltage_source_mapping.N), dtype=int)
        for i in label_mappings.voltage_source_mapping.values:
            Q[i][i] = 1
        Q = np.vstack((np.hstack( (Qi, np.zeros((Qi.shape[0], Q.shape[1]) ))),
                    np.hstack( (np.zeros((Q.shape[0], Qi.shape[1])), Q) )))
        QS = Q[:,[label_mappings.source_mapping[l] for l in label_mappings.source_mapping if l not in values]]
        QL = Q[:,[label_mappings.source_mapping[l] for l in label_mappings.source_mapping if l in values]]
        return QS, QL
    def value_matrix(c_values: Mapping[str, float | symbolic], l_values: Mapping[str, float | symbolic]) -> np.ndarray:
        return matrix_ops.vstack((
            matrix_ops.hstack(( matrix_ops.diag([-C for C in c_values.values()]), matrix_ops.zeros((len(c_values), len(l_values))) )), # type: ignore
            matrix_ops.hstack(( matrix_ops.zeros((len(l_values), len(c_values))), matrix_ops.diag([L for L in l_values.values()]) ))
        ))

    Delta = element_incidence_matrix(c_values)
    A_tilde = nodal_analysis_coefficient_matrix(network, matrix_ops=matrix_ops, label_mappings=label_mappings)
    QS, QL = source_and_inductance_incidence_matrix(l_values)
    DQ = np.hstack((Delta.T, QL))
    Lambda = value_matrix(c_values, l_values)
    invLambda = matrix_ops.diag([1/L for L in matrix_ops.diag_vec(Lambda)]) # type: ignore

    inv_A_tilde = matrix_ops.inv(A_tilde)
    transformed_inv_A_tilde = DQ.T @ inv_A_tilde
    sorted_A_tilde = matrix_ops.inv(transformed_inv_A_tilde @ DQ)

    A = invLambda @ sorted_A_tilde
    C = transformed_inv_A_tilde.T @ sorted_A_tilde
    B = (-invLambda @ C.T) @ QS
    D = (inv_A_tilde - transformed_inv_A_tilde.T @ C.T) @ QS

    return A, B, C, D
