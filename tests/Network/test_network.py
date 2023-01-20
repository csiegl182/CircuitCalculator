import pytest
from CircuitCalculator.Network.network import Network, Branch, FloatingGroundNode, AmbiguousBranchIDs
from CircuitCalculator.Network.elements import resistor
from CircuitCalculator.Network.transformers import switch_ground_node

def test_Network_knows_about_its_node_number() -> None:
    network = Network([Branch('0', '1', resistor('R1', 10))])
    assert network.number_of_nodes == 2

def test_Network_returns_branches_connected_to_node() -> None:
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('0', '2', resistor('R2', 20))
    branchC = Branch('1', '2', resistor('R3', 30))
    network = Network([branchA, branchB, branchC])
    assert network.branches_connected_to(node='2') == [branchB, branchC]

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
    
def test_Network_returns_nodes_connected_to_node() -> None:
    branchA = Branch('0', '1', resistor('R1', 10))
    branchB = Branch('0', '2', resistor('R2', 20))
    branchC = Branch('1', '2', resistor('R3', 30))
    branchD = Branch('0', '2', resistor('R4', 30))
    network = Network([branchA, branchB, branchC, branchD])
    assert network.nodes_connected_to(node='0') == {'1', '2'}

def test_ground_node_of_network_can_be_switched_to_another_node() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    branchA = Branch('0', '1', resistor('R1', R1))
    branchB = Branch('0', '2', resistor('R2', R2))
    branchC = Branch('1', '2', resistor('R3', R3))
    branchD = Branch('0', '2', resistor('R4', R4))
    network = Network([branchA, branchB, branchC, branchD])
    new_network = switch_ground_node(network, '2')
    assert new_network.branches_between('0', '1')[0].element.Z == R1
    assert new_network.branches_between('0', '2')[0].element.Z == R2
    assert new_network.branches_between('1', '2')[0].element.Z == R3
    assert new_network.branches_between('0', '2')[1].element.Z == R4
    assert new_network.is_zero_node('0') == False
    assert new_network.is_zero_node('2') == True

def test_switching_unknown_ground_node_leads_to_error() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    branchA = Branch('0', '1', resistor('R1', R1))
    branchB = Branch('0', '2', resistor('R2', R2))
    branchC = Branch('1', '2', resistor('R3', R3))
    branchD = Branch('0', '2', resistor('R4', R4))
    network = Network([branchA, branchB, branchC, branchD])
    with pytest.raises(FloatingGroundNode):
        switch_ground_node(network, '7')

def test_branch_ids_are_distinct() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    branchA = Branch('0', '1', resistor('R1', R1))
    branchB = Branch('0', '2', resistor('R1', R2))
    branchC = Branch('1', '2', resistor('R1', R3))
    branchD = Branch('0', '2', resistor('R1', R4))
    with pytest.raises(AmbiguousBranchIDs):
        Network([branchA, branchB, branchC, branchD])
