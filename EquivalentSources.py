from typing import Tuple
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

class TheveninEquivalentSource:
    def __init__(self, network: Network, node1: int, node2: int = 0) -> None:
        solution = NodalAnalysisSolution(network)
        branch = network.branches_between(node1, node2)[0]
        if branch.node1 == node1:
            self.U = solution.get_voltage(branch)
        else:
            self.U = -solution.get_voltage(branch)
        self.Z = calculate_total_impedeance(network, node1, node2)

class NortenEquivalentSource:
    def __init__(self, network: Network, node1: int, node2: int = 0) -> None:
        thevenin = TheveninEquivalentSource(network, node1, node2)
        self.I = thevenin.U/thevenin.Z
        self.Y = 1/thevenin.Z
        