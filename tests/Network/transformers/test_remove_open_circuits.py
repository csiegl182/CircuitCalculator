from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import current_source
from CircuitCalculator.Network.transformers import remove_open_circuit_elements

def test_remove_open_circuit() -> None:
    network = Network(
        branches=[
            Branch('0', '1', current_source('Is1', I=0))
        ]
    )
    network = remove_open_circuit_elements(network)
    assert network.branches == []

def test_zero_node_label_is_kept() -> None:
    network = Network(
        branches=[
            Branch('0', '1', current_source('Is1', I=1, Y=1))
        ],
        node_zero_label='1'
    )
    network = remove_open_circuit_elements(network)
    assert network.node_zero_label == '1'
