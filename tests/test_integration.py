from CircuitCalculator.Network.loaders import load_network_from_json
from CircuitCalculator.Network.NodalAnalysis import nodal_analysis_solver
from CircuitCalculator.Network.impedance import open_circuit_impedance
import numpy as np

def test_network_1_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/networks/json/example_network_1.json')
    solution = nodal_analysis_solver(network)
    np.testing.assert_almost_equal(solution.get_current('Uq'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('Uq'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R'), 1.00, decimal=2)

def test_network_2_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/networks/json/example_network_2.json')
    solution = nodal_analysis_solver(network)
    np.testing.assert_almost_equal(solution.get_current('Iq'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('Iq'), -1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R'), 1.00, decimal=2)

def test_network_3_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/networks/json/example_network_3.json')
    solution = nodal_analysis_solver(network)
    np.testing.assert_almost_equal(solution.get_voltage('R1'), 7.69, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R2'), 15.38, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('I1'), -23.08, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R1'), 0.77, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R2'), 0.77, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('I1'), -0.23, decimal=2)

def test_network_4_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/networks/json/example_network_4.json')
    solution = nodal_analysis_solver(network)
    np.testing.assert_almost_equal(solution.get_voltage('R1'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R2'), 0.40, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R3'), 0.60, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('U1'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R1'), 0.10, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R2'), 0.02, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R3'), 0.02, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('U1'), 0.12, decimal=2)

def test_network_5_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/networks/json/example_network_5.json')
    solution = nodal_analysis_solver(network)
    np.testing.assert_almost_equal(solution.get_voltage('R1'), 0.56, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R2'), 0.44, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R3'), 1.04, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R4'), 1.39, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R5'), -2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('U1'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('U2'), 2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R1'), 0.056, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R2'), 0.022, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R3'), 0.035, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R4'), 0.035, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R5'), -0.04, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('U1'), 0.056, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('U2'), 0.075, decimal=3)
    
def test_network_6_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/networks/json/example_network_6.json')
    solution = nodal_analysis_solver(network)
    np.testing.assert_almost_equal(solution.get_voltage('R1'), 0.52, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R2'), 0.48, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R3'), -2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R4'), 1.10, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R5'), 1.38, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('U1'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('U2'), 2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R1'), 0.052, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R2'), 0.024, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R3'), -0.067, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R4'), 0.028, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R5'), 0.028, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('U1'), 0.052, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('U2'), 0.094, decimal=3)

def test_network_7_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/networks/json/example_network_7.json')
    solution = nodal_analysis_solver(network)
    np.testing.assert_almost_equal(solution.get_voltage('R1'), -1.56, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R2'), 2.14, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R3'), 1.44, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R4'), 0.30, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('U1'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('U2'), 2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('U3'), 3.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('I4'), -2.7, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R1'), -0.156, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R2'), 0.107, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R3'), 0.048, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R4'), 0.0075, decimal=4)
    np.testing.assert_almost_equal(solution.get_current('U1'), 0.156, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('U2'), 0.048, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('U3'), 0.0075, decimal=4)
    np.testing.assert_almost_equal(solution.get_current('I4'), 0.1, decimal=3)

def test_network_8_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/networks/json/example_network_8.json')
    Rges = open_circuit_impedance(network, '1', '2').real
    np.testing.assert_almost_equal(Rges, 4.66, decimal=2)

def test_network_9_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/networks/json/example_network_9.json')
    solution = nodal_analysis_solver(network)
    np.testing.assert_almost_equal(solution.get_voltage('Vs1'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('Vs2'), 2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R1'), 3.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('Vs1'), 0.30, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('Vs2'), 0.30, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R1'), 0.30, decimal=3)

def test_network_10_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/networks/json/example_network_10.json')
    solution = nodal_analysis_solver(network)
    np.testing.assert_almost_equal(solution.get_voltage('R1'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R2'), 2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R3'), -0.75, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R4'), -4.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R5'), 3.75, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('U1'), 1.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('U2'), 2.00, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('I3'), -7.75, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R1'), 0.10, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R2'), 0.10, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R3'), -0.025, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R4'), -0.10, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R5'), 0.075, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('U1'), 0.075, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('U2'), 0.075, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('I3'), 0.10, decimal=3)

def test_network_11_with_advanced_nodal_analysis() -> None:
    network = load_network_from_json('./examples/networks/json/example_network_11.json')
    solution = nodal_analysis_solver(network)
    np.testing.assert_almost_equal(solution.get_voltage('R1'), 0, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R2'), 20, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R3'), -20, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('R4'), 100, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('Iq'), 0, decimal=2)
    np.testing.assert_almost_equal(solution.get_voltage('Uq'), 120, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R1'), 0, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R2'), 4, decimal=2)
    np.testing.assert_almost_equal(solution.get_current('R3'), -1, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('R4'), 5, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('Iq'), 4, decimal=3)
    np.testing.assert_almost_equal(solution.get_current('Uq'), 5, decimal=3)

