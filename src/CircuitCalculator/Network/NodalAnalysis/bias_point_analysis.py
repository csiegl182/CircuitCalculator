from . import node_analysis as na
from .solution import NodalAnalysisSolution, NumericNodalAnalysisSolution
from ..network import Network
from ..solution import NetworkSolution
from .. import matrix_operations as mo
from . import label_mapping as map

def numeric_nodal_analysis_bias_point_solution(network: Network, label_mappings_factory: map.LabelMappingsFactory = map.default_label_mappings_factory) -> NodalAnalysisSolution:
        return NumericNodalAnalysisSolution(
            network=network,
            solution_vector=na.nodal_analysis_solution(network, matrix_ops=mo.NumPyMatrixOperations(), label_mappings_factory=label_mappings_factory),
            label_mappings=label_mappings_factory(network)
        )

def symbolic_nodal_analysis_bias_point_solution(network: Network, label_mappings_factory: map.LabelMappingsFactory = map.default_label_mappings_factory) -> NodalAnalysisSolution:
        return NumericNodalAnalysisSolution(
            network=network,
            solution_vector=na.nodal_analysis_solution(network, matrix_ops=mo.SymPyMatrixOperations(), label_mappings_factory=label_mappings_factory),
            label_mappings=label_mappings_factory(network)
        )

def open_circuit_voltage(network: Network, node1: str, node2: str) -> complex:
    solution = numeric_nodal_analysis_bias_point_solution(network)
    if node1 == node2:
        return 0
    phi1 = solution.get_potential(node_id=node1)
    phi2 = solution.get_potential(node_id=node2)
    return phi1-phi2

def short_circuit_current(network: Network, node1: str, node2: str) -> complex:
    Z = complex(na.open_circuit_impedance(network, node1, node2))
    V = open_circuit_voltage(network, node1, node2)
    return V/Z

def nodal_analysis_bias_point_solver(network: Network) -> NetworkSolution: ## TODO still needs to be implemented
    return numeric_nodal_analysis_bias_point_solution(network)

def symbolic_nodal_analysis_bias_point_solver(network: Network) -> NetworkSolution: ## TODO still needs to be implemented
    return symbolic_nodal_analysis_bias_point_solution(network)