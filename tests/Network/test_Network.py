import pytest
from CircuitCalculator.Network import Network, resistor, Branch, switch_network_nodes

def test_Network_knows_about_its_node_number() -> None:
    network = Network([Branch(0, 1, resistor(10))])
    assert network.number_of_nodes == 2

def test_not_connected_nodes_count_for_total_number_of_nodes() -> None:
    network = Network([
        Branch(0, 1, resistor(1)),
        Branch(1, 3, resistor(1)),
        Branch(3, 0, resistor(1))
    ])
    assert network.number_of_nodes == 4

def test_Network_returns_branches_connected_to_node() -> None:
    branchA = Branch(0, 1, resistor(10))
    branchB = Branch(0, 2, resistor(20))
    branchC = Branch(1, 2, resistor(30))
    network = Network([branchA, branchB, branchC])
    assert network.branches_connected_to(node=2) == [branchB, branchC]

def test_Network_returns_branches_between_nodes() -> None:
    branchA = Branch(0, 1, resistor(10))
    branchB = Branch(0, 2, resistor(20))
    branchC = Branch(1, 2, resistor(30))
    branchD = Branch(0, 2, resistor(30))
    network = Network([branchA, branchB, branchC, branchD])
    assert network.branches_between(node1=0, node2=2) == [branchB, branchD]

def test_Network_raises_ValueError_when_asking_for_branches_between_equal_nodes() -> None:
    branchA = Branch(0, 1, resistor(10))
    branchB = Branch(0, 2, resistor(20))
    branchC = Branch(1, 2, resistor(30))
    branchD = Branch(0, 2, resistor(30))
    network = Network([branchA, branchB, branchC, branchD])
    with pytest.raises(ValueError):
        network.branches_between(node1=2, node2=2)

def test_Network_returns_branches_between_nodes_in_reverse_direction() -> None:
    branchA = Branch(0, 1, resistor(10))
    branchB = Branch(0, 2, resistor(20))
    branchC = Branch(1, 2, resistor(30))
    branchD = Branch(0, 2, resistor(30))
    network = Network([branchA, branchB, branchC, branchD])
    assert network.branches_between(node1=2, node2=0) == [branchB, branchD]
    
def test_Network_returns_nodes_connected_to_node() -> None:
    branchA = Branch(0, 1, resistor(10))
    branchB = Branch(0, 2, resistor(20))
    branchC = Branch(1, 2, resistor(30))
    branchD = Branch(0, 2, resistor(30))
    network = Network([branchA, branchB, branchC, branchD])
    assert network.nodes_connected_to(node=0) == {1, 2}

def test_node_zero_of_network_can_be_changed() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    branchA = Branch(0, 1, resistor(R1))
    branchB = Branch(0, 2, resistor(R2))
    branchC = Branch(1, 2, resistor(R3))
    branchD = Branch(0, 2, resistor(R4))
    network = Network([branchA, branchB, branchC, branchD])
    new_network = switch_network_nodes(network, 2)
    assert new_network.branches_between(2, 1)[0].element.Z == R1
    assert new_network.branches_between(2, 0)[0].element.Z == R2
    assert new_network.branches_between(1, 0)[0].element.Z == R3
    assert new_network.branches_between(2, 0)[1].element.Z == R4