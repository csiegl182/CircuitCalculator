import pytest
from CircuitCalculator.AdvancedNodalAnalysis import get_supernode_counterparts, AmbiguousElectricalPotential
from CircuitCalculator.Network import Network, Branch, voltage_source, resistor

def test_parallel_voltage_sources_attached_to_node_zero_lead_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(0, 1, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        get_supernode_counterparts(network)

def test_parallel_voltage_sources_attached_to_node_zero_inverse_direction_lead_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(1, 0, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        get_supernode_counterparts(network)

def test_ambiguous_electrical_potential_leads_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(1, 2, voltage_source(2)),
        Branch(2, 0, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        get_supernode_counterparts(network)
    
def test_get_supernode_counterparts_identifies_all_counterparts() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    r1 = resistor(2)
    r2 = resistor(2)
    network = Network([
        Branch(0, 1, vs1),
        Branch(1, 2, r1),
        Branch(2, 3, vs2),
        Branch(3, 0, r2),
    ])
    counterparts = get_supernode_counterparts(network)
    assert counterparts[3].element == vs2

def test_get_supernode_counterparts_does_not_return_zero_node() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    r1 = resistor(2)
    r2 = resistor(2)
    network = Network([
        Branch(0, 1, vs1),
        Branch(1, 2, r1),
        Branch(2, 3, vs2),
        Branch(3, 0, r2),
    ])
    counterparts = get_supernode_counterparts(network)
    assert 0 not in counterparts.keys()


def test_get_supernode_counterparts_does_not_return_supernodes() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    r1 = resistor(2)
    r2 = resistor(2)
    network = Network([
        Branch(0, 1, vs1),
        Branch(1, 2, vs2),
        Branch(1, 2, r1),
        Branch(3, 0, r2),
    ])
    counterparts = get_supernode_counterparts(network)
    assert counterparts == {}
    