import pytest
from CircuitCalculator.Network.network import Network, Branch, FloatingGroundNode, AmbiguousBranchIDs
from CircuitCalculator.Network.elements import resistor

def test_Network_knows_about_its_node_number() -> None:
    network = Network([Branch('0', '1', resistor('R1', 10))])
    assert network.number_of_nodes == 2

def test_empty_Network_has_one_node() -> None:
    network = Network([])
    assert network.number_of_nodes == 1

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

def test_ground_node_not_part_of_network_raises_error() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    branchA = Branch('0', '1', resistor('R1', R1))
    branchB = Branch('0', '2', resistor('R2', R2))
    branchC = Branch('1', '2', resistor('R3', R3))
    branchD = Branch('0', '2', resistor('R4', R4))
    with pytest.raises(FloatingGroundNode):
        Network([branchA, branchB, branchC, branchD], '7')

def test_empty_network_can_be_generated() -> None:
    network = Network([], node_zero_label='x')
    assert len(network.branches) == 0

def test_branch_ids_are_distinct() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    branchA = Branch('0', '1', resistor('R1', R1))
    branchB = Branch('0', '2', resistor('R1', R2))
    branchC = Branch('1', '2', resistor('R1', R3))
    branchD = Branch('0', '2', resistor('R1', R4))
    with pytest.raises(AmbiguousBranchIDs):
        Network([branchA, branchB, branchC, branchD])

def test_network_returns_branch_by_id() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    branchA = Branch('0', '1', resistor('R1', R1))
    branchB = Branch('0', '2', resistor('R2', R2))
    branchC = Branch('1', '2', resistor('R3', R3))
    branchD = Branch('0', '2', resistor('R4', R4))
    network = Network([branchA, branchB, branchC, branchD])
    assert network['R1'] == branchA
    assert network['R2'] == branchB
    assert network['R3'] == branchC
    assert network['R4'] == branchD

def test_network_returns_key_error_if_id_is_unknown() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    branchA = Branch('0', '1', resistor('R1', R1))
    branchB = Branch('0', '2', resistor('R2', R2))
    branchC = Branch('1', '2', resistor('R3', R3))
    branchD = Branch('0', '2', resistor('R4', R4))
    network = Network([branchA, branchB, branchC, branchD])
    with pytest.raises(KeyError):
        network['X']
