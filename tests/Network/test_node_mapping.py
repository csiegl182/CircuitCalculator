from CircuitCalculator.Network.network import node_index_mapping, Network, Branch
from CircuitCalculator.Network.elements import resistor

def test_node_mapping_has_unique_set_of_node_indices() -> None:
    network = Network(
        [
            Branch('1', '0', resistor(R=10)),
            Branch('0', '4', resistor(R=20)),
            Branch('1', '2', resistor(R=30)),
            Branch('3', '4', resistor(R=30)),
            Branch('4', '0', resistor(R=40))
        ]
    )
    mapping = node_index_mapping(network)
    assert len(mapping.keys()) == len(set(mapping.values()))

def test_number_of_mapping_keys_corresponds_to_the_number_of_network_nodes_when_zero_node_is_labeled() -> None:
    network = Network(
        [
            Branch('1', '0', resistor(R=10)),
            Branch('0', '4', resistor(R=20)),
            Branch('1', '2', resistor(R=30)),
            Branch('3', '4', resistor(R=30)),
            Branch('4', '0', resistor(R=40))
        ]
    )
    mapping = node_index_mapping(network)
    assert len(mapping) == network.number_of_nodes

def test_number_of_mapping_keys_corresponds_to_the_number_of_network_nodes_when_no_zero_node_is_labeled() -> None:
    network = Network(
        branches=[
            Branch('1', '5', resistor(R=10)),
            Branch('5', '4', resistor(R=20)),
            Branch('1', '2', resistor(R=30)),
            Branch('3', '4', resistor(R=30)),
            Branch('4', '5', resistor(R=40))
        ],
        zero_node_label='1'
    )
    mapping = node_index_mapping(network)
    assert len(mapping) == network.number_of_nodes