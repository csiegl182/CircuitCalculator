from CircuitCalculator.Network.network import Branch
from CircuitCalculator.Network.symbolic_elements import voltage_source, current_source, resistor, conductor

def test_ideal_voltage_source_is_not_short_circuit() -> None:
    b = Branch('1', '0', voltage_source('Us1', V='1'))
    assert b.element.is_short_circuit == False

def test_ideal_voltage_source_with_zero_voltage_is_short_circuit() -> None:
    b = Branch('1', '0', voltage_source('Us1', V='0'))
    assert b.element.is_short_circuit == True

def test_voltage_source_is_not_short_circuit() -> None:
    b = Branch('1', '0', voltage_source('Us1', V='1', Z='1'))
    assert b.element.is_short_circuit == False

def test_voltage_source_with_zero_voltage_is_not_short_circuit() -> None:
    b = Branch('1', '0', voltage_source('Us1', V='0', Z='1'))
    assert b.element.is_short_circuit == False

def test_ideal_current_source_is_not_short_circuit() -> None:
    b = Branch('1', '0', current_source('Is1', I='1'))
    assert b.element.is_short_circuit == False

def test_ideal_current_source_with_zero_current_is_not_short_circuit() -> None:
    b = Branch('1', '0', current_source('Is1', I='0'))
    assert b.element.is_short_circuit == False

def test_current_source_is_not_short_circuit() -> None:
    b = Branch('1', '0', current_source('Is1', I='1', Y='1'))
    assert b.element.is_short_circuit == False

def test_current_source_with_zero_current_is_not_short_circuit() -> None:
    b = Branch('1', '0', current_source('Is1', I='0', Y='1'))
    assert b.element.is_short_circuit == False

def test_resistor_is_not_short_circuit() -> None:
    b = Branch('1', '0', resistor('R1', R='1'))
    assert b.element.is_short_circuit == False

def test_conductor_is_not_short_circuit() -> None:
    b = Branch('1', '0', conductor('G1', G='1'))
    assert b.element.is_short_circuit == False