from CircuitCalculator.Utils import FloatPrecision

def test_positive_values_near_zero_are_splitted() -> None:
    value = 0.12345678
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 123
    assert fp_value.exponent == -3

def test_positive_big_values_are_splitted() -> None:
    value = 12345678
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 123
    assert fp_value.exponent == 5

def test_negative_values_near_zero_are_splitted() -> None:
    value = -0.12345678
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == -123
    assert fp_value.exponent == -3

def test_negative_big_values_are_splitted() -> None:
    value = -12345678
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == -123
    assert fp_value.exponent == 5

def test_very_small_values_are_splitted() -> None:
    value = 0.0004
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 400
    assert fp_value.exponent == -6

def test_zero_is_splitted() -> None:
    value = 0
    fp_value = FloatPrecision(value, min_exp=-1)
    assert fp_value.mantissa == 0
    assert fp_value.exponent == 0 

def test_1000_is_splitted() -> None:
    value = 1000
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 100
    assert fp_value.exponent == 1

def test_0_001_is_splitted() -> None:
    value = 0.001
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 100
    assert fp_value.exponent == -5

def test_0_9998_is_splitted() -> None:
    value = 0.9998
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 1
    assert fp_value.exponent == 0

def test_1_1e5_is_splitted() -> None:
    value = 1e-5
    fp_value = FloatPrecision(value)
    assert fp_value.mantissa == 100
    assert fp_value.exponent == -7

def test_value_less_than_max_exponent_is_not_infinity() -> None:
    value = 999.4e3
    fp_value = FloatPrecision(value, max_exp=3)
    assert fp_value.is_inf == False

def test_value_greater_than_max_exponent_is_infinity() -> None:
    value = 1000.1e3
    fp_value = FloatPrecision(value, max_exp=3)
    assert fp_value.is_inf == True

def test_negative_value_less_than_max_exponent_is_not_infinity() -> None:
    value = -999.4e3
    fp_value = FloatPrecision(value, max_exp=3)
    assert fp_value.is_inf == False

def test_negative_value_greater_than_max_exponent_is_infinity() -> None:
    value = -1000.1e3
    fp_value = FloatPrecision(value, max_exp=3)
    assert fp_value.is_inf == True

def test_value_less_than_min_exponent_is_zero() -> None:
    value = 99.9e3
    fp_value = FloatPrecision(value, min_exp=3)
    assert fp_value.is_zero == True

def test_value_greater_than_min_exponent_is_not_zero() -> None:
    value = 1000.1e3
    fp_value = FloatPrecision(value, max_exp=3)
    assert fp_value.is_zero == False

def test_zero_is_zero() -> None:
    value = 0
    fp_value = FloatPrecision(value)
    assert fp_value.is_zero == True