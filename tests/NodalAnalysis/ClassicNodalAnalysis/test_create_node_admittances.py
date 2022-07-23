import pytest
import numpy as np
from ClassicNodalAnalysis import DimensionError, create_node_admittance_matrix

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