import pytest
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor

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
