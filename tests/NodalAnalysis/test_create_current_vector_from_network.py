from CircuitCalculator.NodalAnalysis import create_current_vector_from_network
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor, voltage_source, current_source, linear_current_source, linear_voltage_source
import numpy as np

def test_create_current_vector_from_reference_network_1() -> None:
    R1, R2, Ri = 10, 20, 100
    Iq = 1
    network = Network(
        [
            Branch('0', '1', linear_current_source('Is1', I=Iq, R=Ri)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('2', '0', resistor('R2', R=R2))
        ]
    )
    I = create_current_vector_from_network(network)
    I_ref = np.array([Iq, 0])
    np.testing.assert_almost_equal(I, I_ref)

def test_create_current_vector_from_reference_network_3() -> None:
    R1, R4, R5 = 10, 40, 50
    G1, G4, G5 = 1/R1, 1/R4, 1/R5
    U1, U2 = 1, 2
    network = Network(
        [
            Branch('1', '0', voltage_source('Us1', U=U1)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('3', '4', resistor('R2', R=R4)),
            Branch('4', '0', resistor('R3', R=R5)),
            Branch('0', '4', voltage_source('Us2', U=U2))
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
            Branch('1', '0', voltage_source('Us1', U=U1)),
            Branch('1', '2', resistor('R1', R=R1)),
            Branch('2', '0', resistor('R2', R=R2)),
            Branch('2', '3', resistor('R3', R=R3)),
            Branch('3', '4', resistor('R4', R=R4)),
            Branch('4', '0', resistor('R5', R=R5)),
            Branch('3', '2', voltage_source('Us2', U=U2))
        ]
    )
    I = create_current_vector_from_network(network)
    I_ref = np.array([-U1*G1, U1*G1-U2*G4, -U2*(G4+G3), U2*G4])
    np.testing.assert_almost_equal(I.real, I_ref.real)

def test_create_current_vector_from_reference_network_5() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    G1, G2, G3, G4 = 1/R1, 1/R2, 1/R3, 1/R4
    U1, U2, U3, I4 = 1, 2, 3, 0.1
    network = Network(
        [
            Branch('0', '1', resistor('R1', R=R1)),
            Branch('2', '1', voltage_source('Us2', U=U2)),
            Branch('1', '3', resistor('R2', R=R2)),
            Branch('4', '3', voltage_source('Us3', U=U3)),
            Branch('2', '5', resistor('R3', R=R3)),
            Branch('4', '5', resistor('R4', R=R4)),
            Branch('3', '5', current_source('Is4', I=I4)),
            Branch('0', '5', voltage_source('Us1', U=U1))
        ]
    )
    I = create_current_vector_from_network(network)
    I_ref = np.array([-(U1+U2)*G3, -(U1+U2)*G3, -I4-(U1+U3)*G4, -(U1+U3)*G4, I4+G3*(U1+U2)+G4*(U1+U3)])
    np.testing.assert_almost_equal(I.real, I_ref.real)

def test_create_current_vector_from_reference_network_8() -> None:
    R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
    G1, G2, G4, G5 = 1/R1, 1/R2, 1/R4, 1/R5
    U1, U2, I4 = 1, 2, 0.1
    network = Network(
        [
            Branch('1', '0', voltage_source('Us1', U=U1)),
            Branch('1', '0', resistor('R1', R=R1)),
            Branch('2', '1', voltage_source('Us2', U=U2)),
            Branch('2', '1', resistor('R2', R=R2)),
            Branch('0', '3', resistor('R3', R=R3)),
            Branch('3', '4', current_source('Is4', I=I4)),
            Branch('4', '2', resistor('R4', R=R4)),
            Branch('2', '3', resistor('R5', R=R5)),
        ]
    )
    I = create_current_vector_from_network(network)
    I_ref = np.array([-U1*G1+U2*G2, -(U1+U2)*(G4+G5)-U2*G2, -I4+(U1+U2)*G5, I4+(U1+U2)*G4])
    np.testing.assert_almost_equal(I.real, I_ref.real)

def test_create_current_vektor_from_reference_network_11() -> None:
    R, Ri = 2, 2
    Uq = 9
    network = Network(
        branches=[
            Branch('1', '0', linear_voltage_source('Us1', U=Uq, R=Ri)),
            Branch('1', '0', resistor('R1', R=R))
        ],
        zero_node_label='0'
    )
    I = create_current_vector_from_network(network)
    I_ref = np.array([-Uq/Ri])
    np.testing.assert_almost_equal(I.real, I_ref.real)