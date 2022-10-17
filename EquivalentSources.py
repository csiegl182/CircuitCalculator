from Network import Network, switch_network_nodes
from AdvancedNodalAnalysis import NodalAnalysisSolution, create_node_matrix_from_network
from numpy.linalg import inv as inverse_matrix

def calculate_total_impedeance(network: Network, node1: int, node2: int = 0) -> complex:
    if node1 == node2:
        return 0
    if node1 == 0:
        node1 = node2
        node2 = 0
    if node1 != 0 or node2 != 0:
        network = switch_network_nodes(network, new_node=0, old_node=node2)
    Y = create_node_matrix_from_network(network)
    Z = inverse_matrix(Y)
    return Z[node1-1][node1-1]

def calculate_open_circuit_voltage(network: Network, node1: int, node2: int = 0) -> complex:
    if node1 == node2:
        return 0
    solution = NodalAnalysisSolution(network)
    open_circuit_branch = network.branches_between(node1, node2)[0]
    if open_circuit_branch.node1 == node1:
        return solution.get_voltage(open_circuit_branch)
    else:
        return -solution.get_voltage(open_circuit_branch)

class TheveninEquivalentSource:
    def __init__(self, network: Network, node1: int, node2: int = 0) -> None:
        self.U = calculate_open_circuit_voltage(network, node1, node2)
        self.Z = calculate_total_impedeance(network, node1, node2)

class NortenEquivalentSource:
    def __init__(self, network: Network, node1: int, node2: int = 0) -> None:
        thevenin = TheveninEquivalentSource(network, node1, node2)
        self.I = thevenin.U/thevenin.Z
        self.Y = 1/thevenin.Z
        