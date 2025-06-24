from CircuitCalculator.Network.network import Network, Branch
import CircuitCalculator.Network.elements as elm
from CircuitCalculator.Network.transformers import remove_active_elements

def test_voltage_sources_are_substituted_by_open_circuit() -> None:
    network = Network([Branch('n1', 'n2', elm.voltage_source('Vs', 5.0))], node_zero_label='n2')
    passive_network = remove_active_elements(network)

    assert len(passive_network.branches) == 1
    assert passive_network.node_zero_label == network.node_zero_label
    assert passive_network.branches[0].element.is_open_circuit

def test_linear_voltage_sources_are_substituted_by_inner_resisotr() -> None:
    network = Network([Branch('n1', 'n2', elm.voltage_source('Vs', V=5.0, Z=3))], node_zero_label='n2')
    passive_network = remove_active_elements(network)

    assert len(passive_network.branches) == 1
    assert passive_network.node_zero_label == network.node_zero_label
    assert passive_network.branches[0].element.V == 0.0
    assert passive_network.branches[0].element.Z == 3.0

def test_current_sources_are_substituted_by_open_circuit() -> None:
    network = Network([Branch('n1', 'n2', elm.current_source('Is', 5.0))], node_zero_label='n2')
    passive_network = remove_active_elements(network)

    assert len(passive_network.branches) == 1
    assert passive_network.node_zero_label == network.node_zero_label
    assert passive_network.branches[0].element.is_open_circuit

def test_linear_current_sources_are_substituted_by_open_circuit() -> None:
    network = Network([Branch('n1', 'n2', elm.current_source('Is', I=5.0, Y=3))], node_zero_label='n2')
    passive_network = remove_active_elements(network)

    assert len(passive_network.branches) == 1
    assert passive_network.node_zero_label == network.node_zero_label
    assert passive_network.branches[0].element.I == 0
    assert passive_network.branches[0].element.Y == 3

def test_node_zero_label_is_preserved() -> None:
    network = Network(
        [
            Branch('n1', 'n2', elm.resistor('R', 10.0)),
            Branch('n3', 'n2', elm.voltage_source('Vs', 1.0))
        ], node_zero_label='n1')
    passive_network = remove_active_elements(network)

    assert passive_network.node_zero_label == network.node_zero_label