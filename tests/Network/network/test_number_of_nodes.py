import pytest
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor

def test_Network_knows_about_its_node_number() -> None:
    network = Network([Branch('0', '1', resistor('R1', 10))])
    assert network.number_of_nodes == 2

def test_empty_Network_has_one_node() -> None:
    network = Network([])
    assert network.number_of_nodes == 1
