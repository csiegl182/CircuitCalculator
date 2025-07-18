from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor

def test_network_returns_branches_connected_to_node() -> None:
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('0', '2', resistor('R2', 20))
    branchC = Branch('1', '2', resistor('R3', 30))
    network = Network([branchA, branchB, branchC])
    assert network.branches_connected_to(node='2') == [branchB, branchC]

def test_network_returns_empty_list_for_no_branches_connected() -> None:
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('0', '2', resistor('R2', 20))
    network = Network([branchA, branchB])
    assert network.branches_connected_to(node='3') == []