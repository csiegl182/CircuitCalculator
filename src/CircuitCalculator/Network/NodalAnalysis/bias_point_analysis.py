from dataclasses import dataclass
from . import node_analysis as na
from .solution import NodalAnalysisSolution
from ..network import Network
from ..solution import NetworkSolution
from .. import matrix_operations as mo

@dataclass
class NodalAnalysisBiasPointSolution(NodalAnalysisSolution):
    matrix_ops: mo.MatrixOperations = mo.NumPyMatrixOperations()

    def __post_init__(self) -> None:
        A = na.nodal_analysis_coefficient_matrix(self.network, matrix_ops=self.matrix_ops, node_mapper=self.node_mapper, source_mapper=self.voltage_source_mapper)
        b = na.nodal_analysis_constants_vector(self.network, matrix_ops=self.matrix_ops, node_mapper=self.node_mapper, current_source_mapper=self.current_source_mapper, voltage_source_mapper=self.voltage_source_mapper)
        try:
            self._solution_vector = self.matrix_ops.solve(A, b)
        except mo.MatrixInversionException:
            self._solution_vector = (float('nan'),) * len(b)

    def get_potential(self, node_id: str) -> complex:
        if node_id == self.network.node_zero_label:
            return 0
        return self._potentials[self._node_mapping[node_id]]

    def get_current(self, branch_id: str) -> complex:
        if branch_id in self._voltage_source_mapping.keys:
            return self._voltage_source_currents[self._voltage_source_mapping[branch_id]]
        if self.network[branch_id].element.is_ideal_current_source:
            return complex(self.network[branch_id].element.I)
        if self.network[branch_id].element.is_current_source:
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
    Z = complex(na.open_circuit_impedance(network, node1, node2))
    V = open_circuit_voltage(network, node1, node2)
    return V/Z

def nodal_analysis_bias_point_solver(network: Network) -> NetworkSolution:
    return NodalAnalysisBiasPointSolution(network)

def symbolic_nodal_analysis_bias_point_solver(network: Network) -> NetworkSolution:
    return NodalAnalysisBiasPointSolution(network, matrix_ops=mo.SymPyMatrixOperations())