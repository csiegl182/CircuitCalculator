from .Network import Network, Branch, node_index_mapping, switch_network_nodes
from .AdvancedNodalAnalysis import NodalAnalysisSolution, NodeTypes, create_node_matrix_from_network, is_ideal_current_source
from numpy.linalg import inv as inverse_matrix

def remove_ideal_current_sources(network: Network) -> Network:
    return Network([b for b in network.branches if not is_ideal_current_source(b)])

def remove_ideal_voltage_sources(network: Network) -> Network:
    nodes = NodeTypes(network)
    branches = network.branches
    for an, cp in zip(nodes.active_nodes, nodes.counterparts):
        branches = [Branch(cp, b.node2, b.element) if b.node1 == an else b for b in branches]
        branches = [Branch(b.node1, cp, b.element) if b.node2 == an else b for b in branches]
        branches = [b for b in branches if b.node1 != b.node2]
    return Network(branches)
        
def calculate_total_impedeance(network: Network, node1: str, node2: str) -> complex:
    if node1 == node2:
        return 0
    if network.is_zero_node(node1):
        node1, node2 = node2, node1
    network = switch_network_nodes(network, new_node=network.zero_node_label, old_node=node2)
    network = remove_ideal_current_sources(network)
    network = remove_ideal_voltage_sources(network)
    Y = create_node_matrix_from_network(network)
    Z = inverse_matrix(Y)
    i1 = node_index_mapping(network)[node1]
    return Z[i1-1][i1-1]

def calculate_open_circuit_voltage(network: Network, node1: str, node2: str) -> complex:
    if node1 == node2:
        return 0
    solution = NodalAnalysisSolution(network)
    open_circuit_branch = network.branches_between(node1, node2)[0]
    if open_circuit_branch.node1 == node1:
        return solution.get_voltage(open_circuit_branch)
    else:
        return -solution.get_voltage(open_circuit_branch)

class TheveninEquivalentSource:
    def __init__(self, network: Network, node1: str, node2: str) -> None:
        self.U = calculate_open_circuit_voltage(network, node1, node2)
        self.Z = calculate_total_impedeance(network, node1, node2)

class NortenEquivalentSource:
    def __init__(self, network: Network, node1: str, node2: str) -> None:
        thevenin = TheveninEquivalentSource(network, node1, node2)
        self.I = thevenin.U/thevenin.Z
        self.Y = 1/thevenin.Z
        