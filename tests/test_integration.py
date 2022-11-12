import pytest
from CircuitCalculator.Network import load_network_from_json
from CircuitCalculator.ClassicNodalAnalysis import nodal_analysis_solver as classic_nodal_analysis_solver
from CircuitCalculator.AdvancedNodalAnalysis import nodal_analysis_solver as advanced_nodal_analysis_solver
import numpy as np

def test_network_1_with_classic_nodal_analysis() -> None:
    network = load_network_from_json('./examples/example_network_1.json')
    solution = classic_nodal_analysis_solver(network)
    R1, R2, I1 = tuple(network.branches)
    np.testing.assert_almost_equal(solution.get_voltage(R1), 7.69, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R2), 15.38, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(I1), -23.08, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R1), 0.77, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R2), 0.77, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(I1), -0.23, decimal=2)

def test_network_2_with_classic_nodal_analysis() -> None:
    network = load_network_from_json('./examples/example_network_2.json')
    with pytest.raises(ValueError):
        classic_nodal_analysis_solver(network)

def test_network_2_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/example_network_2.json')
    solution = advanced_nodal_analysis_solver(network)
    R1, R2, R3, U1 = tuple(network.branches)
    np.testing.assert_almost_equal(solution.get_voltage(R1), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R2), 0.40, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R3), 0.60, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(U1), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R1), 0.10, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R2), 0.02, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R3), 0.02, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(U1), 0.12, decimal=2)

def test_network_3_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/example_network_3.json')
    solution = advanced_nodal_analysis_solver(network)
    R1, R2, R3, R4, R5, U1, U2 = tuple(network.branches)
    np.testing.assert_almost_equal(solution.get_voltage(R1), 0.56, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R2), 0.44, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R3), 1.04, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R4), 1.39, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R5), -2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(U1), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(U2), 2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R1), 0.056, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(R2), 0.022, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(R3), 0.035, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(R4), 0.035, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(R5), -0.04, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(U1), 0.056, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(U2), 0.075, decimal=3)

def test_network_4_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/example_network_4.json')
    solution = advanced_nodal_analysis_solver(network)
    R1, R2, R3, R4, R5, U1, U2 = tuple(network.branches)
    np.testing.assert_almost_equal(solution.get_voltage(R1), 0.52, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R2), 0.48, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R3), -2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R4), 1.10, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R5), 1.38, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(U1), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(U2), 2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R1), 0.052, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(R2), 0.024, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(R3), -0.067, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(R4), 0.028, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(R5), 0.028, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(U1), 0.052, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(U2), 0.094, decimal=3)

def test_network_8_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/example_network_8.json')
    solution = advanced_nodal_analysis_solver(network)
    R1, R2, R3, R4, R5, U1, U2, I3 = tuple(network.branches)
    np.testing.assert_almost_equal(solution.get_voltage(R1), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R2), 2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R3), -0.75, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R4), -4.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R5), 3.75, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(U1), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(U2), 2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(I3), -7.75, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R1), 0.10, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R2), 0.10, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R3), -0.025, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(R4), -0.10, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(R5), 0.075, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(U1), 0.075, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(U2), 0.075, decimal=3)
    np.testing.assert_almost_equal(solution.get_current(I3), 0.10, decimal=3)

def test_network_9_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/example_network_9.json')
    solution = advanced_nodal_analysis_solver(network)
    I1, R1, R2, R3, Uq, R4 = tuple(network.branches)
    np.testing.assert_almost_equal(solution.get_voltage(R4), 100, decimal=2)