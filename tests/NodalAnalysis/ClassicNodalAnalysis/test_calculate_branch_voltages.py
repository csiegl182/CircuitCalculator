import pytest
import numpy as np
from ClassicNodalAnalysis import DimensionError, calculate_branch_voltage

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
    