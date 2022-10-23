from CircuitCalculator.ClassicNodalAnalysis import create_node_admittance_matrix_from_network
from CircuitCalculator.Network import Network, Branch, conductor, voltage_source
import numpy as np

def test_node_admittance_matrix_is_correct() -> None:
    Y_12, Y_20, Y_23, Y_34, Y_40 = 1, 2, 3, 4, 5
    Y_ref = np.array([[Y_12, -Y_12, 0, 0], [-Y_12, Y_12+Y_20+Y_23, -Y_23, 0], [0, -Y_23, Y_23+Y_34, -Y_34], [0, 0, -Y_34, Y_34+Y_40]])

    network = Network([
        Branch(1, 2, conductor(Y_12)),
        Branch(2, 0, conductor(Y_20)),
        Branch(2, 3, conductor(Y_23)),
        Branch(3, 4, conductor(Y_34)),
        Branch(4, 0, conductor(Y_40))
    ])
    Y = create_node_admittance_matrix_from_network(network)

    np.testing.assert_almost_equal(Y, Y_ref)

def test_node_admittance_matrix_sorts_node_indices() -> None:
    Y_10, Y_20, Y_12 = 1, 2, 3
    Y_ref = np.array([[Y_10+Y_12, -Y_12], [-Y_12, Y_20+Y_12]])

    network = Network([
        Branch(2, 0, conductor(Y_20)),
        Branch(2, 1, conductor(Y_12)),
        Branch(1, 0, conductor(Y_10))
    ])
    Y = create_node_admittance_matrix_from_network(network)

    np.testing.assert_almost_equal(Y, Y_ref)

def test_ideal_voltage_sources_are_ignored_but_matrix_is_finite() -> None:
    network = Network([
        Branch(0, 2, voltage_source(1)),
        Branch(2, 1, voltage_source(1)),
        Branch(1, 0, conductor(1))
    ])
    Y = create_node_admittance_matrix_from_network(network)
    assert np.all(np.isfinite(Y))

def test_ideal_voltage_sources_contribute_to_dimension_of_matrix() -> None:
    network = Network([
        Branch(0, 2, voltage_source(1)),
        Branch(2, 1, voltage_source(1)),
        Branch(1, 0, conductor(1))
    ])
    Y = create_node_admittance_matrix_from_network(network)

    assert Y.shape == (network.number_of_nodes-1, network.number_of_nodes-1)
    