from CircuitCalculator.EquivalentSources import remove_ideal_voltage_sources
from CircuitCalculator.Network import Network, Branch, voltage_source, resistor

def test_all_ideal_voltage_sources_are_removed() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    r1 = resistor(2)
    r2 = resistor(2)
    r3 = resistor(2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', r1),
        Branch('2', '3', r2),
        Branch('3', '4', vs2),
        Branch('4', '0', r3),
    ])
    network = remove_ideal_voltage_sources(network)
    assert any([type(b.element)==type(vs1) for b in network.branches]) == False
    
def test_ideal_voltage_sources_are_substituded_by_short_circuit() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    r1 = resistor(2)
    r2 = resistor(2)
    r3 = resistor(2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', r1),
        Branch('2', '3', r2),
        Branch('3', '4', vs2),
        Branch('4', '0', r3),
    ])
    network = remove_ideal_voltage_sources(network)
    assert r1 in [b.element for b in network.branches_between('0', '2')]
    assert r2 in [b.element for b in network.branches_between('2', '4')]
    assert r3 in [b.element for b in network.branches_between('4', '0')]
    