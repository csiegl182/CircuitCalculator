from .node_analysis import nodal_analysis_coefficient_matrix, nodal_analysis_constants_vector, open_circuit_impedance
from ..elements import is_ideal_current_source, is_current_source
from ..network import Network
from ..solution import NetworkSolution
from .solution import NodalAnalysisSolution
import numpy as np
from dataclasses import dataclass

@dataclass
class NodalAnalysisBiasPointSolution(NodalAnalysisSolution):
    def __post_init__(self) -> None:
        A = nodal_analysis_coefficient_matrix(self.network, node_mapper=self.node_mapper)
        b = nodal_analysis_constants_vector(self.network, node_mapper=self.node_mapper)
        try:
            self._solution_vector = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            self._solution_vector = np.zeros(np.size(b))
        if np.any(np.isnan(self._solution_vector)):
            self._solution_vector = np.zeros(np.size(b))

    @property
    def _potentials(self) -> np.ndarray:
        return self._solution_vector[:self._node_mapping.N]

    @property
    def _voltage_source_currents(self) -> np.ndarray:
        return self._solution_vector[-self._voltage_source_mapping.N:]

    def get_potential(self, node_id: str) -> complex:
        if node_id == self.network.node_zero_label:
            return 0
        return self._potentials[self._node_mapping[node_id]]

    def get_current(self, branch_id: str) -> complex:
        if branch_id in self._voltage_source_mapping.keys:
            return self._voltage_source_currents[self._voltage_source_mapping[branch_id]]
        if is_ideal_current_source(self.network[branch_id].element):
            return self.network[branch_id].element.I
        if is_current_source(self.network[branch_id].element):
            return - (self.network[branch_id].element.I + self.get_voltage(branch_id)/self.network[branch_id].element.Z)
        branch = self.network[branch_id]
        return self.get_voltage(branch_id)/branch.element.Z

def open_circuit_voltage(network: Network, node1: str, node2: str) -> complex:
    solution = NodalAnalysisBiasPointSolution(network)
    if node1 == node2:
        return 0
    phi1 = solution.get_potential(node_id=node1)
    phi2 = solution.get_potential(node_id=node2)
    return phi1-phi2

def short_circuit_current(network: Network, node1: str, node2: str) -> complex:
    Z = open_circuit_impedance(network, node1, node2)
    V = open_circuit_voltage(network, node1, node2)
    return V/Z

def nodal_analysis_bias_point_solver(network: Network) -> NetworkSolution:
    return NodalAnalysisBiasPointSolution(network)