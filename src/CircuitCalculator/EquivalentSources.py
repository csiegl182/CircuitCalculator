from .Network.network import Network
from .Network.transformers import switch_ground_node, passive_network
from .Network import labelmapper as map
from .NodalAnalysis import NodalAnalysisSolution, create_node_matrix_from_network
from numpy.linalg import inv as inverse_matrix
        
def calculate_total_impedeance(network: Network, node1: str, node2: str, node_index_mapper: map.NodeIndexMapper = map.default) -> complex:
    if node1 == node2:
        return 0
    if network.is_zero_node(node1):
        node1, node2 = node2, node1
    network = switch_ground_node(network=network, new_ground=node2)
    network = passive_network(network)
    Y = create_node_matrix_from_network(network, node_index_mapper=node_index_mapper)
    Z = inverse_matrix(Y)
    i1 = node_index_mapper(network)[node1]
    return Z[i1][i1]

def calculate_open_circuit_voltage(network: Network, node1: str, node2: str) -> complex:
    if node1 == node2:
        return 0
    solution = NodalAnalysisSolution(network)
    open_circuit_branch = network.branches_between(node1, node2)[0]
    if open_circuit_branch.node1 == node1:
        return solution.get_voltage(open_circuit_branch.id)
    else:
        return -solution.get_voltage(open_circuit_branch.id)

class TheveninEquivalentSource:
    def __init__(self, network: Network, node1: str, node2: str) -> None:
        self.U = calculate_open_circuit_voltage(network, node1, node2)
        self.Z = calculate_total_impedeance(network, node1, node2)

class NortenEquivalentSource:
    def __init__(self, network: Network, node1: str, node2: str) -> None:
        thevenin = TheveninEquivalentSource(network, node1, node2)
        self.I = thevenin.U/thevenin.Z
        self.Y = 1/thevenin.Z
        