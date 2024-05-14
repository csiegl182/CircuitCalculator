from CircuitCalculator.Network.NodalAnalysis.node_analysis import create_node_matrix_from_network
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import conductor
import numpy as np

def test_node_admittance_matrix_is_correct() -> None:
    Y_12, Y_20, Y_23, Y_34, Y_40 = 1, 2, 3, 4, 5
    Y_ref = np.array([
        [ Y_20+Y_40,     0,          -Y_20,         0,     -Y_40],
        [         0,  Y_12,          -Y_12,         0,         0],
        [     -Y_20, -Y_12, Y_12+Y_20+Y_23,     -Y_23,         0],
        [         0,     0,          -Y_23, Y_23+Y_34,     -Y_34],
        [     -Y_40,     0,              0,     -Y_34, Y_34+Y_40]])

    network = Network([
        Branch('1', '2', conductor('Y_12', Y_12)),
        Branch('2', '0', conductor('Y_20', Y_20)),
        Branch('2', '3', conductor('Y_23', Y_23)),
        Branch('3', '4', conductor('Y_34', Y_34)),
        Branch('4', '0', conductor('Y_40', Y_40))
    ])
    Y = create_node_matrix_from_network(network)

    np.testing.assert_almost_equal(Y, Y_ref)

def test_node_admittance_matrix_sorts_node_indices() -> None:
    Y_10, Y_20, Y_12 = 1, 2, 3
    Y_ref = np.array([
        [Y_10+Y_20,     -Y_10,     -Y_20],
        [    -Y_10, Y_10+Y_12,     -Y_12],
        [    -Y_20,     -Y_12, Y_20+Y_12]
        ])

    network = Network([
        Branch('1', '0', conductor('Y_10', Y_10)),
        Branch('2', '0', conductor('Y_20', Y_20)),
        Branch('2', '1', conductor('Y_12', Y_12))
    ])
    Y = create_node_matrix_from_network(network)

    np.testing.assert_almost_equal(Y, Y_ref)
