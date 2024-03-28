from CircuitCalculator.Network.network import Branch
from CircuitCalculator.Network.elements import voltage_source, resistor, conductor, is_ideal_voltage_source, is_voltage_source

def test_ideal_voltage_source_is_detected() -> None:
    b = Branch('1', '0', voltage_source('Us1', V=1))
    assert is_ideal_voltage_source(b.element) == True
    assert is_voltage_source(b.element) == True

def test_linear_voltage_source_is_detected() -> None:
    b = Branch('1', '0', voltage_source('Us1', V=1))
    assert is_voltage_source(b.element) == True

def test_linear_voltage_source_is_not_ideal() -> None:
    b = Branch('1', '0', voltage_source('Us1', V=1, Z=1))
    assert is_ideal_voltage_source(b.element) == False

def test_resistor_is_not_ideal_voltage_source() -> None:
    b = Branch('1', '0', resistor('R1', R=1))
    assert is_ideal_voltage_source(b.element) == False

def test_resistor_is_not_voltage_source() -> None:
    b = Branch('1', '0', resistor('R1', R=1))
    assert is_voltage_source(b.element) == False

def test_conductor_is_not_ideal_voltage_source() -> None:
    b = Branch('1', '0', conductor('G1', G=1))
    assert is_ideal_voltage_source(b.element) == False

def test_conductor_is_not_voltage_source() -> None:
    b = Branch('1', '0', conductor('G1', G=1))
    assert is_voltage_source(b.element) == False