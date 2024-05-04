from ..network import Network
from . import labelmapper as map
from .node_analysis import create_node_matrix_from_network, create_source_incidence_matrix_from_network
import numpy as np
from dataclasses import dataclass
import itertools

@dataclass(frozen=True)
class BranchValues:
    value: float
    id: str
    node1: str
    node2: str

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
        return self.inv_Y@Delta.T@self.sorted_Y

    @property
    def D(self) -> np.ndarray:
        Q = create_source_incidence_matrix_from_network(
            network=self.network,
            node_index_mapper=self.node_index_mapper,
            source_index_mapper=self.source_index_mapper).real
        Delta = self.capacitor_incidence
        return self.inv_Y@(Q-Delta.T@self.sorted_Y@Delta@self.inv_Y@Q)

    @property
    def state_labels(self) -> list[str]:
        return ['v_'+self.network.branches_between(C.node1, C.node2)[0].id for C in self.c_values]

    @property
    def input_labels(self) -> list[str]:
        return []