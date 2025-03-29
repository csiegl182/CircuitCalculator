import numpy as np
from .node_analysis import state_space_matrices
from . import label_mapping as map
from ..network import Network

class StateSpaceOutput:
    def __init__(self, network: Network, c_values: dict[str, float], l_values: dict[str, float], node_index_mapper: map.NetworkMapper, voltage_source_index_mapper: map.SourceIndexMapper, current_source_index_mapper: map.SourceIndexMapper):
        self.network = network
        self.c_values = c_values
        self.l_values = l_values
        self.A, self.B, self.C, self.D = state_space_matrices(
            network=self.network,
            c_values=self.c_values,
            l_values=self.l_values,
            node_mapper=node_index_mapper,
            voltage_source_mapper=voltage_source_index_mapper,
            current_source_mapper=current_source_index_mapper
        )
        self._node_label_mapping = node_index_mapper(self.network)
        self._voltage_source_label_mapping = voltage_source_index_mapper(self.network)
        self._current_source_label_mapping = current_source_index_mapper(self.network)

    def _row_for_potential(self, node_id: str, matrix: np.ndarray) -> np.ndarray:
        if node_id in self._node_label_mapping:
            return matrix[:][self._node_label_mapping[node_id]:self._node_label_mapping[node_id]+1]
        return np.zeros((1, matrix.shape[1]))

    def c_row_for_potential(self, node_id: str) -> np.ndarray:
        return self._row_for_potential(node_id, self.C)

    def c_row_voltage(self, branch_id: str) -> np.ndarray:
        branch = self.network[branch_id]
        c_pos = self.c_row_for_potential(branch.node1)
        c_neg = self.c_row_for_potential(branch.node2)
        return c_pos - c_neg

    def c_row_current(self, branch_id: str) -> np.ndarray:
        voltage_source_mapping = map.filter(self._voltage_source_label_mapping, lambda x: self.network[x].element.is_ideal_voltage_source)
        if branch_id in self.c_values:
            idx = list(self.c_values.keys()).index(branch_id)
            return self.c_values[branch_id] * self.A[idx][:]
        if branch_id in self._voltage_source_label_mapping:
            return self.C[voltage_source_mapping[branch_id] + self._node_label_mapping.N][:]
        if branch_id in self._current_source_label_mapping:
            return np.zeros(self.C.shape[1])
        branch = self.network[branch_id]
        c_pos = self.c_row_for_potential(branch.node1)
        c_neg = self.c_row_for_potential(branch.node2)
        return (c_pos - c_neg) / branch.element.Z

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
            return self.c_values[branch_id] * self.B[idx][:]
        if branch_id in self._voltage_source_label_mapping:
            return self.D[self._voltage_source_label_mapping[branch_id] + self._node_label_mapping.N][:]
        if branch_id in self._current_source_label_mapping:
            d_row = np.zeros(self.D.shape[1])
            d_row[self._current_source_label_mapping[branch_id]] = 1
            return d_row
        branch = self.network[branch_id]
        d_pos = self.d_row_for_potential(branch.node1)
        d_neg = self.d_row_for_potential(branch.node2)
        return (d_pos - d_neg) / branch.element.Z

    def extend_C_matrix(self, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> np.ndarray:
        extended_C = np.ndarray(shape=(0, self.C.shape[1]))
        for id in potential_nodes:
            extended_C = np.vstack([extended_C, self.c_row_for_potential(id)])
        for id in voltage_ids:
            extended_C = np.vstack([extended_C, self.c_row_voltage(id)])
        for id in current_ids:
            extended_C = np.vstack([extended_C, self.c_row_current(id)])
        return extended_C

    def extend_D_matrix(self, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> np.ndarray:
        extended_D = np.ndarray(shape=(0, self.D.shape[1]))
        for id in potential_nodes:
            extended_D = np.vstack([extended_D, self.d_row_for_potential(id)])
        for id in voltage_ids:
            extended_D = np.vstack([extended_D, self.d_row_voltage(id)])
        for id in current_ids:
            extended_D = np.vstack([extended_D, self.d_row_current(id)])
        return extended_D

    def sources(self) -> list[str]:
        current_sources = self._current_source_label_mapping.keys
        voltage_sources = [vs for vs in self._voltage_source_label_mapping.keys if vs not in self.l_values]
        return current_sources + voltage_sources


def numeric_state_space_model(network: Network, c_values: dict[str, float], l_values: dict[str, float], node_index_mapper: map.NetworkMapper = map.default_node_mapper, voltage_source_index_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper, current_source_index_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper) -> StateSpaceOutput:
    return StateSpaceOutput(
        network=network,
        c_values=c_values,
        l_values=l_values,
        node_index_mapper=node_index_mapper,
        voltage_source_index_mapper=voltage_source_index_mapper,
        current_source_index_mapper=current_source_index_mapper
    )
