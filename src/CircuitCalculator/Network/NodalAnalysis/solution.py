from typing import Any
from dataclasses import dataclass
from ..network import Network
from ..solution import NetworkSolution
from . import matrix_operations as mo
from . import label_mapping as map
from . import node_analysis as na

@dataclass(frozen=True)
class NodalAnalysisSolution:
    network: Network
    solution_vector: tuple
    label_mappings_factory: map.LabelMappingsFactory

    @property
    def label_mappings(self) -> map.NetworkLabelMappings:
        return self.label_mappings_factory(self.network)

    @property
    def _potentials(self) -> tuple:
        return tuple(self.solution_vector[i] for i in sorted(self.label_mappings.node_mapping.values))

    @property
    def _voltage_source_currents(self) -> tuple:
        all_indices = set(range(len(self.solution_vector)))
        remaining_indices = all_indices - set(self.label_mappings.node_mapping.values)
        return tuple(self.solution_vector[i] for i in sorted(remaining_indices))

    def _is_floating_node(self, node_id: str) -> bool:
        all_node_ids = {b.node1 for b in self.network.branches} | {b.node2 for b in self.network.branches}
        if node_id not in all_node_ids:
            raise KeyError(f"Node '{node_id}' not found in the network.")
        return node_id not in self.network.node_labels

    def _is_floating_branch(self, branch_id: str) -> bool:
        all_branch_ids = [b.id for b in self.network.branches]
        if branch_id not in all_branch_ids:
            raise KeyError(f"Branch '{branch_id}' not found in the network.")
        return branch_id not in self.network.branch_ids

    def get_potential(self, node_id: str) -> complex:
        if self._is_floating_node(node_id):
            return float('nan')
        if node_id == self.network.reference_node_label:
            return 0
        return self._potentials[self.label_mappings.node_mapping[node_id]]

    def get_current(self, branch_id: str) -> complex:
        if self._is_floating_branch(branch_id):
            return float('nan')
        if branch_id in self.label_mappings.voltage_source_mapping.keys:
            return self._voltage_source_currents[self.label_mappings.voltage_source_mapping[branch_id]]
        if self.network[branch_id].element.is_ideal_current_source:
            return complex(self.network[branch_id].element.I)
        if self.network[branch_id].element.is_current_source:
            return - (self.network[branch_id].element.I + self.get_voltage(branch_id)/self.network[branch_id].element.Z)
        branch = self.network[branch_id]
        return self.get_voltage(branch_id)/branch.element.Z

    def get_voltage(self, branch_id: str) -> Any:
        if self._is_floating_branch(branch_id):
            return float('nan')
        phi1 = self.get_potential(self.network[branch_id].node1)
        phi2 = self.get_potential(self.network[branch_id].node2)
        return phi1-phi2

    def get_power(self, branch_id: str) -> Any:
        return self.get_voltage(branch_id)*self.get_current(branch_id).conjugate()

def numeric_nodal_analysis_bias_point_solution(network: Network, label_mappings_factory: map.LabelMappingsFactory = map.default_label_mappings_factory) -> NetworkSolution:
        return NodalAnalysisSolution(
            network=network,
            solution_vector=na.nodal_analysis_solution(network, matrix_ops=mo.NumPyMatrixOperations(), label_mappings_factory=label_mappings_factory),
            label_mappings_factory=label_mappings_factory
        )

def symbolic_nodal_analysis_bias_point_solution(network: Network, label_mappings_factory: map.LabelMappingsFactory = map.default_label_mappings_factory) -> NetworkSolution:
        return NodalAnalysisSolution(
            network=network,
            solution_vector=na.nodal_analysis_solution(network, matrix_ops=mo.SymPyMatrixOperations(), label_mappings_factory=label_mappings_factory),
            label_mappings_factory=label_mappings_factory
        )