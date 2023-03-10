from CircuitCalculator.Utils import ScientificFloat
from numpy.testing import assert_almost_equal

def test_ScientificFloat_returns_string_of_correct_length_for_values_greater_than_one() -> None:
    value = 1.23
    precision = 3
    assert len(str(ScientificFloat(value, precision=precision))) == precision+1

def test_ScientificFloat_returns_string_of_correct_length_for_values_less_than_minus_one() -> None:
    value = -1.23
    precision = 3
    assert len(str(ScientificFloat(value, precision=precision))) == precision+2

def test_ScientificFloat_returns_correct_value() -> None:
    value = 1.23
    precision = 3
    assert_almost_equal(float(ScientificFloat(value, precision=precision).__str__()), value, decimal=precision)

def test_ScientificFloat_fills_with_trailing_zeros() -> None:
    value = 1.1
    precision = 3
    str_repr = str(ScientificFloat(value, precision=precision))
    assert str_repr == '1.10'

def test_small_values_are_zoomed_with_exp_factors() -> None:
    value = 0.001
    precision = 3
    str_repr = str(ScientificFloat(value, precision=precision))
    assert str_repr == '1.00e-3'

def test_large_values_are_zoomed_with_exp_factors() -> None:
    value = 1000
    precision = 3
    str_repr = str(ScientificFloat(value, precision=precision))
    assert str_repr == '1.00e3'

def test_zoom_works_always_with_multiple_of_three_for_small_values() -> None:
    value = 0.0001
    precision = 3
    str_repr = str(ScientificFloat(value, precision=precision))
    assert str_repr == '100e-6'

def test_zoom_works_always_with_multiple_of_three_for_large_values() -> None:
    value = 100000000
    precision = 3
    str_repr = str(ScientificFloat(value, precision=precision))
    assert str_repr == '100e6'

def test_zoom_works_with_exponential_prefixes_for_1000() -> None:
    value = 1000
    precision = 3
    str_repr = str(ScientificFloat(value, precision=precision, use_exp_prefix=True))
    assert str_repr == '1.00k'

def test_zoom_works_with_exponential_prefixes_for_100m() -> None:
    value = 0.1
    precision = 3
    str_repr = str(ScientificFloat(value, precision=precision, use_exp_prefix=True))
    assert str_repr == '100m'

def test_zoom_works_with_exponential_prefixes_for_large_values_out_of_range() -> None:
    value = 10e6
    precision = 3
    str_repr = str(ScientificFloat(value, precision=precision, use_exp_prefix=True, exp_prefixes={3: 'k'}))
    assert str_repr == '10.0e3k'

def test_zoom_works_with_exponential_prefixes_for_small_values_out_of_range() -> None:
    value = 1e-5
    precision = 3
    str_repr = str(ScientificFloat(value, precision=precision, use_exp_prefix=True, exp_prefixes={-3: 'm'}))
    assert str_repr == '10.0e-3m'

def test_unscaled_value_with_exp_prefix() -> None:
    value = 1.56
    precision = 3
    str_repr = str(ScientificFloat(value, precision=precision, use_exp_prefix=True))
    assert str_repr == '1.56'

def test_unscaled_value_with_high_precision() -> None:
    value = 1.234567890
    precision = 7
    str_repr = str(ScientificFloat(value, precision=precision, use_exp_prefix=True))
    assert str_repr == '1.234568'

def test_unscaled_value_with_low_precision() -> None:
    value = 1.234567890
    precision = 2
    str_repr = str(ScientificFloat(value, precision=precision, use_exp_prefix=True))
    assert str_repr == '1.2'

def test_unscaled_value_with_unit() -> None:
    value = 1.12
    str_repr = str(ScientificFloat(value, unit='W'))
    assert str_repr == '1.12W'

def test_scaled_value_with_unit() -> None:
    value = 1.12e-3
    str_repr = str(ScientificFloat(value, unit='W'))
    assert str_repr == '1.12e-3W'

def test_scaled_value_with_unit_and_exp_prefix() -> None:
    value = 1.12e-3
    str_repr = str(ScientificFloat(value, unit='W', use_exp_prefix=True))
    assert str_repr == '1.12mW'

def test_scaled_value_at_rounding_edge() -> None:
    value = 0.00999800059980007
    str_repr = str(ScientificFloat(value))
    assert str_repr == '10.0e-3'

def test_scaled_value_at_rounding_edge_with_exp_prefix() -> None:
    value = 0.999800059980007
    str_repr = str(ScientificFloat(value, use_exp_prefix=True))
    assert str_repr == '1.00'