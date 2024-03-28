from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import voltage_source, resistor
from CircuitCalculator.Network.transformers import remove_short_circuit_elements

def test_remove_short_circuit() -> None:
    network = Network(
        branches=[
            Branch('0', '1', voltage_source('Vs1', V=0))
        ]
    )
    network = remove_short_circuit_elements(network)
    assert network.branches == []

def test_remove_short_circuit_removes_node_label_of_serial_element() -> None:
    network = Network(
        branches=[
            Branch('0', '1', resistor('R1', R=1)),
            Branch('1', '2', voltage_source('Vs1', V=0)),
            Branch('2', '3', resistor('R2', R=1))
        ]
    )
    network = remove_short_circuit_elements(network)
    assert '1' not in network.node_labels

def test_zero_node_label_is_kept() -> None:
    network = Network(
        branches=[
            Branch('0', '1', voltage_source('Vs1', V=1, Z=1))
        ],
        node_zero_label='1'
    )
    network = remove_short_circuit_elements(network)
    assert network.node_zero_label == '1'
