import pytest
from CircuitCalculator.AdvancedNodalAnalysis import get_non_supernodes, AmbiguousElectricalPotential
from CircuitCalculator.Network import Network, Branch, voltage_source, resistor

def test_parallel_voltage_sources_lead_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(0, 1, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        get_non_supernodes(network)

def test_parallel_voltage_sources_in_opposite_direction_lead_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(1, 0, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        get_non_supernodes(network)

def test_ambiguous_electrical_potential_leads_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(1, 2, voltage_source(2)),
        Branch(2, 0, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        get_non_supernodes(network)

def test_regular_network_node_zero_is_not_returned() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    network = Network([
        Branch(0, 1, vs1),
        Branch(1, 2, resistor(2)),
        Branch(2, 3, vs2),
        Branch(3, 0, resistor(2)),
    ])
    non_supernodes = get_non_supernodes(network)
    assert 0 not in non_supernodes
    
def test_regular_network_leads_to_correct_list_of_non_supernodes() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    network = Network([
        Branch(0, 1, vs1),
        Branch(1, 2, resistor(2)),
        Branch(2, 3, vs2),
        Branch(3, 0, resistor(2)),
    ])
    non_supernodes = get_non_supernodes(network)
    assert non_supernodes == [3]