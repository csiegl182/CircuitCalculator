from CircuitCalculator.Network.network import Branch
from CircuitCalculator.Network.elements import current_source, voltage_source, resistor, conductor, is_active

def test_resistor_is_not_active() -> None:
    b = Branch('1', '0', resistor('R1', R=1))
    assert is_active(b.element) == False

def test_condutor_is_not_active() -> None:
    b = Branch('1', '0', conductor('G1', G=1))
    assert is_active(b.element) == False

def test_voltage_source_is_active() -> None:
    b = Branch('1', '0', voltage_source('V1', V=1))
    assert is_active(b.element) == True

def test_current_source_is_active() -> None:
    b = Branch('1', '0', current_source('I1', I=1))
    assert is_active(b.element) == True

def test_linear_voltage_source_is_active() -> None:
    b = Branch('1', '0', voltage_source('V1', V=1, Z=1))
    assert is_active(b.element) == True

def test_linear_current_source_is_active() -> None:
    b = Branch('1', '0', current_source('I1', I=1, Y=1))
    assert is_active(b.element) == True