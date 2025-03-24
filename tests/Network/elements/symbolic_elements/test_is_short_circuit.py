from CircuitCalculator.Network.network import Branch
from CircuitCalculator.Network.symbolic_elements import voltage_source, current_source, resistor, conductor
import sympy as sp

def test_ideal_voltage_source_is_not_short_circuit() -> None:
    b = Branch('1', '0', voltage_source('Vs1', V=sp.Symbol('V')))
    assert b.element.is_short_circuit == False

def test_ideal_voltage_source_with_zero_voltage_is_short_circuit() -> None:
    b = Branch('1', '0', voltage_source('Vs1', V=sp.sympify(0)))
    assert b.element.is_short_circuit == True

def test_voltage_source_is_not_short_circuit() -> None:
    b = Branch('1', '0', voltage_source('Vs1', V=sp.Symbol('V'), Z=sp.Symbol('Z')))
    assert b.element.is_short_circuit == False

def test_voltage_source_with_zero_voltage_is_not_short_circuit() -> None:
    b = Branch('1', '0', voltage_source('Vs1', V=sp.sympify(0), Z=sp.Symbol('Z')))
    assert b.element.is_short_circuit == False

def test_ideal_current_source_is_not_short_circuit() -> None:
    b = Branch('1', '0', current_source('Is1', I=sp.Symbol('I')))
    assert b.element.is_short_circuit == False

def test_ideal_current_source_with_zero_current_is_not_short_circuit() -> None:
    b = Branch('1', '0', current_source('Is1', I=sp.sympify(0)))
    assert b.element.is_short_circuit == False

def test_current_source_is_not_short_circuit() -> None:
    b = Branch('1', '0', current_source('Is1', I=sp.Symbol('I'), Y=sp.Symbol('Y')))
    assert b.element.is_short_circuit == False

def test_current_source_with_zero_current_is_not_short_circuit() -> None:
    b = Branch('1', '0', current_source('Is1', I=sp.sympify(0), Y=sp.Symbol('Y')))
    assert b.element.is_short_circuit == False

def test_resistor_is_not_short_circuit() -> None:
    b = Branch('1', '0', resistor('R1', R=sp.Symbol('R')))
    assert b.element.is_short_circuit == False

def test_conductor_is_not_short_circuit() -> None:
    b = Branch('1', '0', conductor('G1', G=sp.Symbol('G')))
    assert b.element.is_short_circuit == False