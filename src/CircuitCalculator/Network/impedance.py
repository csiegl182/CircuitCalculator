from .network import Network
from .elements import is_ideal_voltage_source
from .transformers import switch_ground_node, passive_network, remove_element
from . import labelmapper as map
from .NodalAnalysis import create_node_matrix_from_network
from numpy.linalg import inv as inverse_matrix
        
def open_circuit_impedance(network: Network, node1: str, node2: str, node_index_mapper: map.NodeIndexMapper = map.default) -> complex:
    if node1 == node2:
        return 0
    if any([is_ideal_voltage_source(b.element) for b in network.branches_between(node1, node2)]):
        return 0
    if network.is_zero_node(node1):
        node1, node2 = node2, node1
    network = switch_ground_node(network=network, new_ground=node2)
    network = passive_network(network)
    Y = create_node_matrix_from_network(network, node_index_mapper=node_index_mapper)
    Z = inverse_matrix(Y)
    i1 = node_index_mapper(network)[node1]
    return Z[i1][i1]

def element_impedance(network: Network, element: str, node_index_mapper: map.NodeIndexMapper = map.default) -> complex:
    return open_circuit_impedance(
        network=remove_element(network, element),
        node1=network[element].node1,
        node2=network[element].node2,
        node_index_mapper=node_index_mapper
    )
