from CircuitCalculator.Circuit.impedance import open_circuit_impedance
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit.Components import components as cp

def test_impedance_of_simple_network_can_be_calculated() -> None:
    R = 1
    circuit = Circuit([
        cp.resistor(R=R, id='R1', nodes=('1', '0')),
        cp.resistor(R=R, id='R2', nodes=('1', '0'))
    ])
    assert open_circuit_impedance(circuit, '1', '0') == R/2

def test_impedance_of_inductance_is_zero() -> None:
    L = 100
    circuit = Circuit(components=[cp.inductor(L=L, id='L', nodes=('1', '0'))], ground_node='0')
    assert open_circuit_impedance(circuit, '1', '0') == 0

def test_impedance_of_resistor_with_following_short_circuit() -> None:
    R = 100
    circuit = Circuit([
        cp.resistor(R=R, id='R', nodes=('2', '0')),
        cp.short_circuit(id='X', nodes=('1', '2')),
    ])
    assert open_circuit_impedance(circuit, '1', '0') == R

def test_impedance_of_resistor_with_voltage_source() -> None:
    R = 100
    cicuit = Circuit(
        components=[
            cp.dc_voltage_source(V=1, id='V', nodes=('1', '0')),
            cp.resistor(R=R, id='R1', nodes=('1', '2')),
            cp.resistor(R=R, id='R2', nodes=('2', '0'))
        ],
        ground_node='0'
    )
    assert open_circuit_impedance(cicuit, '2', '0') == R/2

def test_impedance_of_resistor_with_current_source() -> None:
    R = 100
    cicuit = Circuit(
        components=[
            cp.dc_current_source(I=1, id='I', nodes=('1', '0')),
            cp.resistor(R=R, id='R', nodes=('1', '0'))
        ],
        ground_node='0'
    )
    assert open_circuit_impedance(cicuit, '1', '0') == R

def test_impedance_of_resistor_and_capacitor() -> None:
    R, C = 100, 200
    cicuit = Circuit(
        components=[
            cp.dc_voltage_source(V=1, id='V', nodes=('1', '0')),
            cp.resistor(R=R, id='R', nodes=('1', '2')),
            cp.capacitor(C=C, id='C', nodes=('2', '0'))
        ],
        ground_node='0'
    )
    assert open_circuit_impedance(cicuit, '2', '0') == R