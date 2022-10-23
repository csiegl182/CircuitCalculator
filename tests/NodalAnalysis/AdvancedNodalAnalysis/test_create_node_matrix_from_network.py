from CircuitCalculator.AdvancedNodalAnalysis import create_node_matrix_from_network
from CircuitCalculator.Network import Network, Branch, voltage_source, resistor, current_source, conductor
import numpy as np

def test_ideal_voltage_sources_are_ignored_but_matrix_is_finite() -> None:
    network = Network([
        Branch(0, 2, voltage_source(1)),
        Branch(2, 1, voltage_source(1)),
        Branch(1, 0, conductor(1))
    ])
    Y = create_node_matrix_from_network(network)
    assert np.all(np.isfinite(Y))

def test_ideal_voltage_sources_contribute_to_dimension_of_matrix() -> None:
    network = Network([
        Branch(0, 2, voltage_source(1)),
        Branch(2, 1, voltage_source(1)),
        Branch(1, 0, conductor(1))
    ])
    Y = create_node_matrix_from_network(network)

    assert Y.shape == (network.number_of_nodes-1, network.number_of_nodes-1)

def test_create_node_matrix_from_reference_network_3() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G1, G2, G3, G4 = 1/R1, 1/R2, 1/R3, 1/R4
    U1, U2 = 1, 2
    network = Network(
        [
            Branch(1, 0, voltage_source(U=U1)),
            Branch(0, 4, voltage_source(U=U2)),
            Branch(1, 2, resistor(R=R1)),
            Branch(2, 0, resistor(R=R2)),
            Branch(2, 3, resistor(R=R3)),
            Branch(3, 4, resistor(R=R4)),
            Branch(4, 0, resistor(R=R5))
        ]
    )
    Y = create_node_matrix_from_network(network)
    Y_ref = np.array([[-1, -G1, 0, 0], [0, G1+G2+G3, -G3, 0], [0, -G3, G3+G4, 0], [0, 0, -G4, 1]])
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_matrix_from_reference_network_4() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G1, G2, G4, G5 = 1/R1, 1/R2, 1/R4, 1/R5
    U1, U2 = 1, 2
    network = Network(
        [
            Branch(1, 0, voltage_source(U=U1)),
            Branch(3, 2, voltage_source(U=U2)),
            Branch(1, 2, resistor(R=R1)),
            Branch(2, 0, resistor(R=R2)),
            Branch(2, 3, resistor(R=R3)),
            Branch(3, 4, resistor(R=R4)),
            Branch(4, 0, resistor(R=R5))
        ]
    )
    Y = create_node_matrix_from_network(network)
    Y_ref = np.array([[-1, -G1, 0, 0], [0, G1+G2, 1, 0], [0, G4, -1, -G4], [0, -G4, 0, G4+G5]])
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_matrix_from_reference_network_5() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    G1, G2, G3, G4 = 1/R1, 1/R2, 1/R3, 1/R4
    U1, U2, U3, I4 = 1, 2, 3, 0.1
    network = Network(
        [
            Branch(0, 5, voltage_source(U=U1)),
            Branch(0, 1, resistor(R=R1)),
            Branch(2, 1, voltage_source(U=U2)),
            Branch(2, 5, resistor(R=R3)),
            Branch(1, 3, resistor(R=R2)),
            Branch(4, 3, voltage_source(U=U3)),
            Branch(4, 5, resistor(R=R4)),
            Branch(5, 0, current_source(I=I4))
        ]
    )
    Y = create_node_matrix_from_network(network)
    Y_ref = np.array([[G1+G2, 1, -G2, 0, 0], [G3, -1, 0, 0, 0], [-G2, 0, G2, 1, 0], [0, 0, G4, -1, 0], [-G3, 0, -G4, 0, 1]])
    np.testing.assert_almost_equal(Y, Y_ref)