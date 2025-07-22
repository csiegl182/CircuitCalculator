import pytest
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor

def test_network_returns_nodes_connected_to_node() -> None:
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('0', '2', resistor('R2', 20))
    branchC = Branch('1', '2', resistor('R3', 30))
    branchD = Branch('0', '2', resistor('R4', 30))
    network = Network([branchA, branchB, branchC, branchD])
    assert network.nodes_connected_to(node='0') == {'1', '2'}

def test_network_returns_nodes_connected_to_node_with_no_connections() -> None:
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('0', '2', resistor('R2', 20))
    branchC = Branch('1', '2', resistor('R3', 30))
    branchD = Branch('0', '2', resistor('R4', 30))
    network = Network([branchA, branchB, branchC, branchD])
    assert network.nodes_connected_to(node='3') == set()