from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import resistor, voltage_source
from CircuitCalculator.Network.NodalAnalysis.node_analysis import open_circuit_voltage
from numpy.testing import assert_almost_equal

def test_open_circuit_voltage_of_equal_nodes_is_zero() -> None:
    V = 1
    R1, R2, R3 = 10, 20, 30
    network = Network([
        Branch('1', '0', voltage_source('V', V)),
        Branch('1', '2', resistor('R1', R1)),
        Branch('1', '2', resistor('R2', R2)),
        Branch('2', '0', resistor('R3', R3)),
        ])
    V0 = open_circuit_voltage(network, '1', '1')

    assert_almost_equal(V0, 0)

def test_open_circuit_voltage() -> None:
    V = 1
    R1, R2, R3 = 10, 20, 30
    network = Network([
        Branch('1', '0', voltage_source('V', V)),
        Branch('1', '2', resistor('R1', R1)),
        Branch('1', '2', resistor('R2', R2)),
        Branch('2', '0', resistor('R3', R3)),
        ])
    V0 = open_circuit_voltage(network, '2', '0')

    assert_almost_equal(V0, V*R3/(R3+R1*R2/(R1+R2)))