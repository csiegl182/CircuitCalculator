import pytest
from Network import NetworkReducedParallel, resistor, Branch

def test_NetworkReducedParallel_knows_about_its_node_number() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    network = NetworkReducedParallel([Branch(0, 1, resistor(R1)), Branch(0, 1, resistor(R2)), Branch(1, 2, resistor(R3)), Branch(0, 1, resistor(R4))])
    assert network.number_of_nodes == 3

def test_NetworkReducedParallel_reduces_parallel_branches() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    network = NetworkReducedParallel([Branch(0, 1, resistor(R1)), Branch(0, 1, resistor(R2)), Branch(1, 2, resistor(R3)), Branch(0, 1, resistor(R4))])
    assert len(network.branches) == 2

def test_NetworkReducedParallel_returns_only_one_branch_between_two_nodes() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    network = NetworkReducedParallel([Branch(0, 1, resistor(R1)), Branch(0, 1, resistor(R2)), Branch(1, 2, resistor(R3)), Branch(0, 1, resistor(R4))])
    assert len(network.branches_between(node1=0, node2=1)) == 1
    assert len(network.branches_between(node1=1, node2=2)) == 1

def test_NetworkReducedParallel_calculates_parallel_resistors() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    network = NetworkReducedParallel([Branch(0, 1, resistor(R1)), Branch(0, 1, resistor(R2)), Branch(1, 2, resistor(R3)), Branch(0, 1, resistor(R4))])
    assert network.branches_between(node1=0, node2=1)[0].element.Z == pytest.approx(1/(1/R1+1/R2+1/R4), 0.0001)