from CircuitCalculator.Utils import FloatPrecision

def test_float_precision_splits_for_positive_values_near_zero() -> None:
    value = 0.12345678
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 123
    assert fp_value.exponent == -3

def test_float_precision_splits_for_positive_big_values() -> None:
    value = 12345678
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 123
    assert fp_value.exponent == 5

def test_float_precision_splits_for_negative_values_near_zero() -> None:
    value = -0.12345678
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == -123
    assert fp_value.exponent == -3

def test_float_precision_splits_for_negative_big_values() -> None:
    value = -12345678
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == -123
    assert fp_value.exponent == 5

def test_float_precision_splits_for_very_small_values() -> None:
    value = 0.0004
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 400
    assert fp_value.exponent == -6

def test_float_precision_splits_zero() -> None:
    value = 0
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 0
    assert fp_value.exponent == 0

def test_float_precision_splits_1000() -> None:
    value = 1000
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 100
    assert fp_value.exponent == 1

def test_float_precision_splits_0_001() -> None:
    value = 0.001
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 100
    assert fp_value.exponent == -5

def test_float_precision_splits_0_9998() -> None:
    value = 0.9998
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 1
    assert fp_value.exponent == 0

def test_float_precision_splits_1_1e5() -> None:
    value = 1e-5
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 100
    assert fp_value.exponent == -7