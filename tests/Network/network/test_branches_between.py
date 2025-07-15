import pytest
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor

def test_Network_returns_branches_between_nodes() -> None:
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('0', '2', resistor('R2', 20))
    branchC = Branch('1', '2', resistor('R3', 30))
    branchD = Branch('0', '2', resistor('R4', 30))
    network = Network([branchA, branchB, branchC, branchD])
    assert network.branches_between(node1='0', node2='2') == [branchB, branchD]

def test_Network_returns_empty_list_when_asking_for_branches_between_equal_nodes() -> None:
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('0', '2', resistor('R2', 20))
    branchC = Branch('1', '2', resistor('R3', 30))
    branchD = Branch('0', '2', resistor('R4', 30))
    network = Network([branchA, branchB, branchC, branchD])
    assert network.branches_between(node1='2', node2='2') == []

def test_Network_returns_branches_between_nodes_in_reverse_direction() -> None:
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('0', '2', resistor('R2', 20))
    branchC = Branch('1', '2', resistor('R3', 30))
    branchD = Branch('0', '2', resistor('R4', 30))
    network = Network([branchA, branchB, branchC, branchD])
    assert network.branches_between(node1='2', node2='0') == [branchB, branchD]
