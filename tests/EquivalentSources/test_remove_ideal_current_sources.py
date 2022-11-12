from CircuitCalculator.EquivalentSources import remove_ideal_current_sources
from CircuitCalculator.Network import Network, Branch, current_source, resistor

def test_all_ideal_current_sources_are_removed() -> None:
    cs1 = current_source(1)
    cs2 = current_source(2)
    r1 = resistor(2)
    r2 = resistor(2)
    r3 = resistor(2)
    network = Network([
        Branch('0', '1', cs1),
        Branch('1', '2', r1),
        Branch('2', '3', r2),
        Branch('3', '4', cs2),
        Branch('4', '0', r3),
    ])
    network = remove_ideal_current_sources(network)
    assert any([type(b.element)==type(cs1) for b in network.branches]) == False

def test_all_passive_elements_are_kept() -> None:
    cs1 = current_source(1)
    cs2 = current_source(2)
    r1 = resistor(2)
    r2 = resistor(2)
    r3 = resistor(2)
    network = Network([
        Branch('0', '1', cs1),
        Branch('1', '2', r1),
        Branch('2', '3', r2),
        Branch('3', '4', cs2),
        Branch('4', '0', r3),
    ])
    network = remove_ideal_current_sources(network)
    assert r1 in [b.element for b in network.branches]
    assert r2 in [b.element for b in network.branches]
    assert r3 in [b.element for b in network.branches]
    