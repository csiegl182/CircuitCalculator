from CircuitCalculator.Circuit.impedance import element_impedance
from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.Components.components as ccp

def test_element_impedance_of_simple_network_can_be_calculated() -> None:
    R = 1
    circuit = Circuit([
        ccp.resistor(R=R, id='R1', nodes=('1', '0')),
        ccp.resistor(R=R, id='R2', nodes=('1', '0'))
    ])
    assert element_impedance(circuit, 'R1') == R

def test_element_impedance_of_real_voltage_source() -> None:
    V, R1, R2 = 1, 1, 2
    circuit = Circuit(
        components=[
            ccp.dc_voltage_source(V=V, id='V', nodes=('1', '0')),
            ccp.resistor(R=R1, id='R1', nodes=('1', '2')),
            ccp.resistor(R=R2, id='R2', nodes=('2', '0'))
        ],
        ground_node='0'
    )
    assert element_impedance(circuit, 'R2') == R1

def test_element_impedance_of_linear_voltage_source() -> None:
    V, R1, R2 = 1, 1, 2
    circuit = Circuit(
        components=[
            ccp.dc_voltage_source(V=V, R=R1, id='V', nodes=('1', '0')),
            ccp.resistor(R=R2, id='R2', nodes=('1', '0'))
        ],
        ground_node='0'
    )
    assert element_impedance(circuit, 'R2') == R1

def test_element_impedance_of_real_current_source() -> None:
    I, R1, R2 = 1, 1, 2
    circuit = Circuit(
        components=[
            ccp.dc_current_source(I=I, id='I', nodes=('1', '0')),
            ccp.resistor(R=R1, id='R1', nodes=('1', '0')),
            ccp.resistor(R=R2, id='R2', nodes=('1', '0'))
        ],
        ground_node='0'
    )
    assert element_impedance(circuit, 'R2') == R1

def test_element_impedance_of_linear_current_source() -> None:
    I, R1, R2 = 1, 1, 2
    circuit = Circuit(
        components=[
            ccp.dc_current_source(I=I, G=1/R1, id='I', nodes=('1', '0')),
            ccp.resistor(R=R2, id='R2', nodes=('1', '0'))
        ],
        ground_node='0'
    )
    assert element_impedance(circuit, 'R2') == R1