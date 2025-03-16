from CircuitCalculator.Network.network import Branch
from CircuitCalculator.Network.symbolic_elements import current_source, resistor, conductor

def test_ideal_current_source_is_detected() -> None:
    b = Branch('1', '0', current_source('Is1', I='1'))
    assert b.element.is_ideal_current_source == True
    assert b.element.is_current_source == True

def test_linear_current_source_is_detected() -> None:
    b = Branch('1', '0', current_source('Is1', I='1', Y='1'))
    assert b.element.is_current_source == True

def test_linear_current_source_is_not_ideal() -> None:
    b = Branch('1', '0', current_source('Is1', I='1', Y='1'))
    assert b.element.is_ideal_current_source == False

def test_resistor_is_not_ideal_current_source() -> None:
    b = Branch('1', '0', resistor('R1', R='1'))
    assert b.element.is_ideal_current_source == False

def test_resistor_is_not_current_source() -> None:
    b = Branch('1', '0', resistor('R1', R='1'))
    assert b.element.is_current_source == False

def test_conductor_is_not_ideal_current_source() -> None:
    b = Branch('1', '0', conductor('G1', G='1'))
    assert b.element.is_ideal_current_source == False

def test_conductor_is_not_current_source() -> None:
    b = Branch('1', '0', conductor('G1', G='1'))
    assert b.element.is_current_source == False