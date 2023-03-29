from CircuitCalculator.Utils import Float3, FloatPrecision
from numpy.testing import assert_almost_equal

def test_float3_returns_split_values_for_0_12() -> None:
    value = FloatPrecision(0.12)
    f3 = Float3(value)
    assert f3.mantissa == 120
    assert f3.exponent == -3

def test_float3_returns_split_value_for_1200() -> None:
    value = FloatPrecision(1200)
    f3 = Float3(value)
    assert_almost_equal(f3.mantissa, 1.2)
    assert f3.exponent == 3

def test_float3_returns_split_values_for_12() -> None:
    value = FloatPrecision(12)
    f3 = Float3(value)
    assert f3.mantissa == 12
    assert f3.exponent == 0

def test_float3_returns_split_value_for_1000() -> None:
    value = FloatPrecision(1000)
    f3 = Float3(value)
    assert_almost_equal(f3.mantissa, 1.0)
    assert f3.exponent == 3

def test_float3_returns_split_value_for_0_9998() -> None:
    value = FloatPrecision(0.9998)
    f3 = Float3(value)
    assert_almost_equal(f3.mantissa, 1.0)
    assert f3.exponent == 0

def test_float3_reutrns_split_value_for_1234567890() -> None:
    value = FloatPrecision(1234567890, precision=7)
    f3 = Float3(value)
    assert_almost_equal(f3.mantissa, 1.234568)
    assert f3.exponent == 9

def test_float3_reutrns_split_value_for_1_234567890() -> None:
    value = FloatPrecision(1.234567890, precision=7)
    f3 = Float3(value)
    assert_almost_equal(f3.mantissa, 1.234568)
    assert f3.exponent == 0