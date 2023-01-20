from CircuitCalculator.Network.network import Network, Branch, ideal_voltage_sources
from CircuitCalculator.Network.elements import resistor, voltage_source, linear_voltage_source, current_source, linear_current_source

def test_ideal_voltage_sources_are_selected_from_network() -> None:
    vs1 = Branch('2', '3', voltage_source('Us1', 1))
    vs2 = Branch('4', '3', voltage_source('Us2', 2))
    network = Network([
        Branch('1', '0', resistor('R1', 10)),
        Branch('1', '2', resistor('R2', 12)),
        Branch('2', '0', resistor('R3', 20)),
        vs1,
        vs2
    ])
    voltage_sources = ideal_voltage_sources(network)
    assert voltage_sources == [vs1, vs2]

def test_linear_voltage_sources_are_not_selected_from_network() -> None:
    network = Network([
        Branch('1', '0', resistor('R1', 10)),
        Branch('1', '2', resistor('R2', 12)),
        Branch('2', '0', resistor('R3', 20)),
        Branch('2', '3', linear_voltage_source('Us1', 1, 10)),
        Branch('4', '3', linear_voltage_source('Us2', 2, 10))
    ])
    voltage_sources = ideal_voltage_sources(network)
    assert len(voltage_sources) == 0

def test_current_sources_are_not_selected_from_network() -> None:
    network = Network([
        Branch('1', '0', resistor('R1', 10)),
        Branch('1', '2', resistor('R2', 12)),
        Branch('2', '0', resistor('R3', 20)),
        Branch('2', '3', current_source('Is1', 1)),
        Branch('4', '3', current_source('Is2', 2))
    ])
    voltage_sources = ideal_voltage_sources(network)
    assert len(voltage_sources) == 0

def test_linear_current_sources_are_not_selected_from_network() -> None:
    network = Network([
        Branch('1', '0', resistor('R1', 10)),
        Branch('1', '2', resistor('R2', 12)),
        Branch('2', '0', resistor('R3', 20)),
        Branch('2', '3', linear_current_source('Is1', 1, 10)),
        Branch('4', '3', linear_current_source('Is2', 2, 10))
    ])
    voltage_sources = ideal_voltage_sources(network)
    assert len(voltage_sources) == 0