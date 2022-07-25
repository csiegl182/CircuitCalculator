import pytest
from Network import Network, resistor, Branch

def test_Network_knows_about_its_node_number() -> None:
    network = Network([Branch(0, 1, resistor(10))])
    assert network.number_of_nodes == 2

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
    assert network.nodes_connected_to(node=0) == [1, 2]