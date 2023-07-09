from CircuitCalculator.Circuit.impedance import open_circuit_impedance
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit.components import Resistor

def test_impedance_of_simple_network_can_be_calculated() -> None:
    R = 1
    circuit = Circuit([
        Resistor(R=R, id='R1', nodes=('1', '0')),
        Resistor(R=R, id='R2', nodes=('1', '0'))
    ])
    assert open_circuit_impedance(circuit, '1', '0') == R/2
