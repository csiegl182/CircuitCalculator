import numpy as np
import itertools
from dataclasses import dataclass
from .node_analysis import source_incidence_matrix, nodal_analysis_coefficient_matrix
from . import label_mapping as map
from ..elements import is_ideal_voltage_source
from ..network import Network
from ...SignalProcessing import state_space_model as sp

def state_space_matrices(network: Network, c_values: dict[str, float] = {}, l_values: dict[str, float] = {}, node_mapper: map.NetworkMapper = map.default_node_mapper, current_source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper, voltage_source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    def element_incidence_matrix(values: dict[str, float]) -> np.ndarray:
        node_mapping = node_mapper(network)
        Delta = np.zeros((len(values), node_mapping.N))
        for (k, value), (i_label) in itertools.product(enumerate(values), node_mapping):
            if i_label == network[value].node1:
                Delta[k][node_mapping(i_label)] = +1
            if i_label == network[value].node2:
                Delta[k][node_mapping(i_label)] = -1
        return np.hstack((Delta, np.zeros((Delta.shape[0], voltage_source_mapper(network).N))))
    def source_and_inductance_incidence_matrix(values: dict[str, float]) -> tuple[np.ndarray, np.ndarray]:
        voltage_source_mapping_all = voltage_source_mapper(network)
        source_mapping_all = map.default_source_mapper(network)
        Qi = source_incidence_matrix(network=network)
        Q = np.zeros((voltage_source_mapping_all.N, voltage_source_mapping_all.N), dtype=int)
        for i in voltage_source_mapping_all.values:
            Q[i][i] = 1
        Q = np.vstack((np.hstack( (Qi, np.zeros((Qi.shape[0], Q.shape[1]) ))),
                    np.hstack( (np.zeros((Q.shape[0], Qi.shape[1])), Q) )))
        QS = Q[:,[source_mapping_all[l] for l in source_mapping_all if l not in l_values]]
        QL = Q[:,[source_mapping_all[l] for l in source_mapping_all if l in l_values]]
        return QS, QL
    def value_matrix(c_values: dict[str, float], l_values: dict[str, float]) -> np.ndarray:
        return np.vstack((
            np.hstack(( np.diag([-C for C in c_values.values()]), np.zeros((len(c_values), len(l_values))) )),
            np.hstack(( np.zeros((len(l_values), len(c_values))), np.diag([L for L in l_values.values()]) ))
        ))

    Delta = element_incidence_matrix(c_values)
    A_tilde = nodal_analysis_coefficient_matrix(network).real
    QS, QL = source_and_inductance_incidence_matrix(l_values)
    DQ = np.hstack((Delta.T, QL))
    Lambda = value_matrix(c_values, l_values)
    invLambda = np.diag([1/L for L in np.diag(Lambda)])

    inv_A_tilde = np.linalg.inv(A_tilde)
    transformed_inv_A_tilde = DQ.T @ inv_A_tilde
    sorted_A_tilde = np.linalg.inv(transformed_inv_A_tilde @ DQ)

    A = invLambda @ sorted_A_tilde
    C = transformed_inv_A_tilde.T @ sorted_A_tilde
    B = (-invLambda @ C.T) @ QS
    D = (inv_A_tilde - transformed_inv_A_tilde.T @ C.T) @ QS

    return A, B, C, D

@dataclass(frozen=True)
class NodalStateSpaceModel(sp.StateSpaceModel):
    network: Network
    c_values: dict[str, float]
    l_values: dict[str, float]
    node_index_mapping: map.LabelMapping
    voltage_source_index_mapping: map.LabelMapping
    current_source_index_mapping: map.LabelMapping

    def _row_for_potential(self, node_id: str, matrix: np.ndarray) -> np.ndarray:
        if node_id in self.node_index_mapping:
            return matrix[:][self.node_index_mapping[node_id]:self.node_index_mapping[node_id]+1]
        return np.zeros((1,matrix.shape[1]))

    def c_row_for_potential(self, node_id: str) -> np.ndarray:
        return self._row_for_potential(node_id, self.C)

    def _one_vector(_, length: int, one_indices: list[int]) -> np.ndarray:
        vector = np.zeros(length)
        vector[one_indices] = 1
        return vector

    def c_row_voltage(self, branch_id: str) -> np.ndarray:
        branch = self.network[branch_id]
        c_pos = self.c_row_for_potential(branch.node1)
        c_neg = self.c_row_for_potential(branch.node2)
        return c_pos - c_neg

    def c_row_current(self, branch_id: str) -> np.ndarray:
        voltage_source_mapping = map.filter(self.voltage_source_index_mapping, lambda x: is_ideal_voltage_source(self.network[x].element))
        if branch_id in self.c_values:
            idx = list(self.c_values.keys()).index(branch_id)
            return self.c_values[branch_id]*self.A[idx][:]
        if branch_id in self.voltage_source_index_mapping:
            return self.C[voltage_source_mapping[branch_id]+self.node_index_mapping.N][:]
        if branch_id in self.current_source_index_mapping:
            return np.zeros(self.C.shape[1])
        branch = self.network[branch_id]
        c_pos = self.c_row_for_potential(branch.node1)
        c_neg = self.c_row_for_potential(branch.node2)
        return (c_pos - c_neg)/branch.element.Z

    def d_row_for_potential(self, node_id: str) -> np.ndarray:
        return self._row_for_potential(node_id, self.D)

    def d_row_voltage(self, branch_id: str) -> np.ndarray:
        branch = self.network[branch_id]
        d_pos = self.d_row_for_potential(branch.node1)
        d_neg = self.d_row_for_potential(branch.node2)
        return d_pos - d_neg

    def d_row_current(self, branch_id: str) -> np.ndarray:
        if branch_id in self.c_values:
            idx = list(self.c_values.keys()).index(branch_id)
            return self.c_values[branch_id]*self.B[idx][:]
        if branch_id in self.voltage_source_index_mapping:
            return self.D[self.voltage_source_index_mapping[branch_id]+self.node_index_mapping.N][:]
        if branch_id in self.current_source_index_mapping:
            d_row = np.zeros(self.D.shape[1])
            d_row[self.current_source_index_mapping[branch_id]] = 1
            return d_row
        branch = self.network[branch_id]
        d_pos = self.d_row_for_potential(branch.node1)
        d_neg = self.d_row_for_potential(branch.node2)
        return (d_pos - d_neg)/branch.element.Z

    @property
    def sources(self) -> list[str]:
        current_sources = self.current_source_index_mapping.keys
        voltage_sources = [vs for vs in self.voltage_source_index_mapping.keys if vs not in self.l_values]
        return current_sources+voltage_sources

def nodal_state_space_model(network: Network, c_values: dict[str, float] = {}, l_values: dict[str, float] = {}, node_index_mapper: map.NetworkMapper = map.default_node_mapper, voltage_source_index_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper, current_source_index_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper) -> NodalStateSpaceModel:
    A, B, C, D = state_space_matrices(
        network=network,
        c_values=c_values,
        l_values=l_values,
        node_mapper=node_index_mapper,
        voltage_source_mapper=voltage_source_index_mapper,
        current_source_mapper=current_source_index_mapper
    )
    return NodalStateSpaceModel(
        A=A, B=B, C=C, D=D,
        network=network,
        c_values=c_values,
        l_values=l_values,
        node_index_mapping=node_index_mapper(network),
        voltage_source_index_mapping=voltage_source_index_mapper(network),
        current_source_index_mapping=current_source_index_mapper(network),
    )