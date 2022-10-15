import pytest
from AdvancedNodalAnalysis import get_supernodes, AmbiguousElectricalPotential
from Network import Network, Branch, voltage_source, resistor

def test_parallel_voltage_sources_attached_to_node_zero_lead_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(0, 1, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        get_supernodes(network)

def test_parallel_voltage_sources_attached_to_node_zero_inverse_direction_lead_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(1, 0, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        get_supernodes(network)

def test_ambiguous_electrical_potential_leads_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(1, 2, voltage_source(2)),
        Branch(2, 0, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        get_supernodes(network)
    
def test_get_supernodes_identifies_all_supernodes() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    network = Network([
        Branch(0, 1, vs1),
        Branch(1, 2, resistor(2)),
        Branch(2, 3, vs2),
        Branch(3, 0, resistor(2)),
    ])
    supernodes = get_supernodes(network)
    assert supernodes[1].element == vs1
    assert supernodes[2].element == vs2
    