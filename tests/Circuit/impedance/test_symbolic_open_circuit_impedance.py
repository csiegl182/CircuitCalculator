from CircuitCalculator.Circuit.impedance import symbolic_open_circuit_dc_resistance
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit.Components import symbolic_components as cp
import sympy as sp
from numpy.testing import assert_almost_equal

def test_impedance_of_simple_network_can_be_calculated() -> None:
    R1, R2 = sp.symbols('R1 R2', real=True, positive=True)
    circuit = Circuit([
        cp.resistor(id='R1', nodes=('1', '0')),
        cp.resistor(id='R2', nodes=('1', '0'))
    ])
    print(symbolic_open_circuit_dc_resistance(circuit, '1', '0'))
    assert symbolic_open_circuit_dc_resistance(circuit, '1', '0') == 1/(1/R1+1/R2)

def test_impedance_of_inductance_is_zero() -> None:
    circuit = Circuit([
        cp.inductance(id='L', nodes=('1', '0')),
        cp.ground(nodes=('0',))
    ])
    assert symbolic_open_circuit_dc_resistance(circuit, '1', '0') == 0

def test_impedance_of_resistor_with_following_short_circuit() -> None:
    R = sp.symbols('R', real=True, positive=True)
    circuit = Circuit([
        cp.resistor(id='R', nodes=('2', '0')),
        cp.short_circuit(id='X', nodes=('1', '2')),
    ])
    assert symbolic_open_circuit_dc_resistance(circuit, '1', '0').nsimplify() == R

def test_impedance_of_resistor_with_voltage_source() -> None:
    R1, R2 = sp.symbols('R1 R2', real=True, positive=True)
    cicuit = Circuit([
        cp.voltage_source(id='V', nodes=('1', '0')),
        cp.resistor(id='R1', nodes=('1', '2')),
        cp.resistor(id='R2', nodes=('2', '0')),
        cp.ground(nodes=('0',)),
    ])
    assert symbolic_open_circuit_dc_resistance(cicuit, '2', '0').simplify().nsimplify() == R1*R2/(R1+R2)

def test_impedance_of_resistor_with_current_source() -> None:
    R = sp.symbols('R', real=True, positive=True)
    cicuit = Circuit([
        cp.current_source(id='I', nodes=('1', '0')),
        cp.resistor(id='R', nodes=('1', '0')),
        cp.ground(nodes=('0',)),
    ])
    assert symbolic_open_circuit_dc_resistance(cicuit, '1', '0') == R

def test_impedance_of_resistor_and_capacitor() -> None:
    R = sp.symbols('R', real=True, positive=True)
    cicuit = Circuit([
        cp.voltage_source(id='V', nodes=('1', '0')),
        cp.resistor(id='R', nodes=('1', '2')),
        cp.capacitor(id='C', nodes=('2', '0')),
        cp.ground(nodes=('0',)),
    ])
    assert symbolic_open_circuit_dc_resistance(cicuit, '2', '0').nsimplify() == R