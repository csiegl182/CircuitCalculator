from CircuitCalculator.Network import node_index_mapping, Network, Branch, resistor

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