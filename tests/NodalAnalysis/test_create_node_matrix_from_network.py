from CircuitCalculator.Network.NodalAnalysis import create_node_matrix_from_network
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import voltage_source, conductor
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