from CircuitCalculator.Network import Network, Branch, resistor
from CircuitCalculator.EquivalentSources import calculate_total_impedeance
from numpy.testing import assert_almost_equal

def test_total_impedeance_returns_zero_on_equal_nodes() -> None:
    network = Network([
        Branch(0, 1, resistor(10)),
        Branch(1, 2, resistor(20)),
        Branch(2, 0, resistor(30)),
        ])
    assert calculate_total_impedeance(network, 0, 0) == 0
    assert calculate_total_impedeance(network, 1, 1) == 0
    assert calculate_total_impedeance(network, 2, 2) == 0

def test_total_impedeance_returns_correct_values() -> None:
    R1, R2, R3 = 10, 20, 30
    network = Network([
        Branch(0, 1, resistor(R1)),
        Branch(1, 2, resistor(R2)),
        Branch(2, 0, resistor(R3)),
        ])
    assert_almost_equal(calculate_total_impedeance(network, 1, 0), R1*(R2+R3)/(R1+R2+R3), decimal=4)
    assert_almost_equal(calculate_total_impedeance(network, 2, 0), (R1+R2)*R3/(R1+R2+R3), decimal=4)
    assert_almost_equal(calculate_total_impedeance(network, 1, 2), R2*(R1+R3)/(R1+R2+R3), decimal=4)
    assert_almost_equal(calculate_total_impedeance(network, 0, 1), R1*(R2+R3)/(R1+R2+R3), decimal=4)
    assert_almost_equal(calculate_total_impedeance(network, 0, 2), (R1+R2)*R3/(R1+R2+R3), decimal=4)