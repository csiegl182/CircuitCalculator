import pytest
from CircuitCalculator.Network.network import Network, Branch, FloatingGroundNode, AmbiguousBranchIDs
from CircuitCalculator.Network.elements import resistor
from CircuitCalculator.Network.transformers import switch_ground_node

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