from AdvancedNodalAnalysis import remove_ideal_voltage_sources
from Network import Network, Branch, resistor, voltage_source, real_voltage_source, current_source, real_current_source

def test_ideal_voltage_sources_are_removed_from_network() -> None:
    vs1 = Branch(2, 3, voltage_source(1))
    vs2 = Branch(4, 3, voltage_source(2))
    b1 =  Branch(1, 0, resistor(10))
    b2 =  Branch(1, 2, resistor(12))
    b3 =  Branch(2, 0, resistor(20))
    network = Network([
        b1,
        b2,
        b3,
        vs1,
        vs2
    ])
    voltage_sources = remove_ideal_voltage_sources(network)
    assert voltage_sources.branches == [b1, b2, b3]

def test_real_voltage_sources_are_not_removed_from_network() -> None:
    network = Network([
        Branch(1, 0, resistor(10)),
        Branch(1, 2, resistor(12)),
        Branch(2, 0, resistor(20)),
        Branch(2, 3, real_voltage_source(1, 10)),
        Branch(4, 3, real_voltage_source(2, 10))
    ])
    voltage_sources = remove_ideal_voltage_sources(network)
    assert len(voltage_sources.branches) == len(network.branches)

def test_current_sources_are_not_removed_from_network() -> None:
    network = Network([
        Branch(1, 0, resistor(10)),
        Branch(1, 2, resistor(12)),
        Branch(2, 0, resistor(20)),
        Branch(2, 3, current_source(1)),
        Branch(4, 3, current_source(2))
    ])
    voltage_sources = remove_ideal_voltage_sources(network)
    assert len(voltage_sources.branches) == len(network.branches)

def test_real_current_sources_are_not_removed_from_network() -> None:
    network = Network([
        Branch(1, 0, resistor(10)),
        Branch(1, 2, resistor(12)),
        Branch(2, 0, resistor(20)),
        Branch(2, 3, real_current_source(1, 10)),
        Branch(4, 3, real_current_source(2, 10))
    ])
    voltage_sources = remove_ideal_voltage_sources(network)
    assert len(voltage_sources.branches) == len(network.branches)