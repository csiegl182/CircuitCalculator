from CircuitCalculator.AdvancedNodalAnalysis import is_ideal_voltage_source
from CircuitCalculator.Network import voltage_source, real_voltage_source, resistor

def test_ideal_voltage_source_is_ideal_voltage_source() -> None:
    e = voltage_source(U=1)
    assert is_ideal_voltage_source(e) == True

def test_real_voltage_source_is_not_ideal_voltage_source() -> None:
    e = real_voltage_source(U=1, R=1)
    assert is_ideal_voltage_source(e) == False

def test_resistor_is_not_ideal_voltage_source() -> None:
    e = resistor(R=1)
    assert is_ideal_voltage_source(e) == False