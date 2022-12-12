from CircuitCalculator.AdvancedNodalAnalysis import alphabetic_mapper
from CircuitCalculator.Network import Network, Branch, resistor

def test_alphabetic_mapper_returns_mapping_in_alphabetic_order() -> None:
    network = Network(
        [
            Branch('4', '8', resistor(1)),
            Branch('2', '1', resistor(1)),
            Branch('1', '3', resistor(1)),
            Branch('0', '1', resistor(1)),
            Branch('3', '8', resistor(1)),
            Branch('4', '3', resistor(1)),
            Branch('2', '8', resistor(1)),
            Branch('0', '8', resistor(1))
        ]
    )
    mapping = alphabetic_mapper(network)
    assert mapping['1'] == 0
    assert mapping['2'] == 1
    assert mapping['3'] == 2
    assert mapping['4'] == 3
    assert mapping['8'] == 4

def test_alphabetic_mapper_has_no_mapping_for_zero_node() -> None:
    network = Network(
        [
            Branch('0', '1', resistor(1)),
            Branch('4', '5', resistor(1)),
            Branch('2', '1', resistor(1)),
            Branch('1', '3', resistor(1)),
            Branch('3', '5', resistor(1)),
            Branch('4', '3', resistor(1)),
            Branch('2', '5', resistor(1)),
            Branch('0', '5', resistor(1))
        ],
        zero_node_label='2'
    )
    mapping = alphabetic_mapper(network)
    assert '2' not in mapping.keys()
