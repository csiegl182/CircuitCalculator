from CircuitCalculator.Network.elements import linear_current_source, resistor, conductor, linear_voltage_source
from numpy import inf, nan, isnan

def test_zero_resistance_has_inf_conductance() -> None:
    R = resistor(R=0)
    assert R.Y == inf

def test_inf_resistance_has_zero_conductance() -> None:
    R = resistor(R=inf)
    assert R.Y == 0

def test_zero_conductance_has_inf_resistance() -> None:
    G = conductor(G=0)
    assert G.Z == inf

def test_inf_conductance_has_zero_resistance() -> None:
    G = conductor(G=inf)
    assert G.Z == 0

def test_linear_current_source_with_zero_resistance_has_inf_conductance() -> None:
    I = linear_current_source(I=1, R=0)
    assert I.Y == inf

def test_linear_current_source_with_inf_resistance_has_zero_conductance() -> None:
    I = linear_current_source(I=1, R=inf)
    assert I.Y == 0

def test_linear_current_source_with_zero_resistance_has_zero_voltage() -> None:
    I = linear_current_source(I=1, R=0)
    assert I.U == 0

def test_linear_current_source_with_inf_resistance_has_nan_voltage() -> None:
    I = linear_current_source(I=1, R=inf)
    assert isnan(I.U)

def test_linear_voltage_source_with_zero_resistance_has_inf_conductance() -> None:
    U = linear_voltage_source(U=1, R=0)
    assert U.Y == inf

def test_linear_voltage_source_with_inf_resistance_has_zero_conductance() -> None:
    U = linear_voltage_source(U=1, R=inf)
    assert U.Y == 0

def test_linear_voltage_source_with_inf_resistance_has_zero_current() -> None:
    U = linear_voltage_source(U=1, R=inf)
    assert U.I == 0

def test_linear_voltage_source_with_zero_resistance_has_nan_current() -> None:
    U = linear_voltage_source(U=1, R=0)
    assert isnan(U.I)