from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor, voltage_source
from CircuitCalculator.Network.NodalAnalysis import element_impedance
from numpy.testing import assert_almost_equal

def test_total_impedeance_returns_zero_on_element_parallel_to_voltage_source() -> None:
    V, R, = 1, 10
    network = Network([
        Branch('1', '0', voltage_source('V', V)),
        Branch('1', '0', resistor('R', R)),
        ])
    assert element_impedance(network, 'R') == 0

def test_total_impedeance_returns_correct_values() -> None:
    R1, R2, R3, R4 = 10, 20, 30, 40
    network = Network([
        Branch('0', '1', resistor('R1', R1)),
        Branch('1', '2', resistor('R2', R2)),
        Branch('2', '0', resistor('R3', R3)),
        Branch('2', '0', resistor('R4', R4)),
        ])
    assert_almost_equal(element_impedance(network, 'R1'), R2+(R3*R4)/(R3+R4), decimal=4)
    assert_almost_equal(element_impedance(network, 'R2'), R1+(R3*R4)/(R3+R4), decimal=4)
    assert_almost_equal(element_impedance(network, 'R3'), R4*(R1+R2)/(R1+R2+R4), decimal=4)
    assert_almost_equal(element_impedance(network, 'R4'), R3*(R1+R2)/(R1+R2+R3), decimal=4)
