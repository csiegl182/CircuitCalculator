import pytest
from CircuitCalculator.Network.network import Network, Branch, FloatingGroundNode, AmbiguousBranchIDs
from CircuitCalculator.Network.elements import resistor

def test_ground_node_not_part_of_network_raises_error() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    branchA = Branch('0', '1', resistor('R1', R1))
    branchB = Branch('0', '2', resistor('R2', R2))
    branchC = Branch('1', '2', resistor('R3', R3))
    branchD = Branch('0', '2', resistor('R4', R4))
    with pytest.raises(FloatingGroundNode):
        Network([branchA, branchB, branchC, branchD], '7')

def test_empty_network_can_be_generated() -> None:
    network = Network([], reference_node_label='x')
    assert len(network.branches) == 0

def test_branch_ids_are_distinct() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    branchA = Branch('0', '1', resistor('R1', R1))
    branchB = Branch('0', '2', resistor('R1', R2))
    branchC = Branch('1', '2', resistor('R1', R3))
    branchD = Branch('0', '2', resistor('R1', R4))
    with pytest.raises(AmbiguousBranchIDs):
        Network([branchA, branchB, branchC, branchD])