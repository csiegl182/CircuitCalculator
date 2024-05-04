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
        Delta = self.capacitor_incidence
        some_C = self.inv_Y @ Delta.T @ self.sorted_Y

        sn = SuperNodes(self.network)
        node_mapping = self.node_mapping
        C_ = np.zeros((len(self.output_values), some_C.shape[1]))
        for i in range(C_.shape[0]):
            if self.output_values[i].type == OutputType.POTENTIAL:
                if self.output_values[i].id in node_mapping.keys():
                    node_id = self.output_values[i].id
                    idx = node_mapping[node_id]
                    C_[i][:] = some_C[:][idx]
            if self.output_values[i].type == OutputType.VOLTAGE:
                v_id = self.output_values[i].id
                branch = self.network[v_id]
                i1 = self.node_index_mapper(self.network)[branch.node1]
                i2 = self.node_index_mapper(self.network)[branch.node2]
                C_[i][i1] = 1
                C_[i][i2] = -1
        return C_

    @property
    def D(self) -> np.ndarray:
        node_mapping = self.node_mapping
        Q = create_source_incidence_matrix_from_network(
            network=self.network,
            node_index_mapper=self.node_index_mapper,
            source_index_mapper=self.source_index_mapper).real
        Delta = self.capacitor_incidence
        some_D = self.inv_Y@(Q-Delta.T@self.sorted_Y@Delta@self.inv_Y@Q)
        D_ = np.zeros((len(self.output_values), some_D.shape[1]))
        for i in range(D_.shape[0]):
            if self.output_values[i].type == OutputType.POTENTIAL:
                if self.output_values[i].id in node_mapping.keys():
                    node_id = self.output_values[i].id
                    idx = node_mapping[node_id]
                    D_[i][:] = some_D[:][idx]
                else:
                    source_indices = [self.source_index_mapper(self.network).index(source) for source in voltage_source_labels_to_next_reference(self.network, SuperNodes(self.network), self.output_values[i].id)]
                    D_[i][source_indices] = 1
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