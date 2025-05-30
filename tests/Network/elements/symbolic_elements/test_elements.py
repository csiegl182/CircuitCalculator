import pytest
import CircuitCalculator.Network.symbolic_elements as elm
import sympy as sp

def test_zero_resistance_has_inf_conductance() -> None:
    R = elm.resistor('R1', R=sp.sympify(0))
    assert R.Y == sp.oo

def test_inf_resistance_has_zero_conductance() -> None:
    R = elm.resistor('R1', R=sp.sympify('oo'))
    assert R.Y == 0

def test_zero_conductance_has_inf_resistance() -> None:
    G = elm.conductor('G1', G=sp.sympify(0))
    assert G.Z == sp.oo

def test_inf_conductance_has_zero_resistance() -> None:
    G = elm.conductor('G1', G=sp.sympify('oo'))
    assert G.Z == 0

def test_linear_current_source_with_zero_conductance_has_inf_resistance() -> None:
    I = elm.current_source('Is1', I=sp.Symbol('I'), Y=sp.sympify(0))
    assert I.Z == sp.oo

def test_linear_current_source_with_inf_conductance_has_zero_resistance() -> None:
    I = elm.current_source('Is1', I=sp.Symbol('I'), Y=sp.sympify('oo'))
    assert I.Z == 0

def test_linear_current_source_with_inf_conductance_has_zero_voltage() -> None:
    I = elm.current_source('Is1', I=sp.Symbol('I'), Y=sp.sympify('oo'))
    assert I.V == 0

def test_linear_current_source_with_zero_conductance_has_nan_voltage() -> None:
    I = elm.current_source('Is1', I=sp.Symbol('I'), Y=sp.sympify(0))
    assert I.V == sp.nan

def test_linear_voltage_source_with_zero_resistance_has_inf_conductance() -> None:
    U = elm.voltage_source('Us1', V=sp.Symbol('V'), Z=sp.sympify(0))
    assert U.Y == sp.oo

def test_linear_voltage_source_with_inf_resistance_has_zero_conductance() -> None:
    U = elm.voltage_source('Us1', V=sp.Symbol('V'), Z=sp.sympify('oo'))
    assert U.Y == 0

def test_linear_voltage_source_with_inf_resistance_has_zero_current() -> None:
    U = elm.voltage_source('Us1', V=sp.Symbol('V'), Z=sp.sympify('oo'))
    assert U.I == 0

def test_linear_voltage_source_with_zero_resistance_has_nan_current() -> None:
    U = elm.voltage_source('Us1', V=sp.Symbol('V'), Z=sp.sympify(0))
    assert U.I == sp.nan