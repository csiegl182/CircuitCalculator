import pytest
from hypothesis import given, strategies as st
import CircuitCalculator.Network.elements as elm
from numpy import inf, isnan

def test_zero_resistance_has_inf_conductance() -> None:
    R = elm.resistor('R1', R=0)
    assert R.Y == inf

def test_inf_resistance_has_zero_conductance() -> None:
    R = elm.resistor('R1', R=inf)
    assert R.Y == 0

def test_zero_conductance_has_inf_resistance() -> None:
    G = elm.conductance('G1', G=0)
    assert G.Z == inf

def test_inf_conductance_has_zero_resistance() -> None:
    G = elm.conductance('G1', G=inf)
    assert G.Z == 0

def test_linear_current_source_with_zero_conductance_has_inf_resistance() -> None:
    I = elm.current_source('Is1', I=1, Y=0)
    assert I.Z == inf

def test_linear_current_source_with_inf_conductance_has_zero_resistance() -> None:
    I = elm.current_source('Is1', I=1, Y=inf)
    assert I.Z == 0

def test_linear_current_source_with_inf_conductance_has_zero_voltage() -> None:
    I = elm.current_source('Is1', I=1, Y=inf)
    assert I.V == 0

def test_linear_current_source_with_zero_conductance_has_nan_voltage() -> None:
    I = elm.current_source('Is1', I=1, Y=0)
    assert isnan(I.V)

def test_linear_voltage_source_with_zero_resistance_has_inf_conductance() -> None:
    U = elm.voltage_source('Us1', V=1, Z=0)
    assert U.Y == inf

def test_linear_voltage_source_with_inf_resistance_has_zero_conductance() -> None:
    U = elm.voltage_source('Us1', V=1, Z=inf)
    assert U.Y == 0

def test_linear_voltage_source_with_inf_resistance_has_zero_current() -> None:
    U = elm.voltage_source('Us1', V=1, Z=inf)
    assert U.I == 0

def test_linear_voltage_source_with_zero_resistance_has_nan_current() -> None:
    U = elm.voltage_source('Us1', V=1, Z=0)
    assert isnan(U.I)

def test_load_raises_error_when_not_providing_reference_values() -> None:
    with pytest.raises(AttributeError):
        elm.load(name='load', P = 1)

def test_load_raises_error_when_not_providing_both_reference_values() -> None:
    with pytest.raises(AttributeError):
        elm.load(name='load', P = 1, V_ref = 1, I_ref = 1)

def test_load_raises_error_when_reference_voltage_is_zero() -> None:
    with pytest.raises(ValueError):
        elm.load(name='load', P = 1, V_ref = 0)

def test_load_raises_error_when_reference_current_is_zero() -> None:
    with pytest.raises(ValueError):
        elm.load(name='load', P = 1, I_ref = 0)

def test_load_has_zero_voltage() -> None:
    L = elm.load(name='load', P = 1, V_ref = 1)
    assert L.V == 0

def test_load_has_zero_current() -> None:
    L = elm.load(name='load', P = 1, V_ref = 1)
    assert L.I == 0

@given(st.floats(min_value=0, max_value=1e3, allow_subnormal=False), st.floats(min_value=0, max_value=1e3, allow_subnormal=False), st.floats(min_value=1e-3, max_value=1e3, allow_subnormal=False))
def test_load_resistance_is_calculated_correctly_from_reference_voltage(P, Q, V_ref) -> None:
    L = elm.load(name='load', P = P, Q = Q, V_ref = V_ref)
    assert L.Y == complex(P, Q)/V_ref**2

@given(st.floats(min_value=0, max_value=1e3, allow_subnormal=False), st.floats(min_value=0, max_value=1e3, allow_subnormal=False), st.floats(min_value=1e-3, max_value=1e3, allow_subnormal=False))
def test_load_resistance_is_calculated_correctly_from_reference_current(P, Q, I_ref) -> None:
    L = elm.load(name='load', P = P, Q = Q, I_ref = I_ref)
    assert L.Z == complex(P, Q)/I_ref**2
