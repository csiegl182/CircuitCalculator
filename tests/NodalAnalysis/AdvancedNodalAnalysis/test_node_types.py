import pytest
from CircuitCalculator.AdvancedNodalAnalysis import NodeTypes, AmbiguousElectricalPotential
from CircuitCalculator.Network import Network, Branch, voltage_source, resistor

def test_parallel_voltage_sources_attached_to_node_zero_lead_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(0, 1, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        NodeTypes(network)

def test_parallel_voltage_sources_attached_to_node_zero_inverse_direction_lead_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(1, 0, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        NodeTypes(network)

def test_ambiguous_electrical_potential_leads_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(1, 2, voltage_source(2)),
        Branch(2, 0, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        NodeTypes(network)
    
def test_get_supernodes_identifies_all_supernodes() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    network = Network([
        Branch(0, 1, vs1),
        Branch(1, 2, resistor(2)),
        Branch(2, 3, vs2),
        Branch(3, 0, resistor(2)),
    ])
    nodes = NodeTypes(network)
    assert nodes.get_active_node(vs1) == 1
    assert nodes.get_active_node(vs2) == 2

def test_with_serial_voltage_source_one_source_may_be_connected_to_multiple_supernodes() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    network = Network([
        Branch(0, 1, vs1),
        Branch(1, 2, vs2),
        Branch(2, 0, resistor(2)),
    ])
    nodes = NodeTypes(network)
    assert nodes.get_active_node(vs1) == 1
    assert nodes.get_active_node(vs2) == 2
    
def test_given_a_regular_network_all_active_nodes_are_identified() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    network = Network([
        Branch(0, 1, vs1),
        Branch(1, 2, resistor(2)),
        Branch(2, 3, vs2),
        Branch(3, 0, resistor(2)),
    ])
    nodes = NodeTypes(network)
    assert nodes.is_active(1)
    assert nodes.is_active(2)
    
def test_given_a_regular_network_all_passive_nodes_are_identified() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    network = Network([
        Branch(0, 1, vs1),
        Branch(1, 2, resistor(2)),
        Branch(2, 3, vs2),
        Branch(3, 0, resistor(2)),
    ])
    nodes = NodeTypes(network)
    assert nodes.is_passive(0)
    assert nodes.is_passive(3)

def test_zero_node_is_passive() -> None:
    vs1 = voltage_source(1)
    network = Network([
        Branch(1, 0, vs1),
    ])
    nodes = NodeTypes(network)
    assert nodes.is_passive(0)

def test_parallel_voltage_sources_attached_to_node_zero_inverse_direction_lead_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(1, 0, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        NodeTypes(network)

def test_ambiguous_electrical_potential_leads_to_error() -> None:
    network = Network([
        Branch(0, 1, voltage_source(1)),
        Branch(1, 2, voltage_source(2)),
        Branch(2, 0, voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        NodeTypes(network)
    
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
    nodes = NodeTypes(network)
    assert nodes.get_counterpart(1) == 0
    assert nodes.get_counterpart(2) == 3

def test_get_supernode_counterparts_returns_zero_node() -> None:
    vs1 = voltage_source(1)
    network = Network([
        Branch(0, 1, vs1)
    ])
    nodes = NodeTypes(network)
    assert nodes.get_counterpart(1) == 0