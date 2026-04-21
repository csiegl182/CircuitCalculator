import numpy as np
import itertools
from typing import Any, Callable
from ..network import Branch, Network
from . import matrix_operations as mo
from .. import transformers as trf
from .label_mapping import NetworkLabelMappings

class DimensionError(Exception):
    ...


class InvalidControlledSource(Exception):
    ...


def node_index(
    network: Network,
    label_mappings: NetworkLabelMappings,
    node: str,
    role: str = "Node",
) -> int | None:
    if node == network.reference_node_label:
        return None
    try:
        return label_mappings.node_mapping[node]
    except KeyError as e:
        raise InvalidControlledSource(f"{role} '{node}' is not connected to the network.") from e


def output_nodes(branch: Branch) -> tuple[tuple[str, int], tuple[str, int]]:
    return ((branch.node1, 1), (branch.node2, -1))


def is_norten_thevenin_element(element: Any) -> bool:
    return all(hasattr(element, attribute) for attribute in ('Z', 'Y', 'V', 'I'))


def add_branch_voltage_terms(
    node_terms: dict[str, mo.MatrixElement],
    branch: Branch,
    coefficient: mo.MatrixElement,
    matrix_ops: mo.MatrixOperations,
) -> None:
    for node, sign in output_nodes(branch):
        node_terms[node] = matrix_ops.elm(node_terms.get(node, matrix_ops.elm(0)).value + sign*coefficient.value)


def branch_current_terms(
    network: Network,
    matrix_ops: mo.MatrixOperations,
    label_mappings: NetworkLabelMappings,
    branch_id: str,
) -> tuple[dict[str, mo.MatrixElement], dict[str, mo.MatrixElement], mo.MatrixElement]:
    try:
        branch = network[branch_id]
    except (KeyError, ValueError) as e:
        raise InvalidControlledSource(f"Control branch '{branch_id}' does not exist.") from e

    node_terms: dict[str, mo.MatrixElement] = {}
    voltage_source_terms: dict[str, mo.MatrixElement] = {}
    constant = matrix_ops.elm(0)

    if branch_id in label_mappings.voltage_source_mapping.keys:
        voltage_source_terms[branch_id] = matrix_ops.elm(1)
        return node_terms, voltage_source_terms, constant

    element = branch.element
    if not is_norten_thevenin_element(element):
        raise InvalidControlledSource(f"Control branch '{branch_id}' must be a Norten/Thevenin element.")
    if element.is_ideal_current_source:
        return node_terms, voltage_source_terms, matrix_ops.elm(element.I)
    if element.is_current_source:
        add_branch_voltage_terms(
            node_terms,
            branch,
            matrix_ops.elm(-element.Y),
            matrix_ops,
        )
        return node_terms, voltage_source_terms, matrix_ops.elm(-element.I)

    admittance = matrix_ops.elm(getattr(element, 'Y', 0))
    if not admittance.isfinite:
        raise InvalidControlledSource(f"Control branch '{branch_id}' current cannot be expressed by nodal analysis.")
    add_branch_voltage_terms(node_terms, branch, admittance, matrix_ops)
    return node_terms, voltage_source_terms, constant


def admittance_connected_to(network: Network, node: str, me: Callable[[Any], mo.MatrixElement]) -> complex:
    admittances = [me(getattr(b.element, 'Y', 0)) for b in network.branches_connected_to(node)]
    return sum([e.value for e in admittances if e.isfinite])


def admittance_between(network: Network, node1: str, node2: str, me: Callable[[Any], mo.MatrixElement]) -> complex:
    admittances = [me(getattr(b.element, 'Y', 0)) for b in network.branches_between(node1, node2)]
    return sum([e.value for e in admittances if e.isfinite])


def voltage_controlled_current_source_matrix(
    network: Network,
    matrix_ops: mo.MatrixOperations,
    label_mappings: NetworkLabelMappings,
) -> mo.Matrix:
    def stamp(source: Branch) -> None:
        transconductance = matrix_ops.elm(source.element.transconductance).value
        control_nodes = ((source.element.control_node1, 1), (source.element.control_node2, -1))
        for output_node, output_sign in output_nodes(source):
            row = node_index(network, label_mappings, output_node)
            if row is None:
                continue
            for control_node, control_sign in control_nodes:
                column = node_index(network, label_mappings, control_node, "Control node")
                if column is None:
                    continue
                Y[row, column] += output_sign*control_sign*transconductance

    node_mapping = label_mappings.node_mapper(network)
    Y = matrix_ops.zeros((node_mapping.N, node_mapping.N))
    for branch in network.branches:
        if branch.element.is_voltage_controlled_current_source:
            stamp(branch)
    return Y


def current_controlled_current_source_incidence_matrix(
    network: Network,
    matrix_ops: mo.MatrixOperations,
    label_mappings: NetworkLabelMappings,
) -> mo.Matrix:
    def stamp(source: Branch) -> None:
        current_gain = matrix_ops.elm(source.element.current_gain).value
        _, voltage_source_terms, _ = branch_current_terms(
            network,
            matrix_ops,
            label_mappings,
            source.element.control_branch,
        )
        for output_node, output_sign in output_nodes(source):
            row = node_index(network, label_mappings, output_node)
            if row is None:
                continue
            for voltage_source, coefficient in voltage_source_terms.items():
                column = label_mappings.voltage_source_mapping[voltage_source]
                B[row, column] += output_sign*current_gain*coefficient.value

    node_mapping = label_mappings.node_mapper(network)
    B = matrix_ops.zeros((node_mapping.N, label_mappings.voltage_source_mapping.N))
    for branch in network.branches:
        if branch.element.is_current_controlled_current_source:
            stamp(branch)
    return B


def current_controlled_current_source_admittance_matrix(
    network: Network,
    matrix_ops: mo.MatrixOperations,
    label_mappings: NetworkLabelMappings,
) -> mo.Matrix:
    def stamp(source: Branch) -> None:
        current_gain = matrix_ops.elm(source.element.current_gain).value
        node_terms, _, _ = branch_current_terms(
            network,
            matrix_ops,
            label_mappings,
            source.element.control_branch,
        )
        for output_node, output_sign in output_nodes(source):
            row = node_index(network, label_mappings, output_node)
            if row is None:
                continue
            for node, coefficient in node_terms.items():
                column = node_index(network, label_mappings, node)
                if column is None:
                    continue
                Y[row, column] += output_sign*current_gain*coefficient.value

    node_mapping = label_mappings.node_mapper(network)
    Y = matrix_ops.zeros((node_mapping.N, node_mapping.N))
    for branch in network.branches:
        if branch.element.is_current_controlled_current_source:
            stamp(branch)
    return Y


def current_controlled_current_source_vector(
    network: Network,
    matrix_ops: mo.MatrixOperations,
    label_mappings: NetworkLabelMappings,
) -> mo.Matrix:
    def stamp(source: Branch) -> None:
        current_gain = matrix_ops.elm(source.element.current_gain).value
        _, _, constant = branch_current_terms(
            network,
            matrix_ops,
            label_mappings,
            source.element.control_branch,
        )
        for output_node, output_sign in output_nodes(source):
            row = node_index(network, label_mappings, output_node)
            if row is None:
                continue
            I[row, 0] += -output_sign*current_gain*constant.value

    node_mapping = label_mappings.node_mapper(network)
    I = matrix_ops.zeros((node_mapping.N, 1))
    for branch in network.branches:
        if branch.element.is_current_controlled_current_source:
            stamp(branch)
    return I


def voltage_controlled_voltage_source_constraint_matrix(
    network: Network,
    matrix_ops: mo.MatrixOperations,
    label_mappings: NetworkLabelMappings,
) -> mo.Matrix:
    def stamp(source: Branch) -> None:
        voltage_gain = matrix_ops.elm(source.element.voltage_gain).value
        row = label_mappings.voltage_source_mapping[source.id]
        control_nodes = ((source.element.control_node1, 1), (source.element.control_node2, -1))
        for control_node, control_sign in control_nodes:
            column = node_index(network, label_mappings, control_node, "Control node")
            if column is None:
                continue
            A[row, column] += -control_sign*voltage_gain

    A = matrix_ops.zeros((label_mappings.voltage_source_mapping.N, label_mappings.node_mapping.N))
    for branch in network.branches:
        if branch.element.is_voltage_controlled_voltage_source:
            stamp(branch)
    return A


def current_controlled_voltage_source_constraint_matrix(
    network: Network,
    matrix_ops: mo.MatrixOperations,
    label_mappings: NetworkLabelMappings,
) -> tuple[mo.Matrix, mo.Matrix]:
    def stamp(source: Branch) -> None:
        transresistance = matrix_ops.elm(source.element.transresistance).value
        node_terms, voltage_source_terms, _ = branch_current_terms(
            network,
            matrix_ops,
            label_mappings,
            source.element.control_branch,
        )
        row = label_mappings.voltage_source_mapping[source.id]
        for node, coefficient in node_terms.items():
            column = node_index(network, label_mappings, node)
            if column is None:
                continue
            A[row, column] += -transresistance*coefficient.value
        for voltage_source, coefficient in voltage_source_terms.items():
            column = label_mappings.voltage_source_mapping[voltage_source]
            Z[row, column] += -transresistance*coefficient.value

    A = matrix_ops.zeros((label_mappings.voltage_source_mapping.N, label_mappings.node_mapping.N))
    Z = matrix_ops.zeros((label_mappings.voltage_source_mapping.N, label_mappings.voltage_source_mapping.N))
    for branch in network.branches:
        if branch.element.is_current_controlled_voltage_source:
            stamp(branch)
    return A, Z


def current_controlled_voltage_source_vector(
    network: Network,
    matrix_ops: mo.MatrixOperations,
    label_mappings: NetworkLabelMappings,
) -> mo.Matrix:
    def stamp(source: Branch) -> None:
        transresistance = matrix_ops.elm(source.element.transresistance).value
        _, _, constant = branch_current_terms(
            network,
            matrix_ops,
            label_mappings,
            source.element.control_branch,
        )
        row = label_mappings.voltage_source_mapping[source.id]
        V[row, 0] += transresistance*constant.value

    V = matrix_ops.zeros((label_mappings.voltage_source_mapping.N, 1))
    for branch in network.branches:
        if branch.element.is_current_controlled_voltage_source:
            stamp(branch)
    return V


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
    return (
        Y
        + voltage_controlled_current_source_matrix(network, matrix_ops, label_mappings)
        + current_controlled_current_source_admittance_matrix(network, matrix_ops, label_mappings)
    )

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

def nodal_analysis_coefficient_matrix(
    network: Network,
    matrix_ops: mo.MatrixOperations,
    label_mappings: NetworkLabelMappings,
) -> mo.Matrix:
    Y = node_admittance_matrix(network, matrix_ops, label_mappings)
    B = voltage_source_incidence_matrix(network, matrix_ops, label_mappings)
    B_top = B + current_controlled_current_source_incidence_matrix(
        network,
        matrix_ops,
        label_mappings,
    )
    A_vcvs = voltage_controlled_voltage_source_constraint_matrix(network, matrix_ops, label_mappings)
    A_ccvs, Z_ccvs = current_controlled_voltage_source_constraint_matrix(network, matrix_ops, label_mappings)
    Z = matrix_ops.zeros((B.shape[1], B.shape[1])) + Z_ccvs
    return matrix_ops.vstack((
        matrix_ops.hstack((Y, B_top)),
        matrix_ops.hstack((B.T + A_vcvs + A_ccvs, Z)),
    ))

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
    I = (
        current_source_incidence_vector(network, matrix_ops, label_mappings)
        + current_controlled_current_source_vector(network, matrix_ops, label_mappings)
    )
    V = matrix_ops.column_vector([
        network[vs].element.V if not network[vs].element.is_controlled_voltage_source else 0
        for vs in label_mappings.voltage_source_mapping.keys
    ])
    V = V + current_controlled_voltage_source_vector(network, matrix_ops, label_mappings)
    return matrix_ops.vstack((I, V))
