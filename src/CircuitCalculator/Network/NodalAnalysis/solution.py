from typing import Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from ..network import Network
from . import label_mapping as map
from .. import matrix_operations as mo
from . import node_analysis as na

@dataclass
class NodalAnalysisSolution(ABC):
    network: Network
    solution_vector: tuple
    label_mappings: map.NetworkLabelMappings

    @property
    def _potentials(self) -> tuple:
        return tuple(self.solution_vector[i] for i in sorted(self.label_mappings.node_mapping.values))

    @property
    def _voltage_source_currents(self) -> tuple:
        all_indices = set(range(len(self.solution_vector)))
        remaining_indices = all_indices - set(self.label_mappings.node_mapping.values)
        return tuple(self.solution_vector[i] for i in sorted(remaining_indices))

    @abstractmethod
    def get_potential(self, node_id: str) -> Any:
        ...

    @abstractmethod
    def get_current(self, branch_id: str) -> Any:
        ...

    def get_voltage(self, branch_id: str) -> Any:
        phi1 = self.get_potential(self.network[branch_id].node1)
        phi2 = self.get_potential(self.network[branch_id].node2)
        return phi1-phi2

    def get_power(self, branch_id: str) -> Any:
        return self.get_voltage(branch_id)*self.get_current(branch_id).conjugate()

@dataclass
class NumericNodalAnalysisSolution(NodalAnalysisSolution):
    matrix_ops: mo.MatrixOperations = mo.NumPyMatrixOperations()

    def __post_init__(self) -> None:
        A = na.nodal_analysis_coefficient_matrix(self.network, matrix_ops=self.matrix_ops, label_mappings=self.label_mappings)
        b = na.nodal_analysis_constants_vector(self.network, matrix_ops=self.matrix_ops, label_mappings=self.label_mappings)

        try:
            self.solution_vector = self.matrix_ops.solve(A, b)
        except mo.MatrixInversionException:
            self.solution_vector = (float('nan'),) * len(b)

    def get_potential(self, node_id: str) -> complex:
        if node_id == self.network.reference_node_label:
            return 0
        return self._potentials[self.label_mappings.node_mapping[node_id]]

    def get_current(self, branch_id: str) -> complex:
        if branch_id in self.label_mappings.voltage_source_mapping.keys:
            return self._voltage_source_currents[self.label_mappings.voltage_source_mapping[branch_id]]
        if self.network[branch_id].element.is_ideal_current_source:
            return complex(self.network[branch_id].element.I)
        if self.network[branch_id].element.is_current_source:
            return - (self.network[branch_id].element.I + self.get_voltage(branch_id)/self.network[branch_id].element.Z)
        branch = self.network[branch_id]
        return self.get_voltage(branch_id)/branch.element.Z