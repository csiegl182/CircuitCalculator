from CircuitCalculator.Network.NodalAnalysis import create_node_matrix_from_network
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor, voltage_source, current_source, linear_current_source, linear_voltage_source, conductor
import numpy as np

def test_ideal_voltage_sources_are_ignored_but_matrix_is_finite() -> None:
    network = Network([
        Branch('0', '2', voltage_source('Us1', 1)),
        Branch('2', '1', voltage_source('Us2', 1)),
        Branch('1', '0', conductor('G', 1))
    ])
    Y = create_node_matrix_from_network(network)
    assert np.all(np.isfinite(Y))

def test_ideal_voltage_sources_contribute_to_dimension_of_matrix() -> None:
    network = Network([
        Branch('0', '2', voltage_source('Us1', 1)),
        Branch('2', '1', voltage_source('Us2', 1)),
        Branch('1', '0', conductor('G', 1))
    ])
    Y = create_node_matrix_from_network(network)

    assert Y.shape == (network.number_of_nodes-1, network.number_of_nodes-1)

def test_create_node_matrix_from_reference_network_1() -> None:
    R1, R2, Ri = 10, 20, 100
    G1, G2, Gi = 1/R1, 1/R2, 1/Ri
    Iq = 1
    network = Network(
        [
            Branch('0', '1', linear_current_source('Is', I=Iq, Y=1/Ri)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('2', '0', resistor('R2', R=R2))
        ]
    )
    Y = create_node_matrix_from_network(network)
    Y_ref = np.array([[G1+Gi, -G1], [-G1, G1+G2]])
    np.testing.assert_almost_equal(Y.real, Y_ref.real)

def test_create_node_matrix_from_reference_network_3() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G1, G2, G3, G4 = 1/R1, 1/R2, 1/R3, 1/R4
    U1, U2 = 1, 2
    network = Network(
        [
            Branch('1', '0', voltage_source('Us1', U=U1)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('2', '0', resistor('R2', R=R2)),
            Branch('2', '3', resistor('R3', R=R3)),
            Branch('3', '4', resistor('R4', R=R4)),
            Branch('4', '0', resistor('R5', R=R5)),
            Branch('0', '4', voltage_source('Us2', U=U2))
        ]
    )
    Y = create_node_matrix_from_network(network)
    Y_ref = np.array([[-1, -G1, 0, 0], [0, G1+G2+G3, -G3, 0], [0, -G3, G3+G4, 0], [0, 0, -G4, 1]], np.double)
    np.testing.assert_almost_equal(Y.real, Y_ref.real)

def test_create_node_matrix_from_reference_network_4() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G1, G2, G4, G5 = 1/R1, 1/R2, 1/R4, 1/R5
    U1, U2 = 1, 2
    network = Network(
        [
            Branch('1', '0', voltage_source('Us1', U=U1)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('2', '0', resistor('R2', R=R2)),
            Branch('2', '3', resistor('R3', R=R3)),
            Branch('3', '4', resistor('R4', R=R4)),
            Branch('4', '0', resistor('R5', R=R5)),
            Branch('3', '2', voltage_source('Us2', U=U2))
        ]
    )
    Y = create_node_matrix_from_network(network)
    Y_ref = np.array([[-1, -G1, 0, 0], [0, G1+G2+G4, 0, -G4], [0, G4, -1, -G4], [0, -G4, 0, G4+G5]], np.double)
    np.testing.assert_almost_equal(Y.real, Y_ref.real)

def test_create_node_matrix_from_reference_network_5() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    G1, G2, G3, G4 = 1/R1, 1/R2, 1/R3, 1/R4
    U1, U2, U3, I4 = 1, 2, 3, 0.1
    network = Network(
        [
            Branch('0', '1', resistor('R1', R=R1)),
            Branch('2', '1', voltage_source('Us2', U=U2)),
            Branch('1', '3', resistor('R2', R=R2)),
            Branch('4', '3', voltage_source('Us3', U=U3)),
            Branch('0', '5', voltage_source('Us1', U=U1)),
            Branch('2', '5', resistor('R3', R=R3)),
            Branch('4', '5', resistor('R4', R=R4)),
            Branch('5', '0', current_source('Is4', I=I4))
        ]
    )
    Y = create_node_matrix_from_network(network)
    print(Y.real)
    Y_ref = np.array([[G1+G2+G3, 0, -G2, 0, 0], [G3, -1, 0, 0, 0], [-G2, 0, G2+G4, 0, 0], [0, 0, G4, -1, 0], [-G3, 0, -G4, 0, 1]], np.double)
    print(Y_ref.real)
    np.testing.assert_almost_equal(Y.real, Y_ref.real)

def test_create_node_matrix_from_reference_network_8() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G3, G4, G5 = 1/R3, 1/R4, 1/R5
    U1, U2, I3 = 1, 2, 0.1
    network = Network(
        [
            Branch('1', '0', voltage_source('Us1', U=U1)),
            Branch('1', '0', resistor('R1', R=R1)),
            Branch('2', '1', voltage_source('Us2', U=U2)),
            Branch('2', '1', resistor('R2', R=R2)),
            Branch('0', '3', resistor('R3', R=R3)),
            Branch('3', '4', current_source('Is3', I=I3)),
            Branch('4', '2', resistor('R4', R=R4)),
            Branch('2', '3', resistor('R5', R=R5)),
        ]
    )
    Y = create_node_matrix_from_network(network)
    Y_ref = np.array([[-1, 1, 0, 0], [0, -1, -G5, -G4], [0, 0, G3+G5, 0], [0, 0, 0, G4]], np.double)
    np.testing.assert_almost_equal(Y.real, Y_ref.real)

def test_create_node_matrix_from_reference_network_9() -> None:
    R1, R2, R3, R4 = 15, 5, 20, 20
    G1, G2, G3, G4 = 1/R1, 1/R2, 1/R3, 1/R4
    U, I = 120, 4
    network = Network(
        branches=[
            Branch('0', '1', current_source('Is', I=I)),
            Branch('1', '0', resistor('R1', R=R1)),
            Branch('2', '1', resistor('R2', R=R2)),
            Branch('2', '0', resistor('R3', R=R3)),
            Branch('3', '2', voltage_source('Us', U=U)),
            Branch('3', '0', resistor('R4', R=R4))
        ],
        node_zero_label='0'
    )
    Y = create_node_matrix_from_network(network)
    Y_ref = np.array([[G1+G2, -G2, 0], [-G2, G2+G3+G4, 0], [0, G4, -1]], np.double)
    np.testing.assert_almost_equal(Y.real, Y_ref.real)

def test_create_node_matrix_from_reference_network_11() -> None:
    R, Ri = 2, 1
    G, Gi = 1/R, 1/Ri
    Uq = 9
    network = Network(
        branches=[
            Branch('1', '0', linear_voltage_source('Us', U=Uq, Z=Ri)),
            Branch('1', '0', resistor('R', R=R))
        ],
        node_zero_label='0'
    )
    Y = create_node_matrix_from_network(network)
    Y_ref = np.array([[G+Gi]])
    np.testing.assert_almost_equal(Y.real, Y_ref.real)