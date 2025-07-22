from CircuitCalculator.Network.NodalAnalysis.label_mapping import alphabetic_node_mapper
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor, voltage_source

def test_alphabetic_mapper_returns_mapping_in_alphabetic_order() -> None:
    network = Network(
        [
            Branch('4', '8', resistor('R1', 1)),
            Branch('2', '1', resistor('R2', 1)),
            Branch('1', '3', resistor('R3', 1)),
            Branch('0', '1', resistor('R4', 1)),
            Branch('3', '8', resistor('R5', 1)),
            Branch('4', '3', resistor('R6', 1)),
            Branch('2', '8', resistor('R7', 1)),
            Branch('0', '8', resistor('R8', 1))
        ]
    )
    mapping = alphabetic_node_mapper(network)
    assert mapping['1'] == 0
    assert mapping['2'] == 1
    assert mapping['3'] == 2
    assert mapping['4'] == 3
    assert mapping['8'] == 4

def test_alphabetic_mapper_has_no_mapping_for_zero_node() -> None:
    network = Network(
        [
            Branch('0', '1', resistor('R1', 1)),
            Branch('4', '5', resistor('R2', 1)),
            Branch('2', '1', resistor('R3', 1)),
            Branch('1', '3', resistor('R4', 1)),
            Branch('3', '5', resistor('R5', 1)),
            Branch('4', '3', resistor('R6', 1)),
            Branch('2', '5', resistor('R7', 1)),
            Branch('0', '5', resistor('R8', 1))
        ],
        reference_node_label='2'
    )
    mapping = alphabetic_node_mapper(network)
    assert '2' not in mapping.keys