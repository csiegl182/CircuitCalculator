import pytest
from Network import load_network_from_json
from ClassicNodalAnalysis import nodal_analysis_solver as classic_nodal_analysis_solver
from AdvancedNodalAnalysis import nodal_analysis_solver as advanced_nodal_analysis_solver
import numpy as np

def test_network_1_with_classic_nodal_analysis() -> None:
    network = load_network_from_json('./example_network_1.json')
    solution = classic_nodal_analysis_solver(network)
    R1, R2, I1 = tuple(network.branches)
    np.testing.assert_almost_equal(solution.get_voltage(R1), 7.69, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R2), 15.38, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(I1), -23.08, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R1), 0.77, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R2), 0.77, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(I1), -0.23, decimal=2)

def test_network_1_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./example_network_1.json')
    solution = advanced_nodal_analysis_solver(network)
    R1, R2, I1 = tuple(network.branches)
    np.testing.assert_almost_equal(solution.get_voltage(R1), 7.69, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(R2), 15.38, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage(I1), -23.08, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R1), 0.77, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(R2), 0.77, decimal=2)
    np.testing.assert_almost_equal(solution.get_current(I1), -0.23, decimal=2)

def test_network_2_with_classic_nodal_analysis() -> None:
    network = load_network_from_json('./example_network_2.json')
    with pytest.raises(ValueError):
        solution = classic_nodal_analysis_solver(network)

def test_network_2_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./example_network_2.json')
    solution = advanced_nodal_analysis_solver(network)
    assert False