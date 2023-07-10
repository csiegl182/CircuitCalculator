from CircuitCalculator.Circuit.impedance import element_impedance
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit.components import Resistor

def test_element_impedance_of_simple_network_can_be_calculated() -> None:
    R = 1
    circuit = Circuit([
        Resistor(R=R, id='R1', nodes=('1', '0')),
        Resistor(R=R, id='R2', nodes=('1', '0'))
    ])
    assert element_impedance(circuit, 'R1') == R
