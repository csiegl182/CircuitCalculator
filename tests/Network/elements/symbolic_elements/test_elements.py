import pytest
import CircuitCalculator.Network.symbolic_elements as elm

def test_zero_resistance_has_inf_conductance() -> None:
    R = elm.resistor('R1', R='0')
    assert R.Y == 'oo'

def test_inf_resistance_has_zero_conductance() -> None:
    R = elm.resistor('R1', R='oo')
    assert R.Y == '0'

def test_zero_conductance_has_inf_resistance() -> None:
    G = elm.conductor('G1', G='0')
    assert G.Z == 'oo'

def test_inf_conductance_has_zero_resistance() -> None:
    G = elm.conductor('G1', G='oo')
    assert G.Z == '0'

def test_linear_current_source_with_zero_conductance_has_inf_resistance() -> None:
    I = elm.current_source('Is1', I='1', Y='0')
    assert I.Z == 'oo';

def test_linear_current_source_with_inf_conductance_has_zero_resistance() -> None:
    I = elm.current_source('Is1', I='1', Y='oo')
    assert I.Z == '0'

def test_linear_current_source_with_inf_conductance_has_zero_voltage() -> None:
    I = elm.current_source('Is1', I='1', Y='oo')
    assert I.V == '0'

def test_linear_current_source_with_zero_conductance_has_nan_voltage() -> None:
    I = elm.current_source('Is1', I='1', Y='0')
    assert str(I.V).lower() == 'nan'

def test_linear_voltage_source_with_zero_resistance_has_inf_conductance() -> None:
    U = elm.voltage_source('Us1', V='1', Z='0')
    assert U.Y == 'oo'

def test_linear_voltage_source_with_inf_resistance_has_zero_conductance() -> None:
    U = elm.voltage_source('Us1', V='1', Z='oo')
    assert U.Y == '0'

def test_linear_voltage_source_with_inf_resistance_has_zero_current() -> None:
    U = elm.voltage_source('Us1', V='1', Z='oo')
    assert U.I == '0'

def test_linear_voltage_source_with_zero_resistance_has_nan_current() -> None:
    U = elm.voltage_source('Us1', V='1', Z='0')
    assert str(U.I).lower() == 'nan'

def test_load_raises_error_when_not_providing_reference_values() -> None:
    with pytest.raises(AttributeError):
        elm.load(name='load', P = '1')

def test_load_raises_error_when_not_providing_both_reference_values() -> None:
    with pytest.raises(AttributeError):
        elm.load(name='load', P = '1', V_ref = '1', I_ref = '1')

def test_load_has_zero_voltage() -> None:
    L = elm.load(name='load', P = '1', V_ref = '1')
    assert L.V == '0'

def test_load_has_zero_current() -> None:
    L = elm.load(name='load', P = '1', V_ref = '1')
    assert L.I == '0'

def test_load_resistance_is_calculated_correctly_from_reference_voltage() -> None:
    L = elm.load(name='load', P = 'P', Q = 'Q', V_ref = 'V_ref')
    assert str(L.Y).strip() == '(P+1j*Q)/(V_ref*V_ref)'

def test_load_resistance_is_calculated_correctly_from_reference_current() -> None:
    L = elm.load(name='load', P = 'P', Q = 'Q', I_ref = 'I_ref')
    assert str(L.Z) == '(P+1j*Q)/(I_ref*I_ref)'
