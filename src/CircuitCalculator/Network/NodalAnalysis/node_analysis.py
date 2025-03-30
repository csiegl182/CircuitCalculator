import numpy as np
import sympy as sp
from ..network import Network
from . import label_mapping as map
from .. import transformers as trf
import itertools
from typing import Protocol, Any, Callable, Mapping

Matrix = np.ndarray | sp.Matrix
symbolic = sp.core.symbol.Symbol

class DimensionError(Exception):
    ...

class MatrixElement(Protocol):
    def __init__(self, value: complex | symbolic) -> None: ...
    @property
    def value(self) -> Any: ...

    @property
    def isfinite(self) -> bool: ...

class NumericMatrixElement:
    def __init__(self, value: complex | symbolic) -> None:
        try:
            self._value = complex(value)
        except ValueError:
            self._value = np.nan

    @property
    def value(self) -> complex:
        return self._value

    @property
    def isfinite(self) -> bool:
        if np.isnan(self.value):
            return True
        return np.isfinite(self.value)

class SymbolicMatrixElement:
    def __init__(self, value: complex | symbolic) -> None:
        self._value = sp.sympify(value)

    @property
    def value(self) -> Any:
        return self._value

    @property
    def isfinite(self) -> bool:
        if self.value == sp.nan:
            return True
        if self.value.is_finite is None:
            return True
        return self.value.is_finite

class MatrixOperations(Protocol):
    matrix_inversion_exception: Any

    @staticmethod
    def zeros(shape: tuple[int, int]) -> Any: ...

    @staticmethod
    def nan(shape: tuple[int, int]) -> Any: ...

    @staticmethod
    def column_vector(values: list[complex | symbolic]) -> Any: ...

    @staticmethod
    def vstack(matrices: tuple[Any, ...]) -> Any: ...

    @staticmethod
    def hstack(matrices: tuple[Any, ...]) -> Any: ...
    
    @staticmethod
    def diag(values: list[complex | float | symbolic]) -> Any: ...

    @staticmethod
    def diag_vec(values: Any) -> list[complex | symbolic]: ...

    @staticmethod
    def inv(matrix: Any) -> Any: ...

    @staticmethod
    def solve(A: Any, b: Any) -> Any: ...

    @staticmethod
    def elm(value: complex | symbolic) -> MatrixElement: ...

    @staticmethod
    def shape(matrix: Any) -> tuple[int, int]: ...

    @staticmethod
    def contains_nan(matrix: Any) -> bool: ...

class NumPyMatrixOperations:
    matrix_inversion_exception = np.linalg.LinAlgError

    @staticmethod
    def zeros(shape: tuple[int, int]) -> np.ndarray:
        return np.zeros(shape, dtype=complex)

    @staticmethod
    def nan(shape: tuple[int, int]) -> np.ndarray:
        return np.full(shape, np.nan, dtype=complex)

    @staticmethod
    def column_vector(values: list[complex | symbolic]) -> Any:
        return np.array([NumericMatrixElement(v).value for v in values]).reshape(len(values), 1)

    @staticmethod
    def vstack(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
        return np.vstack(matrices)

    @staticmethod
    def hstack(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
        return np.hstack(matrices)

    @staticmethod
    def diag(values: list[complex | symbolic]) -> np.ndarray:
        return np.diag([NumericMatrixElement(v).value for v in values])

    @staticmethod
    def diag_vec(values: np.ndarray) -> list[complex | symbolic]:
        return [NumericMatrixElement(v).value for v in np.diag(values)]

    @staticmethod
    def inv(matrix: np.ndarray) -> np.ndarray:
        return np.linalg.inv(matrix)

    @staticmethod
    def solve(A: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.linalg.solve(A, b)

    @staticmethod
    def elm(value: complex | symbolic) -> NumericMatrixElement:
        return NumericMatrixElement(value)

    @staticmethod
    def shape(matrix: np.ndarray) -> tuple[int, int]:
        return (matrix.shape[0], matrix.shape[1])

    @staticmethod
    def contains_nan(matrix: np.ndarray) -> bool:
        return np.any(np.isnan(matrix)) == True

class SymPyMatrixOperations:
    matrix_inversion_exception = sp.matrices.common.NonInvertibleMatrixError

    @staticmethod
    def zeros(shape: tuple[int, int]) -> sp.Matrix:
        return sp.zeros(*shape)

    @staticmethod
    def nan(shape: tuple[int, int]) -> sp.Matrix:
        return sp.Matrix([[sp.nan] * shape[1]] * shape[0])

    @staticmethod
    def column_vector(values: list[complex | symbolic]) -> sp.Matrix:
        return sp.Matrix([[v] for v in values]).reshape(len(values), 1)

    @staticmethod
    def vstack(matrices: tuple[sp.Matrix, ...]) -> sp.Matrix:
        return sp.Matrix.vstack(*matrices)

    @staticmethod
    def hstack(matrices: tuple[sp.Matrix, ...]) -> sp.Matrix:
        return sp.Matrix.hstack(*[sp.Matrix(m) for m in matrices])

    @staticmethod
    def diag(values: list[complex | symbolic]) -> sp.Matrix:
        return sp.diag(*values)

    @staticmethod
    def diag_vec(values: sp.Matrix) -> list[complex | symbolic]:
        return list(values.diagonal())

    @staticmethod
    def inv(matrix: sp.Matrix) -> sp.Matrix:
        return sp.Matrix(matrix.inv())

    @staticmethod
    def solve(A: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
        return A.LUsolve(b)

    @staticmethod
    def elm(value: complex | symbolic) -> SymbolicMatrixElement:
        return SymbolicMatrixElement(value)

    @staticmethod
    def shape(matrix: sp.Matrix) -> tuple[int, int]:
        return (matrix.shape[0], matrix.shape[1])

    @staticmethod
    def contains_nan(matrix: sp.Matrix) -> bool:
        return False

def admittance_connected_to(network: Network, node: str, me: Callable[[Any], MatrixElement]) -> complex:
    return sum([e.value for e in [me(b.element.Y) for b in network.branches_connected_to(node)] if e.isfinite])

def admittance_between(network: Network, node1: str, node2: str, me: Callable[[Any], MatrixElement]) -> complex:
    return sum([e.value for e in [me(b.element.Y) for b in network.branches_between(node1, node2)] if e.isfinite])

def connected_nodes(network: Network, node: str) -> list[str]:
    return [b.node1 if b.node1 != node else b.node2 for b in network.branches_connected_to(node)]

def node_admittance_matrix(network: Network, matrix_ops: MatrixOperations = NumPyMatrixOperations(), node_index_mapper: map.NetworkMapper = map.default_node_mapper) -> Matrix:
    def node_matrix_element(i_label:str, j_label:str) -> complex:
        if i_label == j_label:
            return admittance_connected_to(no_voltage_sources_network, i_label, matrix_ops.elm)
        return -admittance_between(no_voltage_sources_network, i_label, j_label, matrix_ops.elm)
    node_mapping = node_index_mapper(network)
    no_voltage_sources_network = Network(branches=[b for b in network.branches if not b.element.is_ideal_voltage_source], node_zero_label=network.node_zero_label)
    Y = matrix_ops.zeros((node_mapping.N, node_mapping.N))
    for i_label, j_label in itertools.product(node_mapping, repeat=2):
        Y[node_mapping(i_label, j_label)] = node_matrix_element(i_label, j_label)
    return Y

def voltage_source_incidence_matrix(network: Network, node_mapper: map.NetworkMapper = map.default_node_mapper, source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper) -> Matrix:
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

def nodal_analysis_coefficient_matrix(network: Network, matrix_ops: MatrixOperations = NumPyMatrixOperations(), node_mapper: map.NetworkMapper = map.default_node_mapper, source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper) -> Matrix:
    Y = node_admittance_matrix(network, matrix_ops, node_mapper)
    B = voltage_source_incidence_matrix(network, node_mapper, source_mapper)
    Z = matrix_ops.zeros((B.shape[1], B.shape[1]))
    return matrix_ops.vstack((matrix_ops.hstack((Y, B)), matrix_ops.hstack((B.T, Z))))

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

def current_source_vector(network: Network, matrix_ops: MatrixOperations = NumPyMatrixOperations(), source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper) -> Matrix:
    cs_index = map.filter(source_mapper(network), lambda x: network[x].element.is_current_source)
    return matrix_ops.column_vector([network[x].element.I for x in cs_index.keys])

def current_source_incidence_vector(network: Network, matrix_ops: MatrixOperations = NumPyMatrixOperations(), node_mapper: map.NetworkMapper = map.default_node_mapper, source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper) -> np.ndarray:
    Q = source_incidence_matrix(network, node_mapper=node_mapper, source_mapper=source_mapper)
    Is = current_source_vector(network, matrix_ops=matrix_ops, source_mapper=source_mapper)
    return Q@Is

def nodal_analysis_constants_vector(network: Network, matrix_ops: MatrixOperations = NumPyMatrixOperations(), node_mapper: map.NetworkMapper = map.default_node_mapper, current_source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper, voltage_source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper) -> Matrix:
    I = current_source_incidence_vector(network, matrix_ops, node_mapper, current_source_mapper)

    vs_mapping = voltage_source_mapper(network)
    V = matrix_ops.column_vector([network[vs].element.V for vs in vs_mapping.keys])
    return matrix_ops.vstack((I, V))

def open_circuit_impedance(network: Network, node1: str, node2: str, node_index_mapper: map.NetworkMapper = map.default_node_mapper) -> complex:
    if node1 == node2:
        return 0
    if any([b.element.is_ideal_voltage_source for b in network.branches_between(node1, node2)]):
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

def state_space_matrices(network: Network, c_values: Mapping[str, float | symbolic] = {}, l_values: Mapping[str, float | symbolic] = {}, matrix_ops: MatrixOperations = NumPyMatrixOperations(), node_mapper: map.NetworkMapper = map.default_node_mapper, current_source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper, voltage_source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper) -> tuple[Matrix, Matrix, Matrix, Matrix]:
    def element_incidence_matrix(values: dict[str, float | symbolic]) -> np.ndarray:
        node_mapping = node_mapper(network)
        Delta = np.zeros((len(values), node_mapping.N))
        for (k, value), (i_label) in itertools.product(enumerate(values), node_mapping):
            if i_label == network[value].node1:
                Delta[k][node_mapping(i_label)] = +1
            if i_label == network[value].node2:
                Delta[k][node_mapping(i_label)] = -1
        return np.hstack((Delta, np.zeros((Delta.shape[0], voltage_source_mapper(network).N))))
    def source_and_inductance_incidence_matrix(values: dict[str, float | symbolic]) -> tuple[np.ndarray, np.ndarray]:
        voltage_source_mapping_all = voltage_source_mapper(network)
        source_mapping_all = map.default_source_mapper(network)
        Qi = source_incidence_matrix(network=network, node_mapper=node_mapper, source_mapper=current_source_mapper)
        Q = np.zeros((voltage_source_mapping_all.N, voltage_source_mapping_all.N), dtype=int)
        for i in voltage_source_mapping_all.values:
            Q[i][i] = 1
        Q = np.vstack((np.hstack( (Qi, np.zeros((Qi.shape[0], Q.shape[1]) ))),
                    np.hstack( (np.zeros((Q.shape[0], Qi.shape[1])), Q) )))
        QS = Q[:,[source_mapping_all[l] for l in source_mapping_all if l not in values]]
        QL = Q[:,[source_mapping_all[l] for l in source_mapping_all if l in values]]
        return QS, QL
    def value_matrix(c_values: dict[str, float | symbolic], l_values: dict[str, float | symbolic]) -> np.ndarray:
        return matrix_ops.vstack((
            matrix_ops.hstack(( matrix_ops.diag([-C for C in c_values.values()]), matrix_ops.zeros((len(c_values), len(l_values))) )), # type: ignore
            matrix_ops.hstack(( matrix_ops.zeros((len(l_values), len(c_values))), matrix_ops.diag([L for L in l_values.values()]) ))
        ))

    Delta = element_incidence_matrix(c_values)
    A_tilde = nodal_analysis_coefficient_matrix(network, matrix_ops=matrix_ops, node_mapper=node_mapper, source_mapper=voltage_source_mapper)
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

# TODO: this function is not used in the codebase: check and remove!
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
