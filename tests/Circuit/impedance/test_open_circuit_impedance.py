from CircuitCalculator.Circuit.impedance import open_circuit_impedance
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit.Components.components import resistor, inductance, ground, short_circuit

def test_impedance_of_simple_network_can_be_calculated() -> None:
    R = 1
    circuit = Circuit([
        resistor(R=R, id='R1', nodes=('1', '0')),
        resistor(R=R, id='R2', nodes=('1', '0'))
    ])
    assert open_circuit_impedance(circuit, '1', '0') == R/2

def test_impedance_of_inductance_is_zero() -> None:
    L = 100
    R = 100
    circuit = Circuit([
        inductance(L=L, id='L', nodes=('1', '0')),
        ground(nodes=('0',))
    ])
    assert open_circuit_impedance(circuit, '1', '0') == 0

def test_impedance_of_resistor_with_following_short_circuit() -> None:
    L = 100
    R = 100
    circuit = Circuit([
        resistor(R=R, id='R', nodes=('2', '0')),
        short_circuit(id='X', nodes=('1', '2')),
    ])
    assert open_circuit_impedance(circuit, '1', '0') == R