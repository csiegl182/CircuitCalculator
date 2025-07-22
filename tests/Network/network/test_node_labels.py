import pytest
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor

def test_node_labels_returns_all_node_labels() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    branchA = Branch('0', '1', resistor('R1', R1))
    branchB = Branch('0', '2', resistor('R2', R2))
    branchC = Branch('1', '2', resistor('R3', R3))
    branchD = Branch('0', '2', resistor('R4', R4))
    network = Network([branchA, branchB, branchC, branchD])
 
def test_reference_node_is_within_set_of_node_labels() -> None:
    R1, R2 = 10, 20
    branchA = Branch('0', '1', resistor('R1', R1))
    branchB = Branch('0', '2', resistor('R2', R2))
    network = Network([branchA, branchB], reference_node_label='1')
    assert '1' in network.node_labels

def test_only_reference_connected_nodes_are_within_set_of_node_labels() -> None:
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('0', '2', resistor('R2', 20))
    branchC = Branch('2', '3', resistor('R3', 30))
    branchD = Branch('3', '4', resistor('R4', 40))
    branchE = Branch('3', '5', resistor('R5', 50))
    branchF = Branch('a', 'b', resistor('R6', 60))
    network = Network([branchA, branchB, branchC, branchD, branchE, branchF])
    assert network.node_labels == {'0', '1', '2', '3', '4', '5'}
