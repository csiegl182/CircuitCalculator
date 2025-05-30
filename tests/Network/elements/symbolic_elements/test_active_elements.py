from CircuitCalculator.Network.network import Branch
from CircuitCalculator.Network.symbolic_elements import current_source, voltage_source, resistor, conductor
import sympy as sp

def test_resistor_is_not_active() -> None:
    b = Branch('1', '0', resistor('R1', R=sp.Symbol('R')))
    assert b.element.is_active == False

def test_condutor_is_not_active() -> None:
    b = Branch('1', '0', conductor('G1', G=sp.Symbol('G')))
    assert b.element.is_active == False

def test_voltage_source_is_active() -> None:
    b = Branch('1', '0', voltage_source('V1', V=sp.Symbol('V')))
    assert b.element.is_active == True

def test_current_source_is_active() -> None:
    b = Branch('1', '0', current_source('I1', I=sp.Symbol('I')))
    assert b.element.is_active == True

def test_linear_voltage_source_is_active() -> None:
    b = Branch('1', '0', voltage_source('V1', V=sp.Symbol('V'), Z=sp.Symbol('Z')))
    assert b.element.is_active == True

def test_linear_current_source_is_active() -> None:
    b = Branch('1', '0', current_source('I1', I=sp.Symbol('I'), Y=sp.Symbol('Y')))
    assert b.element.is_active == True