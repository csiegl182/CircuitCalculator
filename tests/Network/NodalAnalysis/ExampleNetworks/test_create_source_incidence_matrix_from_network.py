from CircuitCalculator.Network.NodalAnalysis.node_analysis import source_incidence_matrix
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor, voltage_source, current_source
from CircuitCalculator.Network.NodalAnalysis.label_mapping import default_label_mappings_factory
import numpy as np

def test_source_incidence_matrix_from_reference_network_1() -> None:
    Vq = 1+0j
    R = 1
    network = Network(
        [
            Branch('1', '0', voltage_source('Uq', V=Vq)),
            Branch('1', '0', resistor('R1', R=R))
        ]
    )
    Q = source_incidence_matrix(network, default_label_mappings_factory(network))
    Q_ref = np.empty((1,0), dtype=complex)
    np.testing.assert_almost_equal(Q, Q_ref)

def test_source_incidence_matrix_from_reference_network_2() -> None:
    Iq = 1+0j
    R = 1
    network = Network(
        [
            Branch('0', '1', current_source('Iq', I=Iq)),
            Branch('1', '0', resistor('R1', R=R))
        ]
    )
    Q = source_incidence_matrix(network, default_label_mappings_factory(network))
    Q_ref = np.array([[1]], dtype=complex)
    np.testing.assert_almost_equal(Q, Q_ref)

def test_source_incidence_matrix_from_reference_network_3() -> None:
    R1, R2, Ri = 10, 20, 100
    Iq = 1
    network = Network(
        [
            Branch('0', '1', current_source('Iq1', I=Iq, Y=1/Ri)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('2', '0', resistor('R2', R=R2))
        ]
    )
    Q = source_incidence_matrix(network, default_label_mappings_factory(network))
    Q_ref = np.array([[1],
                      [0]], dtype=complex)
    np.testing.assert_almost_equal(Q, Q_ref)

def test_source_incidence_matrix_from_reference_network_4() -> None:
    R1, R2, R3 = 10, 20, 30
    G2 = 1/R2
    Uq = 1
    network = Network(
        [
            Branch('1', '0', voltage_source('Uq', V=Uq)),
            Branch('1', '0', resistor('R1', R=R1)),
            Branch('1', '2', resistor('R2', R=R2)),
            Branch('2', '0', resistor('R3', R=R3))
        ]
    )
    Q = source_incidence_matrix(network, default_label_mappings_factory(network))
    Q_ref = np.empty((2, 0), dtype=complex)
    np.testing.assert_almost_equal(Q, Q_ref)

def test_source_incidence_matrix_from_reference_network_5() -> None:
    R1, R4, R5 = 10, 40, 50
    G1, G4 = 1/R1, 1/R4
    U1, U2 = 1, 2
    network = Network(
        [
            Branch('1', '0', voltage_source('Uq1', V=U1)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('3', '4', resistor('R4', R=R4)),
            Branch('4', '0', resistor('R5', R=R5)),
            Branch('0', '4', voltage_source('Uq2', V=U2))
        ]
    )
    Q = source_incidence_matrix(network, default_label_mappings_factory(network))
    Q_ref = np.empty((4,0), dtype=complex)
    np.testing.assert_almost_equal(Q, Q_ref)

def test_source_incidence_matrix_from_reference_network_6() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G1, G3, G4 = 1/R1, 1/R3, 1/R4
    V1, V2 = 1, 2
    network = Network(
        [
            Branch('1', '0', voltage_source('Us1', V=V1)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('2', '0', resistor('R2', R=R2)),
            Branch('2', '3', resistor('R3', R=R3)),
            Branch('3', '4', resistor('R4', R=R4)),
            Branch('4', '0', resistor('R5', R=R5)),
            Branch('3', '2', voltage_source('Us2', V=V2))
        ]
    )
    Q = source_incidence_matrix(network, default_label_mappings_factory(network))
    Q_ref = np.empty((4, 0), dtype=complex)
    np.testing.assert_almost_equal(Q, Q_ref)

def test_source_incidence_matrix_from_reference_network_7() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    V1, V2, V3, I4 = 1, 2, 3, 0.1
    network = Network(
        [
            Branch('0', '1', resistor('R1', R=R1)),
            Branch('2', '1', voltage_source('Us2', V=V2)),
            Branch('1', '3', resistor('R2', R=R2)),
            Branch('4', '3', voltage_source('Us3', V=V3)),
            Branch('2', '5', resistor('R3', R=R3)),
            Branch('4', '5', resistor('R4', R=R4)),
            Branch('3', '5', current_source('Is4', I=I4)),
            Branch('0', '5', voltage_source('Us1', V=V1))
        ]
    )
    Q = source_incidence_matrix(network, default_label_mappings_factory(network))
    Q_ref = np.array([
        [ 0],
        [ 0],
        [-1],
        [ 0],
        [ 1]
        ], dtype=complex)
    np.testing.assert_almost_equal(Q, Q_ref)

def test_source_incidence_matrix_from_reference_network_10() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    V1, V2, I4 = 1, 2, 0.1
    network = Network(
        [
            Branch('1', '0', voltage_source('Us1', V=V1)),
            Branch('1', '0', resistor('R1', R=R1)),
            Branch('2', '1', voltage_source('Us2', V=V2)),
            Branch('2', '1', resistor('R2', R=R2)),
            Branch('0', '4', resistor('R3', R=R3)),
            Branch('4', '3', current_source('Is4', I=I4)),
            Branch('3', '2', resistor('R4', R=R4)),
            Branch('2', '4', resistor('R5', R=R5)),
        ]
    )
    Q = source_incidence_matrix(network, default_label_mappings_factory(network))
    Q_ref = np.array([
        [ 0],
        [ 0],
        [ 1],
        [-1]
        ], dtype=complex)
    np.testing.assert_almost_equal(Q, Q_ref)

def test_source_incidence_matrix_from_reference_network_13() -> None:
    R1, R2, R3 = 10, 20, 30
    G1, G2 = 1/R1, 1/R2
    V = 1
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('V', V=V)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('1', '2', resistor('R2', R=R2)),
            Branch('2', '0', resistor('R3', R=R3))
        ],
        reference_node_label='0'
    )
    Q = source_incidence_matrix(network, default_label_mappings_factory(network))
    Q_ref = np.empty((2, 0), dtype=complex)
    np.testing.assert_almost_equal(Q, Q_ref)