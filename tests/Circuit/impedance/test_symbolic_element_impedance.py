from CircuitCalculator.Circuit.impedance import symbolic_element_impedance
from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.Components.symbolic_components as ccp
import sympy as sp

def test_element_impedance_of_simple_network_can_be_calculated() -> None:
    R2 = sp.symbols('R2', real=True, positive=True)
    circuit = Circuit([
        ccp.resistor(id='R1', nodes=('1', '0')),
        ccp.resistor(id='R2', nodes=('1', '0'))
    ])
    assert symbolic_element_impedance(circuit, 'R1') == R2

def test_element_impedance_of_real_voltage_source() -> None:
    R1 = sp.symbols('R1', real=True, positive=True)
    circuit = Circuit([
        ccp.voltage_source(id='V', nodes=('1', '0')),
        ccp.resistor(id='R1', nodes=('1', '2')),
        ccp.resistor(id='R2', nodes=('2', '0')),
        ccp.ground(nodes=('0',))
    ])
    assert symbolic_element_impedance(circuit, 'R2') == R1

def test_element_impedance_of_linear_voltage_source() -> None:
    circuit = Circuit([
        ccp.voltage_source(id='V', nodes=('1', '0')),
        ccp.resistor(id='R2', nodes=('1', '0')),
        ccp.ground(nodes=('0',))
    ])
    assert symbolic_element_impedance(circuit, 'R2') == 0

def test_element_impedance_of_real_current_source() -> None:
    R1 = sp.symbols('R1', real=True, positive=True)
    circuit = Circuit([
        ccp.current_source(id='I', nodes=('1', '0')),
        ccp.resistor(id='R1', nodes=('1', '0')),
        ccp.resistor(id='R2', nodes=('1', '0')),
        ccp.ground(nodes=('0',))
    ])
    assert symbolic_element_impedance(circuit, 'R2') == R1

def test_element_impedance_of_linear_current_source() -> None:
    G1 = sp.sympify('G1')
    circuit = Circuit([
        ccp.current_source(G='G1', id='I', nodes=('1', '0')),
        ccp.resistor(id='R2', nodes=('1', '0')),
        ccp.ground(nodes=('0',))
    ])
    assert symbolic_element_impedance(circuit, 'R2') == 1/G1