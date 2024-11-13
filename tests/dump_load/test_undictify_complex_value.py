from hypothesis import given, strategies as st
from CircuitCalculator.dump_load import undictify_complex_values
import numpy as np
from numpy.testing import assert_approx_equal
import pytest

@given(st.complex_numbers(allow_nan=False))
def test_undictify_complex_from_real_imag_data(z: complex) -> None:
    data = {'z': {'real': z.real, 'imag': z.imag}}
    restored_data = undictify_complex_values(data)
    assert restored_data['z'] == z

def test_additional_field_to_real_imag_prevents_restoring_of_complex_number() -> None:
    not_complex_number = {'real': 1, 'imag': 2, 'additional': 3}
    data = {'z': not_complex_number}
    restored_data = undictify_complex_values(data)
    assert restored_data['z'] == not_complex_number

def test_missing_imag_field_prevents_restoring_of_complex_number() -> None:
    not_complex_number = {'real': 1}
    data = {'z': not_complex_number}
    restored_data = undictify_complex_values(data)
    assert restored_data['z'] == not_complex_number

def test_missing_real_field_prevents_restoring_of_complex_number() -> None:
    not_complex_number = {'imag': 2}
    data = {'z': not_complex_number}
    restored_data = undictify_complex_values(data)
    assert restored_data['z'] == not_complex_number

@given(st.complex_numbers(allow_nan=False, allow_infinity=False))
def test_undictify_complex_from_abs_phase_data(z: complex) -> None:
    data = {'z': {'abs': np.abs(z), 'phase': np.angle(z)}}
    restored_data = undictify_complex_values(data)
    assert_approx_equal(np.abs(restored_data['z']), np.abs(z))
    assert_approx_equal(np.mod(np.angle(restored_data['z']), np.pi), np.mod(np.angle(z), np.pi))

def test_additional_field_to_abs_phase_prevents_restoring_of_complex_number() -> None:
    not_complex_number = {'abs': 1, 'phase': 2, 'additional': 3}
    data = {'z': not_complex_number}
    restored_data = undictify_complex_values(data)
    assert restored_data['z'] == not_complex_number

def test_missing_phase_field_prevents_restoring_of_complex_number() -> None:
    not_complex_number = {'abs': 1}
    data = {'z': not_complex_number}
    restored_data = undictify_complex_values(data)
    assert restored_data['z'] == not_complex_number

def test_missing_abs_field_prevents_restoring_of_complex_number() -> None:
    not_complex_number = {'phase': 2}
    data = {'z': not_complex_number}
    restored_data = undictify_complex_values(data)
    assert restored_data['z'] == not_complex_number

def test_undictify_complex_from_abs_phase_data_with_negative_abs_raises_value_error() -> None:
    data = {'z': {'abs': -1, 'phase': np.pi}}
    with pytest.raises(ValueError):
        _ = undictify_complex_values(data)

@given(st.complex_numbers(allow_nan=False, allow_infinity=False))
def test_undictify_complex_from_abs_phase_data_with_deg_phase(z: complex) -> None:
    data = {'z': {'abs': np.abs(z), 'phase_deg': np.angle(z)/np.pi*180}}
    restored_data = undictify_complex_values(data)
    assert_approx_equal(np.abs(restored_data['z']), np.abs(z))
    assert_approx_equal(np.mod(np.angle(restored_data['z']), np.pi), np.mod(np.angle(z), np.pi))

def test_additional_field_to_abs_phase_allows_negative_abs() -> None:
    not_complex_number = {'abs': -1, 'phase': 2, 'additional': 3}
    data = {'z': not_complex_number}
    restored_data = undictify_complex_values(data)
    assert restored_data['z'] == not_complex_number

def test_additional_field_to_abs_phase_deg_allows_negative_abs() -> None:
    not_complex_number = {'abs': -1, 'phase_deg': 2, 'additional': 3}
    data = {'z': not_complex_number}
    restored_data = undictify_complex_values(data)
    assert restored_data['z'] == not_complex_number