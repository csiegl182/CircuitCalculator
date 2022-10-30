from CircuitCalculator.AdvancedNodalAnalysis import create_current_vector_from_network
from CircuitCalculator.Network import Network, Branch, resistor, voltage_source, current_source
import numpy as np

def test_create_current_vector_from_reference_network_3() -> None:
    R1, R4, R5 = 10, 40, 50
    G1, G4, G5 = 1/R1, 1/R4, 1/R5
    U1, U2 = 1, 2
    network = Network(
        [
            Branch(1, 0, voltage_source(U=U1)),
            Branch(0, 4, voltage_source(U=U2)),
            Branch(1, 2, resistor(R=R1)),
            Branch(3, 4, resistor(R=R4)),
            Branch(4, 0, resistor(R=R5))
        ]
    )
    I = create_current_vector_from_network(network)
    I_ref = np.array([-U1*G1, U1*G1, -U2*G4, U2*(G4+G5)])
    np.testing.assert_almost_equal(I, I_ref)

def test_create_current_vector_from_reference_network_4() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G1, G3, G4 = 1/R1, 1/R3, 1/R4
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
    I = create_current_vector_from_network(network)
    I_ref = np.array([-U1*G1, U1*G1+U2*G3, -U2*(G4+G3), U2*G4])
    np.testing.assert_almost_equal(I, I_ref)

def test_create_current_vector_from_reference_network_5() -> None:
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
            Branch(3, 5, current_source(I=I4))
        ]
    )
    I = create_current_vector_from_network(network)
    I_ref = np.array([0, -(U1+U2)*G3, -I4, -(U1+U3)*G4, I4+U1*(G3+G4)+U2*G3+U3*G4])
    np.testing.assert_almost_equal(I, I_ref)

def test_create_current_vector_from_reference_network_8() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G1, G2, G4, G5 = 1/R1, 1/R2, 1/R4, 1/R5
    U1, U2, I4 = 1, 2, 0.1
    network = Network(
        [
            Branch(1, 0, voltage_source(U=U1)),
            Branch(1, 0, resistor(R=R1)),
            Branch(2, 1, voltage_source(U=U2)),
            Branch(2, 1, resistor(R=R2)),
            Branch(0, 3, resistor(R=R3)),
            Branch(3, 4, current_source(I=I4)),
            Branch(4, 2, resistor(R=R4)),
            Branch(2, 3, resistor(R=R5)),
        ]
    )
    I = create_current_vector_from_network(network)
    I_ref = np.array([-U1*(G1+G2)+(U1+U2)*G2, -U2*(G2+G4+G5)-U1*(G4+G5), -I4+(U1+U2)*G5, I4+(U1+U2)*G4])
    np.testing.assert_almost_equal(I, I_ref)