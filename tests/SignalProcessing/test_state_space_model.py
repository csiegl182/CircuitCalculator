from CircuitCalculator.SignalProcessing.state_space_model import StateSpaceModel
import numpy as np
import pytest

def test_state_space_model_only_accepts_square_state_matrices() -> None:
    A = np.array([[1, 2, 3], [4, 5, 6]])
    B = np.array([[1], [2]])
    C = np.array([[1, 2]])
    D = np.array([[1]])
    with pytest.raises(ValueError):
        StateSpaceModel(A, B, C, D)

def test_state_space_model_raises_exception_if_number_of_rows_of_input_matrix_does_not_match_number_of_states() -> None:
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[1], [2], [3]])
    C = np.array([[1, 2]])
    D = np.array([[1]])
    with pytest.raises(ValueError):
        StateSpaceModel(A, B, C, D)

def test_state_space_model_raises_exception_if_number_of_columns_of_output_matrix_does_not_match_number_of_states() -> None:
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[1], [2]])
    C = np.array([[1, 2, 3]])
    D = np.array([[1]])
    with pytest.raises(ValueError):
        StateSpaceModel(A, B, C, D)

def test_state_space_model_raises_exception_if_number_of_columns_of_feedthrough_matrix_does_not_match_number_of_columns_of_input_matrix() -> None:
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[1], [2]])
    C = np.array([[1, 2]])
    D = np.array([[1, 2]])
    with pytest.raises(ValueError):
        StateSpaceModel(A, B, C, D)

def test_state_space_model_raises_exception_if_number_of_rows_of_feedthrough_matrix_does_not_match_number_of_rows_of_output_matrix() -> None:
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[1], [2]])
    C = np.array([[1, 2]])
    D = np.array([[1], [2]])
    with pytest.raises(ValueError):
        StateSpaceModel(A, B, C, D)

def test_state_space_model_returns_number_of_states() -> None:
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[1], [2]])
    C = np.array([[1, 2]])
    D = np.array([[1]])
    model = StateSpaceModel(A, B, C, D)
    assert model.n_states == 2

def test_state_space_model_returns_number_of_inputs() -> None:
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[1], [2]])
    C = np.array([[1, 2]])
    D = np.array([[1]])
    model = StateSpaceModel(A, B, C, D)
    assert model.n_inputs == 1

def test_state_space_model_returns_number_of_outputs() -> None:
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[1], [2]])
    C = np.array([[1, 2]])
    D = np.array([[1]])
    model = StateSpaceModel(A, B, C, D)
    assert model.n_outputs == 1