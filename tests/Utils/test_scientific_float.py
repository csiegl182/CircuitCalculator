from CircuitCalculator.Utils import scientific_float
from numpy.testing import assert_almost_equal

def test_scientific_float_returns_string_of_correct_length_for_values_greater_than_one() -> None:
    value = 1.23
    precision = 3
    assert len(scientific_float(value, precision=precision)) == precision+1

def test_scientific_float_returns_string_of_correct_length_for_values_less_than_minus_one() -> None:
    value = -1.23
    precision = 3
    assert len(scientific_float(value, precision=precision)) == precision+2

def test_scientific_float_returns_correct_value() -> None:
    value = 1.23
    precision = 3
    assert_almost_equal(float(scientific_float(value, precision=precision)), value, decimal=precision)

def test_scientific_float_fills_with_trailing_zeros() -> None:
    value = 1.1
    precision = 3
    str_repr = scientific_float(value, precision=precision)
    assert str_repr == '1.10'

def test_small_values_are_zoomed_with_exp_factors() -> None:
    value = 0.001
    precision = 3
    str_repr = scientific_float(value, precision=precision)
    assert str_repr == '1.00e-3'

def test_large_values_are_zoomed_with_exp_factors() -> None:
    value = 1000
    precision = 3
    str_repr = scientific_float(value, precision=precision)
    assert str_repr == '1.00e3'

def test_zoom_works_always_with_multiple_of_three_for_small_values() -> None:
    value = 0.0001
    precision = 3
    str_repr = scientific_float(value, precision=precision)
    assert str_repr == '100e-6'

def test_zoom_works_always_with_multiple_of_three_for_large_values() -> None:
    value = 100000000
    precision = 3
    str_repr = scientific_float(value, precision=precision)
    assert str_repr == '100e6'

def test_zoom_works_with_exponential_prefixes_for_1000() -> None:
    value = 1000
    precision = 3
    str_repr = scientific_float(value, precision=precision, use_exp_prefix=True)
    assert str_repr == '1.00k'

def test_zoom_works_with_exponential_prefixes_for_100m() -> None:
    value = 0.1
    precision = 3
    str_repr = scientific_float(value, precision=precision, use_exp_prefix=True)
    assert str_repr == '100m'

def test_zoom_works_with_exponential_prefixes_for_large_values_out_of_range() -> None:
    value = 10e6
    precision = 3
    str_repr = scientific_float(value, precision=precision, use_exp_prefix=True, exp_prefixes={3: 'k'})
    assert str_repr == '10.0e3k'

def test_zoom_works_with_exponential_prefixes_for_small_values_out_of_range() -> None:
    value = 1e-5
    precision = 3
    str_repr = scientific_float(value, precision=precision, use_exp_prefix=True, exp_prefixes={-3: 'm'})
    assert str_repr == '10.0e-3m'

def test_unscaled_value_with_exp_prefix() -> None:
    value = 1.56
    precision = 3
    str_repr = scientific_float(value, precision=precision, use_exp_prefix=True)
    assert str_repr == '1.56'