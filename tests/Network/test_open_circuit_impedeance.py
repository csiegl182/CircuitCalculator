from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor, voltage_source
from CircuitCalculator.Network.equivalent_sources import open_circuit_impedance
from numpy.testing import assert_almost_equal

def test_total_impedeance_returns_zero_on_equal_nodes() -> None:
    R1, R2, R3 = 10, 20, 30
    network = Network([
        Branch('0', '1', resistor('R1', R1)),
        Branch('1', '2', resistor('R2', R2)),
        Branch('2', '0', resistor('R3', R3)),
        ])
    assert open_circuit_impedance(network, '0', '0') == 0
    assert open_circuit_impedance(network, '1', '1') == 0
    assert open_circuit_impedance(network, '2', '2') == 0

def test_total_impedeance_returns_zero_on_nodes_of_ideal_voltage_source() -> None:
    Uq = 1
    R1, R2, R3 = 10, 20, 30
    network = Network([
        Branch('0', '1', voltage_source('Uq', Uq)),
        Branch('1', '2', resistor('R1', R1)),
        Branch('2', '3', resistor('R2', R2)),
        Branch('3', '0', resistor('R3', R3)),
        ])
    assert open_circuit_impedance(network, '0', '1') == 0

def test_total_impedeance_returns_correct_values() -> None:
    R1, R2, R3 = 10, 20, 30
    network = Network([
        Branch('0', '1', resistor('R1', R1)),
        Branch('1', '2', resistor('R2', R2)),
        Branch('2', '0', resistor('R3', R3)),
        ])
    assert_almost_equal(open_circuit_impedance(network, '1', '0'), R1*(R2+R3)/(R1+R2+R3), decimal=4)
    assert_almost_equal(open_circuit_impedance(network, '2', '0'), (R1+R2)*R3/(R1+R2+R3), decimal=4)
    assert_almost_equal(open_circuit_impedance(network, '1', '2'), R2*(R1+R3)/(R1+R2+R3), decimal=4)
    assert_almost_equal(open_circuit_impedance(network, '0', '1'), R1*(R2+R3)/(R1+R2+R3), decimal=4)
    assert_almost_equal(open_circuit_impedance(network, '0', '2'), (R1+R2)*R3/(R1+R2+R3), decimal=4)