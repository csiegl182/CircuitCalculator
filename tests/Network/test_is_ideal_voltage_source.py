from CircuitCalculator.Network import Branch, voltage_source, real_voltage_source, resistor, is_ideal_voltage_source

def test_ideal_voltage_source_is_ideal_voltage_source() -> None:
    b = Branch('1', '0', voltage_source(U=1))
    assert is_ideal_voltage_source(b.element) == True

def test_real_voltage_source_is_not_ideal_voltage_source() -> None:
    b = Branch('1', '0', real_voltage_source(U=1, R=1))
    assert is_ideal_voltage_source(b.element) == False

def test_resistor_is_not_ideal_voltage_source() -> None:
    b = Branch('1', '0', resistor(R=1))
    assert is_ideal_voltage_source(b.element) == False