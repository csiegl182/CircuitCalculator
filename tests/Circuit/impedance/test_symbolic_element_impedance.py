from CircuitCalculator.Circuit.impedance import symbolic_element_impedance
from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.Components.symbolic_components as ccp
import sympy as sp

def test_element_impedance_of_simple_network_can_be_calculated() -> None:
    R = '1'
    circuit = Circuit([
        ccp.resistor(R=R, id='R1', nodes=('1', '0')),
        ccp.resistor(R=R, id='R2', nodes=('1', '0'))
    ])
    assert symbolic_element_impedance(circuit, 'R1') == sp.sympify(R)

def test_element_impedance_of_real_voltage_source() -> None:
    R1, R2 = '1', '2'
    circuit = Circuit([
        ccp.voltage_source(id='V', nodes=('1', '0')),
        ccp.resistor(R=R1, id='R1', nodes=('1', '2')),
        ccp.resistor(R=R2, id='R2', nodes=('2', '0')),
        ccp.ground(nodes=('0',))
    ])
    assert symbolic_element_impedance(circuit, 'R2') == sp.sympify(R1)

def test_element_impedance_of_linear_voltage_source() -> None:
    R1, R2 = '1', '2'
    circuit = Circuit([
        ccp.voltage_source(R=R1, id='V', nodes=('1', '0')),
        ccp.resistor(R=R2, id='R2', nodes=('1', '0')),
        ccp.ground(nodes=('0',))
    ])
    assert symbolic_element_impedance(circuit, 'R2') == sp.sympify(R1)

def test_element_impedance_of_real_current_source() -> None:
    R1, R2 = '1', '2'
    circuit = Circuit([
        ccp.current_source(id='I', nodes=('1', '0')),
        ccp.resistor(R=R1, id='R1', nodes=('1', '0')),
        ccp.resistor(R=R2, id='R2', nodes=('1', '0')),
        ccp.ground(nodes=('0',))
    ])
    assert symbolic_element_impedance(circuit, 'R2') == sp.sympify(R1)

def test_element_impedance_of_linear_current_source() -> None:
    R1, R2 = '1', '2'
    circuit = Circuit([
        ccp.current_source(G=f'1/{R1}', id='I', nodes=('1', '0')),
        ccp.resistor(R=R2, id='R2', nodes=('1', '0')),
        ccp.ground(nodes=('0',))
    ])
    assert symbolic_element_impedance(circuit, 'R2') == sp.sympify(R1)