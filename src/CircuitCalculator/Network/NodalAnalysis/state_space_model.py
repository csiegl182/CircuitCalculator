from ..network import Network
from . import label_mapping as map
from .node_analysis import create_node_matrix_from_network, create_source_incidence_matrix_from_network
import numpy as np
from dataclasses import dataclass
import itertools
from enum import Enum, auto
from .supernodes import SuperNodes, voltage_source_labels_to_next_reference
from ...SignalProcessing import state_space_model as sp

@dataclass(frozen=True)
class BranchValues:
    value: float
    id: str
    node1: str # TODO: are these properties necessary?
    node2: str

class OutputType(Enum):
    VOLTAGE = auto()
    CURRENT = auto()
    POTENTIAL = auto()

@dataclass(frozen=True)
class Output:
    type: OutputType
    id: str

def state_space_matrices_for_potentials(network: Network, c_values: list[BranchValues], node_index_mapper: map.NetworkMapper = map.default_node_mapper, source_index_mapper: map.SourceIndexMapper = map.default_source_mapper) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    node_mapping = node_index_mapper(network)
    def element_incidence_matrix(values: list[BranchValues]) -> np.ndarray:
        Delta = np.zeros((len(values), node_mapping.N))
        for (k, value), (i_label) in itertools.product(enumerate(values), node_mapping):
            if i_label == value.node1:
                Delta[k][node_mapping(i_label)] = +1
            if i_label == value.node2:
                Delta[k][node_mapping(i_label)] = -1
        return Delta

    invC = np.diag([float(1/C.value) for C in c_values])
    Delta = element_incidence_matrix(c_values)
    Q = create_source_incidence_matrix_from_network(
        network=network,
        node_index_mapper=node_index_mapper,
        source_index_mapper=source_index_mapper).real
    inv_Y = np.linalg.inv(create_node_matrix_from_network(network=network, node_index_mapper=node_index_mapper).real)
    sorted_Y = np.linalg.inv(Delta @ inv_Y @ Delta.T)

    A =  -invC @ sorted_Y
    B = -A @ Delta @ inv_Y @ Q
    C = inv_Y @ Delta.T @ sorted_Y
    D = inv_Y @ (Q-Delta.T @ sorted_Y @ Delta @ inv_Y @ Q)
    return A, B, C, D

@dataclass(frozen=True)
class NewNodalStateSpaceModel(sp.StateSpaceModel):
    network: Network
    c_values: list[BranchValues]
    node_index_mapping: map.LabelMapping
    source_index_mapping: map.LabelMapping

    def c_row_for_potential(self, node_id: str) -> np.ndarray:
        if node_id in self.node_index_mapping:
            idx = self.node_index_mapping[node_id]
            return self.C[:][idx]
        return np.zeros(self.C.shape[1])

    def c_row_voltage(self, branch_id: str) -> np.ndarray:
        branch = self.network[branch_id]
        c_pos = self.c_row_for_potential(branch.node1)
        c_neg = self.c_row_for_potential(branch.node2)
        return c_pos - c_neg

    def c_row_current(self, branch_id: str) -> np.ndarray:
        if branch_id in [c.id for c in self.c_values]:
            idx = [c.id for c in self.c_values].index(branch_id)
            C_ = self.c_values[idx].value*self.A[idx][:]
        else:
            branch = self.network[branch_id]
            c_pos = self.c_row_for_potential(branch.node1)
            c_neg = self.c_row_for_potential(branch.node2)
            C_ = (c_pos - c_neg)/branch.element.Z
        return C_

    def d_row_for_potential(self, node_id: str) -> np.ndarray:
        if node_id in self.node_index_mapping:
            idx = self.node_index_mapping[node_id]
            return self.D[:][idx]
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
        if branch_id in [c.id for c in self.c_values]:
            idx = [c.id for c in self.c_values].index(branch_id)
            D_ = self.c_values[idx].value*self.B[idx][:]
        else:
            if branch_id in self.source_index_mapping:
                D_ = np.zeros(self.n_inputs)
                D_[self.source_index_mapping[branch_id]] = 1
            else:
                branch = self.network[branch_id]
                d_pos = self.d_row_for_potential(branch.node1)
                d_neg = self.d_row_for_potential(branch.node2)
                D_ = (d_pos - d_neg)/branch.element.Z
        return D_

def nodal_state_space_model(network: Network, c_values: list[BranchValues], node_index_mapper: map.NetworkMapper = map.default_node_mapper, source_index_mapper: map.SourceIndexMapper = map.default_source_mapper) -> NewNodalStateSpaceModel:
    A, B, C, D = state_space_matrices_for_potentials(
        network=network,
        c_values=c_values,
        node_index_mapper=node_index_mapper,
        source_index_mapper=source_index_mapper
    )
    return NewNodalStateSpaceModel(
        A=A, B=B, C=C, D=D,
        network=network,
        c_values=c_values,
        node_index_mapping=node_index_mapper(network),
        source_index_mapping=source_index_mapper(network),
    )