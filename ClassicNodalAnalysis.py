from Network import Network, RealCurrentSource, Branch, NetworkReducedParallel
import numpy as np

class DimensionError(Exception): pass

def calculate_node_voltages(Y : np.ndarray, I : np.ndarray) -> np.ndarray:
    if Y.ndim != 2:
        raise DimensionError('dim error')
    if I.ndim != 1:
        raise DimensionError('dim error')
    m, n = Y.shape
    if n != m:
        raise DimensionError('dim error')
    return np.linalg.solve(Y, I)

def create_node_admittance_matrix(zero_node_admittances, *node_admittances) ->  np.ndarray:
    if [len(y_vec) for y_vec in node_admittances] != list(range(1, len(zero_node_admittances)))[::-1]:
        raise DimensionError('dim error')
        
    Y = np.diag(zero_node_admittances)
    for n, admittances in enumerate(node_admittances):
        Y[n,n] += np.sum(admittances)
        for m, y in enumerate(admittances):
            Y[n+m+1,n+m+1] += y
            Y[n+m+1, n] = -y
    Y += np.tril(Y,-1).T

    return Y

def calculate_branch_voltage(V_node : np.ndarray, node1 : int, node2 : int) -> float:
    if node1 < 0 or node2 < 0:
        raise DimensionError('dim error')
    try:
        V1 = 0 if node1 == 0 else V_node[node1-1]
        V2 = 0 if node2 == 0 else V_node[node2-1]
    except IndexError:
        raise DimensionError('dim error')
    return V1 - V2

def create_node_admittance_matrix_from_network(network : Network) -> np.ndarray:
    network = NetworkReducedParallel(network.branches)
    zero_node_admittances = [branch.element.Y for branch in network.branches_connected_to(node=0)]
    node_admittances = []
    for i in range(1, network.number_of_nodes-1):
        node_admittances += [[branch.element.Y for branch in network.branches_connected_to(node=i) if branch.node1 > i or branch.node2 > i]]
    return create_node_admittance_matrix(zero_node_admittances, *node_admittances)
    
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
    
    def get_voltage(self, branch: Branch) -> float:
        return calculate_branch_voltage(self.node_voltages, branch.node1, branch.node2)

    def get_current(self, branch: Branch) -> float:
        return self.get_voltage(branch)/branch.element.Z.real
        
def nodal_analysis_solver(network):
    return NodalAnalysisSolution(calculate_node_voltages_from_network(network))