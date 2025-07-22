from . import node_analysis as na
from .solution import numeric_nodal_analysis_bias_point_solution
from ..network import Network

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
