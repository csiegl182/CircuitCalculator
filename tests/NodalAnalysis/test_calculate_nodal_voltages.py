import pytest
import numpy as np
from NodalAnalysis import DimensionError, calculate_node_voltages

def test_only_two_dimensional_y_matrix_is_accepted() -> None:
    with pytest.raises(DimensionError):
        calculate_node_voltages(Y=np.array([1, 2, 3]), I=np.array([1, 2, 3]))

def test_only_one_dimensional_i_vector_is_accepted() -> None:
    with pytest.raises(DimensionError):
        calculate_node_voltages(Y=np.array([[1, 2, 3], [4, 5, 6]]), I=np.array([[1, 2, 3], [4, 5,6]]))

def test_only_square_y_matrix_is_accepted() -> None:
    with pytest.raises(DimensionError):
        calculate_node_voltages(Y=np.array([[1, 2, 3], [4, 5, 6]]), I=np.array([1, 2, 3]))

def test_equation_array_is_solved_correctly() -> None:
    Y = np.array([[1, 2], [0, 1]], dtype=float)
    I = np.array([0, -1], dtype=float)
    np.testing.assert_almost_equal(calculate_node_voltages(Y, I), np.array([2, -1], dtype=float))
