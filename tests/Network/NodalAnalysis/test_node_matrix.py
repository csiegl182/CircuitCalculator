from CircuitCalculator.Network.NodalAnalysis.node_analysis_calculations import node_admittance_matrix
from CircuitCalculator.Network.NodalAnalysis.label_mapping import default_label_mappings_factory
from CircuitCalculator.Network.NodalAnalysis.matrix_operations import NumPyMatrixOperations
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import voltage_source, conductor
import numpy as np

def test_ideal_voltage_sources_are_ignored_but_matrix_is_finite() -> None:
    network = Network([
        Branch('0', '2', voltage_source('Us1', 1)),
        Branch('2', '1', voltage_source('Us2', 1)),
        Branch('1', '0', conductor('G', 1))
    ])
    Y = node_admittance_matrix(network, NumPyMatrixOperations(), default_label_mappings_factory(network))
    assert np.all(np.isfinite(Y))

def test_node_admittance_matrix_is_correct() -> None:
    Y_12, Y_20, Y_23, Y_34, Y_40 = 1, 2, 3, 4, 5
    Y_ref = np.array([
        [ Y_12,          -Y_12,         0,         0],
        [-Y_12, Y_12+Y_20+Y_23,     -Y_23,         0],
        [    0,          -Y_23, Y_23+Y_34,     -Y_34],
        [    0,              0,     -Y_34, Y_34+Y_40]])

    network = Network([
        Branch('1', '2', conductor('Y_12', Y_12)),
        Branch('2', '0', conductor('Y_20', Y_20)),
        Branch('2', '3', conductor('Y_23', Y_23)),
        Branch('3', '4', conductor('Y_34', Y_34)),
        Branch('4', '0', conductor('Y_40', Y_40))
    ])
    Y = node_admittance_matrix(network, NumPyMatrixOperations(), default_label_mappings_factory(network))

    np.testing.assert_almost_equal(Y, Y_ref)

def test_node_admittance_matrix_sorts_node_indices() -> None:
    Y_10, Y_20, Y_12 = 1, 2, 3
    Y_ref = np.array([
        [Y_10+Y_12,     -Y_12],
        [    -Y_12, Y_20+Y_12]
        ])

    network = Network([
        Branch('1', '0', conductor('Y_10', Y_10)),
        Branch('2', '0', conductor('Y_20', Y_20)),
        Branch('2', '1', conductor('Y_12', Y_12))
    ])
    Y = node_admittance_matrix(network, NumPyMatrixOperations(), default_label_mappings_factory(network))

    np.testing.assert_almost_equal(Y, Y_ref)

def test_node_admittance_matrix_contains_nan_values_when_conductance_is_nan() -> None:
    Y_10, Y_20, Y_12 = 1, 2, np.nan
    network = Network([
        Branch('1', '0', conductor('Y_10', Y_10)),
        Branch('2', '0', conductor('Y_20', Y_20)),
        Branch('2', '1', conductor('Y_12', Y_12))
    ])
    Y = node_admittance_matrix(network, NumPyMatrixOperations(), default_label_mappings_factory(network))

    assert np.any(np.isnan(Y))
