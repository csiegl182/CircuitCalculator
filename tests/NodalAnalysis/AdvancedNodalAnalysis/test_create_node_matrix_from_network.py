from CircuitCalculator.AdvancedNodalAnalysis import create_node_matrix_from_network
from CircuitCalculator.Network import Network, Branch, voltage_source, resistor
import numpy as np

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