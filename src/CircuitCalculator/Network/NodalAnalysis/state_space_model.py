from ..network import Network
from . import labelmapper as map
from .node_analysis import create_node_matrix_from_network, create_source_incidence_matrix_from_network
import numpy as np
from dataclasses import dataclass
import itertools
from enum import Enum, auto
from .supernodes import SuperNodes, voltage_source_labels_to_next_reference

@dataclass(frozen=True)
class BranchValues:
    value: float
    id: str
    node1: str
    node2: str

class OutputType(Enum):
    VOLTAGE = auto()
    CURRENT = auto()
    POTENTIAL = auto()

@dataclass(frozen=True)
class Output:
    type: OutputType
    id: str

def create_element_incidence_matrix(values: list[BranchValues], node_mapping: dict[str, int]) -> np.ndarray:
    Delta = np.zeros((len(values), len(node_mapping)))
    for (k, value), (i_label, i) in itertools.product(enumerate(values), node_mapping.items()):
        if i_label == value.node1:
            Delta[k][i] = +1
        if i_label == value.node2:
            Delta[k][i] = -1
    return Delta

@dataclass(frozen=True)
class NodalStateSpaceModel:
    network: Network
    c_values: list[BranchValues]
    output_values: list[Output]
    node_index_mapper: map.NodeIndexMapper = map.default_node_mapper
    source_index_mapper: map.SourceIndexMapper = map.default_source_mapper

    @property
    def node_mapping(self) -> dict[str, int]:
        return self.node_index_mapper(self.network)

    def element_incidence_matrix(self, values: list[BranchValues]) -> np.ndarray:
        Delta = np.zeros((len(values), len(self.node_mapping)))
        for (k, value), (i_label, i) in itertools.product(enumerate(values), self.node_mapping.items()):
            if i_label == value.node1:
                Delta[k][i] = +1
            if i_label == value.node2:
                Delta[k][i] = -1
        return Delta

    @property
    def capacitor_incidence(self) -> np.ndarray:
        return self.element_incidence_matrix(self.c_values)

    @property
    def inv_Y(self) -> np.ndarray:
        return np.linalg.inv(create_node_matrix_from_network(network=self.network, node_index_mapper=self.node_index_mapper).real)

    @property
    def sorted_Y(self) -> np.ndarray:
        Delta = self.capacitor_incidence
        return np.linalg.inv(Delta@self.inv_Y@Delta.T)
    
    @property
    def A(self) -> np.ndarray:
        invC = np.diag([float(1/C.value) for C in self.c_values])
        return -invC@self.sorted_Y

    @property
    def B(self) -> np.ndarray:
        Q = create_source_incidence_matrix_from_network(
            network=self.network,
            node_index_mapper=self.node_index_mapper,
            source_index_mapper=self.source_index_mapper).real
        Delta = self.capacitor_incidence
        return -self.A@Delta@self.inv_Y@Q

    @property
    def C(self) -> np.ndarray:
        C_ = np.zeros((len(self.output_values), self.number_of_states))
        for i in range(C_.shape[0]):
            if self.output_values[i].type == OutputType.POTENTIAL:
                C_[i][:] = c_row_for_potential(self.output_values[i].id, self.network, self.node_index_mapper, self.source_index_mapper, self.c_values)
            if self.output_values[i].type == OutputType.VOLTAGE:
                v_id = self.output_values[i].id
                branch = self.network[v_id]
                c_pos = c_row_for_potential(branch.node1, self.network, self.node_index_mapper, self.source_index_mapper, self.c_values)
                c_neg = c_row_for_potential(branch.node2, self.network, self.node_index_mapper, self.source_index_mapper, self.c_values)
                C_[i][:] = c_pos - c_neg
            if self.output_values[i].type == OutputType.CURRENT:
                v_id = self.output_values[i].id
                branch = self.network[v_id]
                c_pos = c_row_for_potential(branch.node1, self.network, self.node_index_mapper, self.source_index_mapper, self.c_values)
                c_neg = c_row_for_potential(branch.node2, self.network, self.node_index_mapper, self.source_index_mapper, self.c_values)
                C_[i][:] = (c_pos - c_neg)/branch.element.Z
        return C_

    @property
    def D(self) -> np.ndarray:
        D_ = np.zeros((len(self.output_values), self.number_of_inputs))
        for i in range(D_.shape[0]):
            if self.output_values[i].type == OutputType.POTENTIAL:
                D_[i][:] = d_row_for_potential(self.output_values[i].id, self.network, self.node_index_mapper, self.source_index_mapper, self.c_values)
            if self.output_values[i].type == OutputType.VOLTAGE:
                v_id = self.output_values[i].id
                branch = self.network[v_id]
                d_pos = d_row_for_potential(branch.node1, self.network, self.node_index_mapper, self.source_index_mapper, self.c_values)
                d_neg = d_row_for_potential(branch.node2, self.network, self.node_index_mapper, self.source_index_mapper, self.c_values)
                D_[i][:] = d_pos - d_neg
            if self.output_values[i].type == OutputType.CURRENT:
                v_id = self.output_values[i].id
                branch = self.network[v_id]
                d_pos = d_row_for_potential(branch.node1, self.network, self.node_index_mapper, self.source_index_mapper, self.c_values)
                d_neg = d_row_for_potential(branch.node2, self.network, self.node_index_mapper, self.source_index_mapper, self.c_values)
                D_[i][:] = (d_pos - d_neg)/branch.element.Z
        return D_

    @property
    def state_labels(self) -> list[str]:
        return ['v_'+self.network.branches_between(C.node1, C.node2)[0].id for C in self.c_values]

    @property
    def input_labels(self) -> list[str]:
        return [label for label in self.source_index_mapper(self.network)]

    @property
    def number_of_states(self) -> int:
        return len(self.state_labels)

    @property
    def number_of_inputs(self) -> int:
        return len(self.input_labels)

def output_matrices(network: Network, c_values: list[BranchValues], node_index_mapper: map.NodeIndexMapper = map.default_node_mapper, source_index_mapper: map.SourceIndexMapper = map.default_source_mapper) -> tuple[np.ndarray, np.ndarray]:
    node_mapping = node_index_mapper(network)
    def element_incidence_matrix(values: list[BranchValues]) -> np.ndarray:
        Delta = np.zeros((len(values), len(node_mapping)))
        for (k, value), (i_label, i) in itertools.product(enumerate(values), node_mapping.items()):
            if i_label == value.node1:
                Delta[k][i] = +1
            if i_label == value.node2:
                Delta[k][i] = -1
        return Delta

    Delta = element_incidence_matrix(c_values)
    Q = create_source_incidence_matrix_from_network(
        network=network,
        node_index_mapper=node_index_mapper,
        source_index_mapper=source_index_mapper).real
    inv_Y = np.linalg.inv(create_node_matrix_from_network(network=network, node_index_mapper=node_index_mapper).real)
    sorted_Y = np.linalg.inv(Delta @ inv_Y @ Delta.T)

    C = inv_Y @ Delta.T @ sorted_Y
    D = inv_Y @ (Q-Delta.T @ sorted_Y @ Delta @ inv_Y @ Q)
    return C, D

def c_row_for_potential(node_id: str, network: Network, node_index_mapper: map.NodeIndexMapper = map.default_node_mapper, source_index_mapper: map.SourceIndexMapper = map.default_source_mapper, c_values: list[BranchValues]= []) -> np.ndarray:
    C, _ = output_matrices(network, c_values, node_index_mapper=node_index_mapper, source_index_mapper=source_index_mapper)
    node_mapping = node_index_mapper(network)
    if node_id in node_mapping.keys():
        idx = node_mapping[node_id]
        return C[:][idx]
    return np.zeros(C.shape[1])

def d_row_for_potential(node_id: str, network: Network, node_index_mapper: map.NodeIndexMapper = map.default_node_mapper, source_index_mapper: map.SourceIndexMapper = map.default_source_mapper, c_values: list[BranchValues]= []) -> np.ndarray:
    _, D = output_matrices(network, c_values, node_index_mapper=node_index_mapper, source_index_mapper=source_index_mapper)
    node_mapping = node_index_mapper(network)
    if node_id in node_mapping.keys():
        idx = node_mapping[node_id]
        return D[:][idx]
    if network.is_zero_node(node_id):
        return np.zeros(D.shape[1])
    source_indices = [source_index_mapper(network).index(source) for source in voltage_source_labels_to_next_reference(network, SuperNodes(network), node_id)]
    D = np.zeros(D.shape[1])
    D[source_indices] = 1
    return D