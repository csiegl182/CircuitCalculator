from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor, voltage_source, current_source, open_circuit, short_circuit
from CircuitCalculator.Network.NodalAnalysis.state_space_model import state_space_matrices
import numpy as np
from numpy.testing import assert_almost_equal

def test_output_matrix_of_transient_network_1() -> None:
    Vs = 1
    R1, R2, R3 = 10, 20, 30
    C = 1e-3
    network = Network([
        Branch('1', '0', voltage_source('Vs', V=Vs)),
        Branch('1', '2', resistor('R1', R=R1)),
        Branch('2', '0', resistor('R2', R=R2)),
        Branch('2', '3', resistor('R3', R=R3)),
        Branch('3', '0', open_circuit('C'))
    ])
    _, _, C, _ = state_space_matrices(network, {'C' : C})
    assert_almost_equal(C, np.array([[0], [R1*R2/(R1*R2+R2*R3+R1*R3)], [1], [R2/(R1*R2+R2*R3+R1*R3)]]), decimal=5)

def test_output_matrix_of_transient_network_2() -> None:
    Vs = 1
    R1, R2, R3 = 10, 20, 30
    C = 1e-3
    network = Network([
        Branch('1', '0', voltage_source('Vs', V=Vs)),
        Branch('1', '2', resistor('R1', R=R1)),
        Branch('2', '0', resistor('R2', R=R2)),
        Branch('2', '3', open_circuit('C')),
        Branch('3', '0', resistor('R3', R=R3))
    ])
    _, _, C, _ = state_space_matrices(network, {'C' : C})
    assert_almost_equal(C, np.array([[0], [R1*R2/(R1*R2 + R1*R3 + R2*R3)], [-R3*(R1 + R2)/(R1*R2 + R1*R3 + R2*R3)], [R2/(R1*R2 + R1*R3 + R2*R3)]]), decimal=5)

def test_output_matrix_of_transient_network_3() -> None:
    Vs = 1
    Is = 1
    R1, R2 = 10, 20
    C = 1e-3
    network = Network([
        Branch('1', '0', voltage_source('Vs', V=Vs)),
        Branch('1', '2', resistor('R1', R=R1)),
        Branch('2', '3', open_circuit('C')),
        Branch('3', '0', resistor('R2', R=R2)),
        Branch('0', '3', current_source('Is', I=Is))
    ])
    _, _, C, _ = state_space_matrices(network, {'C' : C})
    assert_almost_equal(C, np.array([[0], [R1/(R1+R2)], [-R2/(R1+R2)], [1/(R1+R2)]]))

def test_output_matrix_of_transient_network_4() -> None:
    Vs = 1
    R1, R2 = 10, 20
    C1, C2 = 5e-3, 1e-3
    network = Network([
        Branch('1', '0', voltage_source('Vs', V=Vs)),
        Branch('1', '2', resistor('R1', R=R1)),
        Branch('2', '3', open_circuit('C1')),
        Branch('3', '0', resistor('R2', R=R2)),
        Branch('3', '0', open_circuit('C2'))
    ])
    _, _, C, _ = state_space_matrices(network, {'C1' : C1, 'C2' : C2})
    assert_almost_equal(C, np.array([[0, 0], [1, 1], [0, 1], [1/R1, 1/R1]]))

def test_output_matrix_of_transient_network_5() -> None:
    V0 = 5
    R1, R2, R3 = 10, 20, 30
    L = 0.1
    network = Network([
        Branch('1', '0', voltage_source('Vq', V=V0)),
        Branch('1', '2', resistor('R1', R=R1)),
        Branch('2', '0', resistor('R2', R=R2)),
        Branch('2', '3', resistor('R3', R=R3)),
        Branch('3', '0', short_circuit('L'))
    ])
    _, _, C, _ = state_space_matrices(network, l_values={'L' : L})
    assert_almost_equal(C, np.array([[0], [-R1*R2/(R1+R2)], [-(R1*R2+R1*R3+R2*R3)/(R1+R2)], [1], [-R2/(R1+R2)]]))

def test_output_matrix_of_transient_network_6() -> None:
    R1, R2, R3 = 10, 20, 30
    L = 0.1
    V0 = 5
    network = Network([
        Branch('1', '0', voltage_source('Vq', V=V0)),
        Branch('1', '2', resistor('R1', R=R1)),
        Branch('2', '0', resistor('R2', R=R2)),
        Branch('2', '3', short_circuit('L')),
        Branch('3', '0', resistor('R3', R=R3))
    ])
    _, _, C, _ = state_space_matrices(network, l_values={'L' : L})
    assert_almost_equal(C, np.array([[0], [-R1*R2/(R1+R2)], [R3], [1], [-R2/(R1+R2)]]))

def test_output_matrix_of_transient_network_7() -> None:
    R1, R2, R3 = 10, 20, 30
    L = 0.1
    V0 = 5
    I0 = 1
    network = Network([
        Branch('1', '0', voltage_source('Vq', V=V0)),
        Branch('1', '2', resistor('R1', R=R1)),
        Branch('2', '0', resistor('R2', R=R2)),
        Branch('2', '3', short_circuit('L')),
        Branch('3', '0', resistor('R3', R=R3)),
        Branch('0', '3', current_source('Iq', I=I0))
    ])
    _, _, C, _ = state_space_matrices(network, l_values={'L' : L})
    assert_almost_equal(C, np.array([[0], [-R1*R2/(R1+R2)], [R3], [1], [-R2/(R1+R2)]]))

def test_output_matrix_of_transient_network_8() -> None:
    R1, R2 = 10, 20
    L1, L2 = 0.1, 0.2
    V0 = 5
    network = Network([
        Branch('1', '0', voltage_source('Vq', V=V0)),
        Branch('1', '2', resistor('R1', R=R1)),
        Branch('2', '3', short_circuit('L1')),
        Branch('3', '0', resistor('R2', R=R2)),
        Branch('3', '0', short_circuit('L2'))
    ])
    _, _, C, _ = state_space_matrices(network, l_values={'L1' : L1, 'L2' : L2})
    assert_almost_equal(C, np.array([[0, 0], [-R1, 0], [R2, -R2], [1, 0], [0, 1], [-1, 0]]))

def test_output_matrix_of_transient_network_9() -> None:
    R = 2
    L = 2e-3
    C = 0.5e-3
    V0 = 5
    network = Network([
        Branch('1', '0', voltage_source('Vq', V=V0)), 
        Branch('1', '2', resistor('R', R=R)),
        Branch('2', '3', short_circuit('L')),
        Branch('3', '0', open_circuit('C'))
    ])
    _, _, C, _ = state_space_matrices(network, c_values={'C': C}, l_values={'L' : L})
    assert_almost_equal(C, np.array([[0, 0], [0, -R], [1, 0], [0, 1], [0, -1]]))