from NodalAnalysis import create_node_admittance_matrix_from_network
from Network import Network, Branch, conductor
import numpy as np

def test_node_admittance_matrix_is_correct() -> None:
    Y_10, Y_20, Y_12 = 1, 2, 3
    Y_ref = np.array([[Y_10+Y_12, -Y_12], [-Y_12, Y_20+Y_12]])

    network = Network()
    network.add_branch(Branch(1, 0, conductor(Y_10)))
    network.add_branch(Branch(1, 2, conductor(Y_12)))
    network.add_branch(Branch(2, 0, conductor(Y_20)))
    Y = create_node_admittance_matrix_from_network(network)

    np.testing.assert_almost_equal(Y, Y_ref)

def test_node_admittance_matrix_sorts_node_indices() -> None:
    Y_10, Y_20, Y_12 = 1, 2, 3
    Y_ref = np.array([[Y_10+Y_12, -Y_12], [-Y_12, Y_20+Y_12]])

    network = Network()
    network.add_branch(Branch(2, 0, conductor(Y_20)))
    network.add_branch(Branch(2, 1, conductor(Y_12)))
    network.add_branch(Branch(1, 0, conductor(Y_10)))
    Y = create_node_admittance_matrix_from_network(network)

    np.testing.assert_almost_equal(Y, Y_ref)
    

    