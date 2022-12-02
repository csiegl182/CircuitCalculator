from .Network import Network, Branch, node_index_mapping, NetworkSolution
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
    def full_admittance_connected_to(node: str) -> complex:
        return sum(b.element.Y for b in network.branches_connected_to(node))
    node_mapping = node_index_mapping(network)
    Y = np.diag([full_admittance_connected_to(node) for node in node_mapping.keys() if not network.is_zero_node(node)])
    for b in network.branches:
        if not network.is_zero_node(b.node1) and not network.is_zero_node(b.node2):
            i1, i2 = map(lambda x: node_mapping[x], (b.node1, b.node2))
            Y[i1-1, i2-1] += -b.element.Y
            Y[i2-1, i1-1] += -b.element.Y
    return Y
    
def create_current_vector_from_network(network : Network) -> np.ndarray:
    node_mapping = node_index_mapping(network)
    I = np.zeros(network.number_of_nodes-1)
    for n, i in node_mapping.items():
        current_sources = [branch for branch in network.branches_connected_to(node=n) if branch.element.active]
        if len(current_sources) > 0:
            I[i-1] = sum([cs.element.I if cs.node2 == n else -cs.element.I for cs in current_sources])
        else:
            I[i-1] = 0
    return I

class NodalAnalysisSolution:
    def __init__(self, network: Network) -> None:
        Y = create_node_admittance_matrix_from_network(network)
        I = create_current_vector_from_network(network)
        self._network = network
        self._node_voltages = calculate_node_voltages(Y, I)
        self._node_mapping = node_index_mapping(network)
    
    def get_voltage(self, branch: Branch) -> complex:
        branch_voltage = calculate_branch_voltage(self._node_voltages, self._node_mapping[branch.node1], self._node_mapping[branch.node2])
        if branch.element.active:
            branch_voltage += branch.element.U
        return branch_voltage

    def get_current(self, branch: Branch) -> complex:
        return self.get_voltage(branch)/branch.element.Z.real
        
def nodal_analysis_solver(network) -> NetworkSolution:
    return NodalAnalysisSolution(network)