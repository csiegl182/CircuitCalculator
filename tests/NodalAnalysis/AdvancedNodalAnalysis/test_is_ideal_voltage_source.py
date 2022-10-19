from CircuitCalculator.AdvancedNodalAnalysis import is_ideal_voltage_source
from CircuitCalculator.Network import voltage_source, real_voltage_source

def test_ideal_voltage_source_is_ideal_voltage_source() -> None:
    vs = voltage_source(U=1)
    assert is_ideal_voltage_source(vs) == True

def test_real_voltage_source_is_not_ideal_voltage_source() -> None:
    vs = real_voltage_source(U=1, R=1)
    assert is_ideal_voltage_source(vs) == False