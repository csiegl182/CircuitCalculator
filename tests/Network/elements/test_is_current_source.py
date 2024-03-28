from CircuitCalculator.Network.network import Branch
from CircuitCalculator.Network.elements import current_source, resistor, conductor, is_ideal_current_source, is_current_source

def test_ideal_current_source_is_detected() -> None:
    b = Branch('1', '0', current_source('Is1', I=1))
    assert is_ideal_current_source(b.element) == True
    assert is_current_source(b.element) == True

def test_linear_current_source_is_detected() -> None:
    b = Branch('1', '0', current_source('Is1', I=1, Y=1))
    assert is_current_source(b.element) == True

def test_linear_current_source_is_not_ideal() -> None:
    b = Branch('1', '0', current_source('Is1', I=1, Y=1))
    assert is_ideal_current_source(b.element) == False

def test_resistor_is_not_ideal_current_source() -> None:
    b = Branch('1', '0', resistor('R1', R=1))
    assert is_ideal_current_source(b.element) == False

def test_resistor_is_not_current_source() -> None:
    b = Branch('1', '0', resistor('R1', R=1))
    assert is_current_source(b.element) == False

def test_conductor_is_not_ideal_current_source() -> None:
    b = Branch('1', '0', conductor('G1', G=1))
    assert is_ideal_current_source(b.element) == False

def test_conductor_is_not_current_source() -> None:
    b = Branch('1', '0', conductor('G1', G=1))
    assert is_current_source(b.element) == False