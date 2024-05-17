from .node_analysis import node_admittance_matrix, source_incidence_matrix, nodal_analysis_coefficient_matrix
from .supernodes import SuperNodes, voltage_source_labels_to_next_reference
from . import label_mapping as map
from ..network import Network
from ...SignalProcessing import state_space_model as sp
import numpy as np
import itertools
from dataclasses import dataclass

def state_space_matrices_for_potentials(network: Network, c_values: dict[str, float], node_mapper: map.NetworkMapper = map.default_node_mapper, current_source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper, voltage_source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    node_mapping = node_mapper(network)
    def element_incidence_matrix(values: dict[str, float]) -> np.ndarray:
        Delta = np.zeros((len(values), node_mapping.N))
        for (k, value), (i_label) in itertools.product(enumerate(values), node_mapping):
            if i_label == network[value].node1:
                Delta[k][node_mapping(i_label)] = +1
            if i_label == network[value].node2:
                Delta[k][node_mapping(i_label)] = -1
        return np.hstack((Delta, np.zeros((Delta.shape[0], voltage_source_mapper(network).N))))

    invC = np.diag([float(1/C) for C in c_values.values()])
    Delta = element_incidence_matrix(c_values)
    Qi = source_incidence_matrix(
         network=network,
         node_mapper=node_mapper,
         source_mapper=current_source_mapper).real
    Q = np.vstack((np.hstack((Qi, np.zeros((Qi.shape[0], voltage_source_mapper(network).N)))), np.hstack((np.zeros((1, Qi.shape[1])), np.eye(voltage_source_mapper(network).N)))))
    inv_Y = np.linalg.inv(nodal_analysis_coefficient_matrix(network=network, node_mapper=node_mapper).real)
    sorted_Y = np.linalg.inv(Delta @ inv_Y @ Delta.T)

    A = -invC @ sorted_Y
    B = -A @ Delta @ inv_Y @ Q
    C = inv_Y @ Delta.T @ sorted_Y
    D = inv_Y @ (Q-Delta.T @ sorted_Y @ Delta @ inv_Y @ Q)
    return A, B, C, D

@dataclass(frozen=True)
class NodalStateSpaceModel(sp.StateSpaceModel):
    network: Network
    c_values: dict[str, float]
    node_index_mapping: map.LabelMapping
    source_index_mapping: map.LabelMapping

    def c_row_for_potential(self, node_id: str) -> np.ndarray:
        if node_id in self.node_index_mapping:
            return self.C[:][self.node_index_mapping(node_id)]
        return np.zeros(self.C.shape[1])

    def c_row_voltage(self, branch_id: str) -> np.ndarray:
        branch = self.network[branch_id]
        c_pos = self.c_row_for_potential(branch.node1)
        c_neg = self.c_row_for_potential(branch.node2)
        return c_pos - c_neg

    def c_row_current(self, branch_id: str) -> np.ndarray:
        if branch_id in self.c_values:
            idx = list(self.c_values.keys()).index(branch_id)
            return self.c_values[branch_id]*self.A[idx][:]
        if branch_id in self.source_index_mapping:
            return self.C[self.source_index_mapping[branch_id]][:]
        branch = self.network[branch_id]
        c_pos = self.c_row_for_potential(branch.node1)
        c_neg = self.c_row_for_potential(branch.node2)
        return (c_pos - c_neg)/branch.element.Z

    def d_row_for_potential(self, node_id: str) -> np.ndarray:
        if node_id in self.node_index_mapping:
            return self.D[:][self.node_index_mapping(node_id)]
        if self.network.is_zero_node(node_id):
            return np.zeros(self.D.shape[1])
        source_indices = [self.source_index_mapping[source] for source in voltage_source_labels_to_next_reference(self.network, SuperNodes(self.network), node_id)]
        D = np.zeros(self.D.shape[1])
        D[source_indices] = 1
        return D

    def d_row_voltage(self, branch_id: str) -> np.ndarray:
        branch = self.network[branch_id]
        d_pos = self.d_row_for_potential(branch.node1)
        d_neg = self.d_row_for_potential(branch.node2)
        return d_pos - d_neg

    def d_row_current(self, branch_id: str) -> np.ndarray:
        if branch_id in self.c_values:
            idx = list(self.c_values.keys()).index(branch_id)
            return self.c_values[branch_id]*self.B[idx][:]
        if branch_id in self.source_index_mapping:
            D_ = np.zeros(self.n_inputs)
            D_[self.source_index_mapping[branch_id]] = 1
            return D_
        branch = self.network[branch_id]
        d_pos = self.d_row_for_potential(branch.node1)
        d_neg = self.d_row_for_potential(branch.node2)
        return (d_pos - d_neg)/branch.element.Z

def nodal_state_space_model(network: Network, c_values: dict[str, float], node_index_mapper: map.NetworkMapper = map.default_node_mapper, source_index_mapper: map.SourceIndexMapper = map.default_source_mapper) -> NodalStateSpaceModel:
    A, B, C, D = state_space_matrices_for_potentials(
        network=network,
        c_values=c_values,
        node_mapper=node_index_mapper,
        # source_mapper=source_index_mapper
    )
    return NodalStateSpaceModel(
        A=A, B=B, C=C, D=D,
        network=network,
        c_values=c_values,
        node_index_mapping=node_index_mapper(network),
        source_index_mapping=source_index_mapper(network),
    )