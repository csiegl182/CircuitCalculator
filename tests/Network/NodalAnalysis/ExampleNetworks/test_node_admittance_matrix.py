from CircuitCalculator.Network.NodalAnalysis.node_analysis import node_admittance_matrix
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor, voltage_source, current_source
import numpy as np

def test_create_node_matrix_from_reference_network_1() -> None:
    Vq = 1+0j
    R = 1
    G = 1/R
    network = Network(
        [
            Branch('1', '0', voltage_source('Vq', V=Vq)),
            Branch('1', '0', resistor('R', R=R))
        ]
    )
    Y = node_admittance_matrix(network)
    Y_ref = np.array([
        [G]
        ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_matrix_from_reference_network_2() -> None:
    Iq = 1+0j
    R = 1
    G = 1/R
    network = Network(
        [
            Branch('0', '1', current_source('Iq', I=Iq)),
            Branch('1', '0', resistor('R1', R=R))
        ]
    )
    Y = node_admittance_matrix(network)
    Y_ref = np.array([
        [G]
        ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_matrix_from_reference_network_3() -> None:
    R1, R2, Ri = 10, 20, 100
    G1, G2, Gi = 1/R1, 1/R2, 1/Ri
    Iq = 1
    network = Network(
        [
            Branch('0', '1', current_source('Is', I=Iq, Y=1/Ri)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('2', '0', resistor('R2', R=R2))
        ]
    )
    Y = node_admittance_matrix(network)
    Y_ref = np.array([
        [G1+Gi,   -G1],
        [  -G1, G1+G2]
        ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_matrix_from_reference_network_4() -> None:
    R1, R2, R3 = 10, 20, 30
    G1, G2, G3 = 1/R1, 1/R2, 1/R3
    Uq = 1
    network = Network(
        [
            Branch('1', '0', voltage_source('Uq', V=Uq)),
            Branch('1', '0', resistor('R1', R=R1)),
            Branch('1', '2', resistor('R2', R=R2)),
            Branch('2', '0', resistor('R3', R=R3))
        ]
    )
    Y = node_admittance_matrix(network)
    Y_ref = np.array([
        [G1+G2,    -G2],
        [  -G2,  G2+G3]
        ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_matrix_from_reference_network_5() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G1, G2, G3, G4, G5 = 1/R1, 1/R2, 1/R3, 1/R4, 1/R5
    Uq1, Uq2 = 1, 2
    network = Network(
        [
            Branch('1', '0', voltage_source('Uq1', V=Uq1)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('2', '0', resistor('R2', R=R2)),
            Branch('2', '3', resistor('R3', R=R3)),
            Branch('3', '4', resistor('R4', R=R4)),
            Branch('4', '0', resistor('R5', R=R5)),
            Branch('0', '4', voltage_source('Uq2', V=Uq2))
        ]
    )
    Y = node_admittance_matrix(network)
    Y_ref = np.array([
        [ G1,      -G1,     0,     0],
        [-G1, G1+G2+G3,   -G3,     0],
        [  0,      -G3, G3+G4,   -G4],
        [  0,        0,   -G4, G4+G5]
        ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_matrix_from_reference_network_6() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G1, G2, G3, G4, G5 = 1/R1, 1/R2, 1/R3, 1/R4, 1/R5
    U1, U2 = 1, 2
    network = Network(
        [
            Branch('1', '0', voltage_source('Uq1', V=U1)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('2', '0', resistor('R2', R=R2)),
            Branch('2', '3', resistor('R3', R=R3)),
            Branch('3', '4', resistor('R4', R=R4)),
            Branch('4', '0', resistor('R5', R=R5)),
            Branch('3', '2', voltage_source('Uq2', V=U2))
        ]
    )
    Y = node_admittance_matrix(network)
    Y_ref = np.array([
        [ G1,      -G1,     0,     0],
        [-G1, G1+G2+G3,   -G3,     0],
        [  0,      -G3, G3+G4,   -G4],
        [  0,        0,   -G4, G4+G5]
        ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref.real)

def test_create_node_matrix_from_reference_network_7() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    G1, G2, G3, G4 = 1/R1, 1/R2, 1/R3, 1/R4
    U1, U2, U3, I4 = 1, 2, 3, 0.1
    network = Network(
        [
            Branch('1', '0', resistor('R1', R=R1)),
            Branch('2', '1', voltage_source('Us2', V=U2)),
            Branch('1', '3', resistor('R2', R=R2)),
            Branch('4', '3', voltage_source('Us3', V=U3)),
            Branch('0', '5', voltage_source('Us1', V=U1)),
            Branch('2', '5', resistor('R3', R=R3)),
            Branch('4', '5', resistor('R4', R=R4)),
            Branch('3', '5', current_source('Is4', I=I4))
        ]
    )
    Y = node_admittance_matrix(network)
    Y_ref = np.array([
        [G1+G2,   0, -G2,   0,     0],
        [    0,  G3,   0,   0,   -G3],
        [  -G2,   0,  G2,   0,     0],
        [    0,   0,   0,  G4,   -G4],
        [    0, -G3,   0, -G4, G3+G4]
        ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_matrix_from_reference_network_10() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G1, G2, G3, G4, G5 = 1/R1, 1/R2, 1/R3, 1/R4, 1/R5
    U1, U2, I3 = 1, 2, 0.1
    network = Network(
        [
            Branch('1', '0', voltage_source('Us1', V=U1)),
            Branch('1', '0', resistor('R1', R=R1)),
            Branch('2', '1', voltage_source('Us2', V=U2)),
            Branch('2', '1', resistor('R2', R=R2)),
            Branch('0', '4', resistor('R3', R=R3)),
            Branch('4', '3', current_source('Is3', I=I3)),
            Branch('3', '2', resistor('R4', R=R4)),
            Branch('2', '4', resistor('R5', R=R5)),
        ]
    )
    Y = node_admittance_matrix(network)
    Y_ref = np.array([
        [G1+G2,      -G2,   0,     0],
        [  -G2, G2+G4+G5, -G4,   -G5],
        [    0,      -G4,  G4,     0],
        [    0,      -G5,   0, G3+G5]
        ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_matrix_from_reference_network_11() -> None:
    R1, R2, R3, R4 = 15, 5, 20, 20
    G1, G2, G3, G4 = 1/R1, 1/R2, 1/R3, 1/R4
    U, I = 120, 4
    network = Network(
        branches=[
            Branch('0', '1', current_source('Is', I=I)),
            Branch('1', '0', resistor('R1', R=R1)),
            Branch('2', '1', resistor('R2', R=R2)),
            Branch('2', '0', resistor('R3', R=R3)),
            Branch('3', '2', voltage_source('Us', V=U)),
            Branch('3', '0', resistor('R4', R=R4))
        ],
        node_zero_label='0'
    )
    Y = node_admittance_matrix(network)
    Y_ref = np.array([
        [G1+G2,   -G2,   0],
        [  -G2, G2+G3,   0],
        [    0,     0,  G4]
        ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_matrix_from_reference_network_13() -> None:
    R1, R2, R3 = 10, 20, 30
    G1, G2, G3 = 1/R1, 1/R2, 1/R3
    V = 1
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('V', V=V)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('1', '2', resistor('R2', R=R2)),
            Branch('2', '0', resistor('R3', R=R3))
        ],
        node_zero_label='0'
    )
    Y = node_admittance_matrix(network)
    Y_ref = np.array([
        [ G1+G2,   -G1-G2],
        [-G1-G2, G1+G2+G3]
        ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref)