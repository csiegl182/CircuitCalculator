from CircuitCalculator.Circuit.impedance import symbolic_open_circuit_dc_resistance
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit.Components import symbolic_components as cp
import sympy as sp
from numpy.testing import assert_almost_equal

def test_impedance_of_simple_network_can_be_calculated() -> None:
    R1, R2 = '2', '3'
    circuit = Circuit([
        cp.resistor(R=R1, id='R1', nodes=('1', '0')),
        cp.resistor(R=R2, id='R2', nodes=('1', '0'))
    ])
    assert symbolic_open_circuit_dc_resistance(circuit, '1', '0') == sp.sympify(f'1/(1/{R1} + 1/{R2})')

def test_impedance_of_inductance_is_zero() -> None:
    L = '100'
    circuit = Circuit([
        cp.inductance(L=L, id='L', nodes=('1', '0')),
        cp.ground(nodes=('0',))
    ])
    assert symbolic_open_circuit_dc_resistance(circuit, '1', '0') == 0

def test_impedance_of_resistor_with_following_short_circuit() -> None:
    R = '100'
    circuit = Circuit([
        cp.resistor(R=R, id='R', nodes=('2', '0')),
        cp.short_circuit(id='X', nodes=('1', '2')),
    ])
    assert symbolic_open_circuit_dc_resistance(circuit, '1', '0') == sp.sympify(R)

def test_impedance_of_resistor_with_voltage_source() -> None:
    R = '100'
    cicuit = Circuit([
        cp.voltage_source(id='V', nodes=('1', '0')),
        cp.resistor(R=R, id='R1', nodes=('1', '2')),
        cp.resistor(R=R, id='R2', nodes=('2', '0')),
        cp.ground(nodes=('0',)),
    ])
    assert_almost_equal(float(symbolic_open_circuit_dc_resistance(cicuit, '2', '0')), float(sp.sympify(f'{R}/2')), decimal=5)

def test_impedance_of_resistor_with_current_source() -> None:
    R = '100'
    cicuit = Circuit([
        cp.current_source(id='I', nodes=('1', '0')),
        cp.resistor(R=R, id='R', nodes=('1', '0')),
        cp.ground(nodes=('0',)),
    ])
    assert symbolic_open_circuit_dc_resistance(cicuit, '1', '0') == sp.sympify(R)

def test_impedance_of_resistor_and_capacitor() -> None:
    R, C = '100', '200'
    cicuit = Circuit([
        cp.voltage_source(id='V', nodes=('1', '0')),
        cp.resistor(R=R, id='R', nodes=('1', '2')),
        cp.capacitor(C=C, id='C', nodes=('2', '0')),
        cp.ground(nodes=('0',)),
    ])
    assert symbolic_open_circuit_dc_resistance(cicuit, '2', '0') == sp.sympify(R)