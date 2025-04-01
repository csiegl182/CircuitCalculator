from CircuitCalculator.Circuit.Components.symbolic_components import value_less_than_zero

def test_value_less_than_zero_returns_true_for_negative_value() -> None:
    value = '-1'
    assert value_less_than_zero(value) == True

def test_value_less_than_zero_returns_false_for_zero_value() -> None:
    value = '0'
    assert value_less_than_zero(value) == False

def test_value_less_than_zero_returns_false_for_positive_value() -> None:
    value = '1'
    assert value_less_than_zero(value) == False

def test_value_less_than_zero_returns_false_for_non_numeric_value() -> None:
    value = 'a'
    assert value_less_than_zero(value) == False

def test_value_less_than_zero_returns_true_for_negative_rational_number() -> None:
    value = '-3/7'
    assert value_less_than_zero(value) == True

def test_value_less_than_zero_returns_false_for_postive_rational_number() -> None:
    value = '3/7'
    assert value_less_than_zero(value) == False

def test_value_less_than_zero_returns_false_for_empty_number() -> None:
    value = ''
    assert value_less_than_zero(value) == False