from CircuitCalculator.AdvancedNodalAnalysis import is_ideal_current_source
from CircuitCalculator.Network import current_source, real_current_source, resistor

def test_ideal_current_source_is_ideal_current_source() -> None:
    e = current_source(I=1)
    assert is_ideal_current_source(e) == True

def test_real_current_source_is_not_ideal_current_source() -> None:
    e = real_current_source(I=1, R=1)
    assert is_ideal_current_source(e) == False

def test_resistor_is_not_ideal_current_source() -> None:
    e = resistor(R=1)
    assert is_ideal_current_source(e) == False