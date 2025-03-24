from CircuitCalculator.Network.network import Branch
from CircuitCalculator.Network.symbolic_elements import voltage_source, resistor, conductor, current_source
import sympy as sp

def test_ideal_voltage_source_is_detected() -> None:
    b = Branch('1', '0', voltage_source('Us1', V=sp.Symbol('V')))
    assert b.element.is_ideal_voltage_source == True
    assert b.element.is_voltage_source == True

def test_linear_voltage_source_is_detected() -> None:
    b = Branch('1', '0', voltage_source('Us1', V=sp.Symbol('V')))
    assert b.element.is_voltage_source == True

def test_linear_voltage_source_is_not_ideal() -> None:
    b = Branch('1', '0', voltage_source('Us1', V=sp.Symbol('V'), Z=sp.Symbol('Z')))
    assert b.element.is_ideal_voltage_source == False

def test_resistor_is_not_ideal_voltage_source() -> None:
    b = Branch('1', '0', resistor('R1', R=sp.Symbol('R')))
    assert b.element.is_ideal_voltage_source == False

def test_resistor_is_not_voltage_source() -> None:
    b = Branch('1', '0', resistor('R1', R=sp.Symbol('R')))
    assert b.element.is_voltage_source == False

def test_conductor_is_not_ideal_voltage_source() -> None:
    b = Branch('1', '0', conductor('G1', G=sp.Symbol('G')))
    assert b.element.is_ideal_voltage_source == False

def test_conductor_is_not_voltage_source() -> None:
    b = Branch('1', '0', conductor('G1', G=sp.Symbol('G')))
    assert b.element.is_voltage_source == False

def test_current_source_is_not_voltage_source() -> None:
    b = Branch('1', '0', current_source('Is1', I=sp.Symbol('I')))
    assert b.element.is_voltage_source == False