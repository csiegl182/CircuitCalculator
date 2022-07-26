from AdvancedNodalAnalysis import create_current_vector_from_network
from Network import Network, Branch, resistor, voltage_source
import numpy as np

def test_create_current_vector_from_reference_network() -> None:
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