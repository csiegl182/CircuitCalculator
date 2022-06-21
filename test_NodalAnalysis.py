import pytest
import numpy as np
from NodalAnalysis import DimensionError, calculate_node_voltages, create_node_admittance_matrix, calculate_branch_voltage

def test_calculate_nodal_voltages_accepts_only_two_dimensional_y_matrix() -> None:
    with pytest.raises(DimensionError):
        calculate_node_voltages(Y=np.array([1, 2, 3]), I=np.array([1, 2, 3]))

def test_calculate_nodal_voltages_accepts_only_one_dimensional_i_vector() -> None:
    with pytest.raises(DimensionError):
        calculate_node_voltages(Y=np.array([[1, 2, 3], [4, 5, 6]]), I=np.array([[1, 2, 3], [4, 5,6]]))

def test_calculate_nodal_voltages_accepts_only_square_y_matrix() -> None:
    with pytest.raises(DimensionError):
        calculate_node_voltages(Y=np.array([[1, 2, 3], [4, 5, 6]]), I=np.array([1, 2, 3]))

def test_calculate_nodal_voltages_solves_equation_array() -> None:
    Y = np.array([[1, 2], [0, 1]], dtype=float)
    I = np.array([0, -1], dtype=float)
    np.testing.assert_almost_equal(calculate_node_voltages(Y, I), np.array([2, -1], dtype=float))

def test_create_node_admittances_number_of_node_admittances_is_decreasing() -> None:
    with pytest.raises(DimensionError):
        create_node_admittance_matrix([1, 2], [1, 2], [3, 4])
    with pytest.raises(DimensionError):
        create_node_admittance_matrix([1, 2])
    with pytest.raises(DimensionError):
        create_node_admittance_matrix([1, 2, 3], [1])

def test_create_node_admittance_matrix_for_single_node_network() -> None:
    Y_01 = 5
    Y = create_node_admittance_matrix([Y_01])
    Y_ref = np.array([[Y_01]])
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_admittance_matrix_for_two_node_network() -> None:
    Y_01, Y_02, Y_12 = 1, 2, 3
    Y = create_node_admittance_matrix([Y_01, Y_02], [Y_12])
    Y_ref = np.array([[Y_01+Y_12, -Y_12], [-Y_12, Y_02+Y_12]])
    np.testing.assert_almost_equal(Y, Y_ref)

def test_create_node_admittance_matrix_for_three_node_network() -> None:
    Y_01, Y_02, Y_03, Y_12, Y_13, Y_23 = 1, 2, 3, 4, 5, 6
    Y = create_node_admittance_matrix([Y_01, Y_02, Y_03], [Y_12, Y_13], [Y_23])
    Y_ref = np.array([[Y_01+Y_12+Y_13, -Y_12, -Y_13], [-Y_12, Y_02+Y_12+Y_23, -Y_23], [-Y_13, -Y_23, Y_03+Y_13+Y_23]])
    np.testing.assert_almost_equal(Y, Y_ref)

def test_calculate_branch_voltages_returns_diff_from_node_voltages() -> None:
    V = np.array([3, 2, 1])
    assert calculate_branch_voltage(V, 1, 2) == 1

def test_calculate_branch_voltages_returns_branch_value_for_zero_node_index() -> None:
    V = np.array([3, 2, 1])
    assert calculate_branch_voltage(V, 0, 2) == -2
    assert calculate_branch_voltage(V, 2, 0) == 2

def test_calculate_branch_voltages_raises_dimension_error_on_negative_node_index() -> None:
    V = np.array([3, 2, 1])
    with pytest.raises(DimensionError):
        calculate_branch_voltage(V, -2, 2)
    with pytest.raises(DimensionError):
        calculate_branch_voltage(V, 2, -2)

def test_calculate_branch_voltages_raises_dimension_error_when_exceeding_node_index() -> None:
    V = np.array([3, 2, 1])
    with pytest.raises(DimensionError):
        calculate_branch_voltage(V, 1, 4)
    
