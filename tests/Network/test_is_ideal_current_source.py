from CircuitCalculator.Network.network import Branch
from CircuitCalculator.Network.elements import current_source, linear_current_source, resistor, is_ideal_current_source

def test_ideal_current_source_is_ideal_current_source() -> None:
    b = Branch('1', '0', current_source('Is1', I=1))
    assert is_ideal_current_source(b.element) == True

def test_linear_current_source_is_not_ideal_current_source() -> None:
    b = Branch('1', '0', linear_current_source('Is1', I=1, Y=1))
    assert is_ideal_current_source(b.element) == False

def test_resistor_is_not_ideal_current_source() -> None:
    b = Branch('1', '0', resistor('R1', R=1))
    assert is_ideal_current_source(b.element) == False