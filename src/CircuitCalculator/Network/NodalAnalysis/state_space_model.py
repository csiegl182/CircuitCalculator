from typing import Mapping
from .node_analysis import state_space_matrices
from . import label_mapping as map
from ..network import Network
from . import matrix_operations as mo
from .matrix_operations import symbolic

class StateSpaceGenericOutput:
    def __init__(self, network: Network, c_values: Mapping[str, float | symbolic], l_values: Mapping[str, float | symbolic], matrix_ops: mo.MatrixOperations, label_mappings_factory: map.LabelMappingsFactory):
        self.network = network
        self.c_values = c_values
        self.l_values = l_values
        self.matrix_ops = matrix_ops
        self.A, self.B, self.C, self.D = state_space_matrices(
            network=self.network,
            c_values=self.c_values,
            l_values=self.l_values,
            matrix_ops=self.matrix_ops,
            label_mappings_factory=label_mappings_factory
        )
        self._node_label_mapping = label_mappings_factory(self.network).node_mapping
        self._voltage_source_label_mapping = label_mappings_factory(self.network).voltage_source_mapping
        self._current_source_label_mapping = label_mappings_factory(self.network).current_source_mapping

    def _row_for_potential(self, node_id: str, matrix: mo.Matrix) -> mo.Matrix:
        if node_id in self._node_label_mapping:
            return matrix[self._node_label_mapping[node_id]:self._node_label_mapping[node_id]+1, :] # type: ignore
        return self.matrix_ops.zeros((1, matrix.shape[1]))

    def c_row_for_potential(self, node_id: str) -> mo.Matrix:
        return self._row_for_potential(node_id, self.C)

    def c_row_voltage(self, branch_id: str) -> mo.Matrix:
        branch = self.network[branch_id]
        c_pos = self.c_row_for_potential(branch.node1)
        c_neg = self.c_row_for_potential(branch.node2)
        return c_pos - c_neg

    def c_row_current(self, branch_id: str) -> mo.Matrix:
        voltage_source_mapping = self._voltage_source_label_mapping.filter_keys(lambda x: self.network[x].element.is_ideal_voltage_source)
        if branch_id in self.c_values:
            idx = list(self.c_values.keys()).index(branch_id)
            return self.c_values[branch_id] * self.A[idx, :] # type: ignore
        if branch_id in self._voltage_source_label_mapping:
            return self.C[voltage_source_mapping[branch_id] + self._node_label_mapping.N, :] # type: ignore
        if branch_id in self._current_source_label_mapping:
            return self.matrix_ops.zeros((1, self.C.shape[1]))
        branch = self.network[branch_id]
        c_pos = self.c_row_for_potential(branch.node1)
        c_neg = self.c_row_for_potential(branch.node2)
        return (c_pos - c_neg) / branch.element.Z

    def d_row_for_potential(self, node_id: str) -> mo.Matrix:
        return self._row_for_potential(node_id, self.D)

    def d_row_voltage(self, branch_id: str) -> mo.Matrix:
        branch = self.network[branch_id]
        d_pos = self.d_row_for_potential(branch.node1)
        d_neg = self.d_row_for_potential(branch.node2)
        return d_pos - d_neg

    def d_row_current(self, branch_id: str) -> mo.Matrix:
        if branch_id in self.c_values:
            idx = list(self.c_values.keys()).index(branch_id)
            return self.c_values[branch_id] * self.B[idx, :] # type: ignore
        if branch_id in self._voltage_source_label_mapping:
            return self.D[self._voltage_source_label_mapping[branch_id] + self._node_label_mapping.N, :] # type: ignore
        if branch_id in self._current_source_label_mapping:
            d_row = self.matrix_ops.zeros((1, self.D.shape[1]))
            d_row[0, self._current_source_label_mapping[branch_id]] = 1
            return d_row
        branch = self.network[branch_id]
        d_pos = self.d_row_for_potential(branch.node1)
        d_neg = self.d_row_for_potential(branch.node2)
        return (d_pos - d_neg) / branch.element.Z

    def extend_C_matrix(self, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> mo.Matrix:
        extended_C = self.matrix_ops.zeros((0, self.C.shape[1]))
        for id in potential_nodes:
            extended_C = self.matrix_ops.vstack((extended_C, self.c_row_for_potential(id)))
        for id in voltage_ids:
            extended_C = self.matrix_ops.vstack((extended_C, self.c_row_voltage(id)))
        for id in current_ids:
            extended_C = self.matrix_ops.vstack((extended_C, self.c_row_current(id)))
        return extended_C

    def extend_D_matrix(self, potential_nodes: list[str] = [], voltage_ids: list[str] = [], current_ids: list[str] = []) -> mo.Matrix:
        extended_D = self.matrix_ops.zeros((0, self.D.shape[1]))
        for id in potential_nodes:
            extended_D = self.matrix_ops.vstack((extended_D, self.d_row_for_potential(id)))
        for id in voltage_ids:
            extended_D = self.matrix_ops.vstack((extended_D, self.d_row_voltage(id)))
        for id in current_ids:
            extended_D = self.matrix_ops.vstack((extended_D, self.d_row_current(id)))
        return extended_D

    def sources(self) -> list[str]:
        current_sources = self._current_source_label_mapping.keys
        voltage_sources = [vs for vs in self._voltage_source_label_mapping.keys if vs not in self.l_values]
        return current_sources + voltage_sources

# def numeric_state_space_model(network: Network, c_values: Mapping[str, float], l_values: Mapping[str, float], node_index_mapper: map.NetworkMapper = map.default_node_mapper, voltage_source_index_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper, current_source_index_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper) -> StateSpaceGenericOutput:
def numeric_state_space_model(network: Network, c_values: Mapping[str, float], l_values: Mapping[str, float], label_mappings_factory: map.LabelMappingsFactory = map.default_label_mappings_factory) -> StateSpaceGenericOutput:
    return StateSpaceGenericOutput(
        network=network,
        c_values=c_values,
        l_values=l_values,
        matrix_ops=mo.NumPyMatrixOperations(),
        label_mappings_factory=label_mappings_factory
    )

# def symbolic_state_space_model(network: Network, c_values: Mapping[str, symbolic], l_values: Mapping[str, symbolic], node_index_mapper: map.NetworkMapper = map.default_node_mapper, voltage_source_index_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper, current_source_index_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper) -> StateSpaceGenericOutput:
def symbolic_state_space_model(network: Network, c_values: Mapping[str, symbolic], l_values: Mapping[str, symbolic], label_mappings_factory: map.LabelMappingsFactory = map.default_label_mappings_factory) -> StateSpaceGenericOutput:
    return StateSpaceGenericOutput(
        network=network,
        c_values=c_values,
        l_values=l_values,
        matrix_ops=mo.SymPyMatrixOperations(),
        label_mappings_factory=label_mappings_factory
    )
