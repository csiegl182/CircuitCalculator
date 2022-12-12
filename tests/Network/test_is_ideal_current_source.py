from CircuitCalculator.Network import Branch, current_source, real_current_source, resistor, is_ideal_current_source

def test_ideal_current_source_is_ideal_current_source() -> None:
    b = Branch('1', '0', current_source(I=1))
    assert is_ideal_current_source(b.element) == True

def test_real_current_source_is_not_ideal_current_source() -> None:
    b = Branch('1', '0', real_current_source(I=1, R=1))
    assert is_ideal_current_source(b.element) == False

def test_resistor_is_not_ideal_current_source() -> None:
    b = Branch('1', '0', resistor(R=1))
    assert is_ideal_current_source(b.element) == False