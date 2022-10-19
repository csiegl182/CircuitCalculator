from CircuitCalculator.Network import Network, Branch, NetworkSolution
import numpy as np

class DimensionError(Exception): pass

def calculate_node_voltages(Y : np.ndarray, I : np.ndarray) -> np.ndarray:
    if np.any(np.logical_not(np.isfinite(Y))):
        raise ValueError
    if np.any(np.logical_not(np.isfinite(I))):
        raise ValueError
    if Y.ndim != 2:
        raise DimensionError('dim error')
    if I.ndim != 1:
        raise DimensionError('dim error')
    m, n = Y.shape
    if n != m:
        raise DimensionError('dim error')
    return np.linalg.solve(Y, I)

def calculate_branch_voltage(V_node : np.ndarray, node1 : int, node2 : int) -> complex:
    if node1 < 0 or node2 < 0:
        raise DimensionError('dim error')
    try:
        V1 = 0 if node1 == 0 else V_node[node1-1]
        V2 = 0 if node2 == 0 else V_node[node2-1]
    except IndexError:
        raise DimensionError('dim error')
    return V1 - V2

def create_node_admittance_matrix_from_network(network : Network) -> np.ndarray:
    def full_admittance_between(node1: int, node2: int) -> complex:
        return sum(b.element.Y for b in network.branches_between(node1=node1, node2=node2))
    def full_admittance_connected_to(node: int) -> complex:
        return sum(b.element.Y for b in network.branches_connected_to(node))
    Y = np.diag([full_admittance_connected_to(node) for node in range(1, network.number_of_nodes)])
    for n1 in range(1, network.number_of_nodes):
        for n2 in range(n1+1, network.number_of_nodes):
            Y[n1-1, n2-1] = -full_admittance_between(n1, n2)
    Y += np.triu(Y,1).T
    return Y
    
def create_current_vector_from_network(network : Network) -> np.ndarray:
    I = np.zeros(network.number_of_nodes-1)
    for i in range(1, network.number_of_nodes):
        current_sources = [branch for branch in network.branches_connected_to(node=i) if branch.element.active]
        if len(current_sources) > 0:
            I[i-1] = sum([cs.element.I if cs.node2 == i else -cs.element.I for cs in current_sources])
        else:
            I[i-1] = 0
    return I

def calculate_node_voltages_from_network(network: Network) -> np.ndarray:
    Y = create_node_admittance_matrix_from_network(network)
    I = create_current_vector_from_network(network)
    return calculate_node_voltages(Y, I)

class NodalAnalysisSolution:
    def __init__(self, node_voltages = np.ndarray) -> None:
        self.node_voltages = node_voltages
    
    def get_voltage(self, branch: Branch) -> complex:
        return calculate_branch_voltage(self.node_voltages, branch.node1, branch.node2)

    def get_current(self, branch: Branch) -> complex:
        return self.get_voltage(branch)/branch.element.Z.real
        
def nodal_analysis_solver(network) -> NetworkSolution:
    return NodalAnalysisSolution(calculate_node_voltages_from_network(network))