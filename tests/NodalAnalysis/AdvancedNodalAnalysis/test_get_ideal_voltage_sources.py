from CircuitCalculator.AdvancedNodalAnalysis import ideal_voltage_sources
from CircuitCalculator.Network import Network, Branch, resistor, voltage_source, real_voltage_source, current_source, real_current_source

def test_ideal_voltage_sources_are_selected_from_network() -> None:
    vs1 = Branch(2, 3, voltage_source(1))
    vs2 = Branch(4, 3, voltage_source(2))
    network = Network([
        Branch(1, 0, resistor(10)),
        Branch(1, 2, resistor(12)),
        Branch(2, 0, resistor(20)),
        vs1,
        vs2
    ])
    voltage_sources = ideal_voltage_sources(network)
    assert voltage_sources.branches == [vs1, vs2]

def test_real_voltage_sources_are_not_selected_from_network() -> None:
    network = Network([
        Branch(1, 0, resistor(10)),
        Branch(1, 2, resistor(12)),
        Branch(2, 0, resistor(20)),
        Branch(2, 3, real_voltage_source(1, 10)),
        Branch(4, 3, real_voltage_source(2, 10))
    ])
    voltage_sources = ideal_voltage_sources(network)
    assert len(voltage_sources.branches) == 0

def test_current_sources_are_not_selected_from_network() -> None:
    network = Network([
        Branch(1, 0, resistor(10)),
        Branch(1, 2, resistor(12)),
        Branch(2, 0, resistor(20)),
        Branch(2, 3, current_source(1)),
        Branch(4, 3, current_source(2))
    ])
    voltage_sources = ideal_voltage_sources(network)
    assert len(voltage_sources.branches) == 0

def test_real_current_sources_are_not_selected_from_network() -> None:
    network = Network([
        Branch(1, 0, resistor(10)),
        Branch(1, 2, resistor(12)),
        Branch(2, 0, resistor(20)),
        Branch(2, 3, real_current_source(1, 10)),
        Branch(4, 3, real_current_source(2, 10))
    ])
    voltage_sources = ideal_voltage_sources(network)
    assert len(voltage_sources.branches) == 0