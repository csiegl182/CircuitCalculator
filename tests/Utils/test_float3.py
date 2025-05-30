from CircuitCalculator.Utils import Float3
from numpy.testing import assert_almost_equal
from numpy import isnan

def test_float3_returns_split_values_for_0_12() -> None:
    f3 = Float3(0.12)
    assert f3.mantissa3 == 120
    assert f3.exponent3 == -3

def test_float3_returns_split_value_for_1200() -> None:
    f3 = Float3(1200)
    assert_almost_equal(f3.mantissa3, 1.2)
    assert f3.exponent3 == 3

def test_float3_returns_split_values_for_12() -> None:
    f3 = Float3(12)
    assert f3.mantissa3 == 12
    assert f3.exponent3 == 0

def test_float3_returns_split_value_for_1000() -> None:
    f3 = Float3(1000)
    assert_almost_equal(f3.mantissa3, 1.0)
    assert f3.exponent3 == 3

def test_float3_returns_split_value_for_0_9998() -> None:
    f3 = Float3(0.9998)
    assert_almost_equal(f3.mantissa3, 1.0)
    assert f3.exponent3 == 0

def test_float3_returns_split_value_for_1234567890() -> None:
    f3 = Float3(1234567890, precision=7)
    assert_almost_equal(f3.mantissa3, 1.234568)
    assert f3.exponent3 == 9

def test_float3_returns_split_value_for_1_234567890() -> None:
    f3 = Float3(1.234567890, precision=7)
    assert_almost_equal(f3.mantissa3, 1.234568)
    assert f3.exponent3 == 0

def test_float3_returns_nan_mantissa_and_zero_exponent_for_nan_value() -> None:
    f3 = Float3(float('nan'))
    assert isnan(f3.mantissa3)
    assert f3.exponent3 == 0

