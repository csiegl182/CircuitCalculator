import pytest
from CircuitCalculator.Network.supernodes import SuperNodes, AmbiguousElectricalPotential
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import voltage_source, resistor

def test_parallel_voltage_sources_attached_to_node_zero_lead_to_error() -> None:
    network = Network([
        Branch('0', '1', voltage_source('Us1', 1)),
        Branch('0', '1', voltage_source('Us2', 2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        SuperNodes(network)

def test_parallel_voltage_sources_attached_to_node_zero_inverse_direction_lead_to_error() -> None:
    network = Network([
        Branch('0', '1', voltage_source('Us1', 1)),
        Branch('1', '0', voltage_source('Us2', 2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        SuperNodes(network)

def test_ambiguous_electrical_potential_leads_to_error() -> None:
    network = Network([
        Branch('0', '1', voltage_source('Us1', 1)),
        Branch('1', '2', voltage_source('Us2', 2)),
        Branch('2', '0', voltage_source('Us3', 2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        SuperNodes(network)
    
def test_given_a_regular_network_all_active_nodes_are_identified() -> None:
    vs1 = voltage_source('Us1', 1)
    vs2 = voltage_source('Us2', 2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', resistor('R1', 2)),
        Branch('2', '3', vs2),
        Branch('3', '0', resistor('R2', 2)),
    ])
    nodes = SuperNodes(network)
    assert nodes.is_active('1')
    assert nodes.is_active('2')
    
def test_given_a_regular_network_all_passive_nodes_are_identified() -> None:
    vs1 = voltage_source('Us1', 1)
    vs2 = voltage_source('Us2', 2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', resistor('R1', 2)),
        Branch('2', '3', vs2),
        Branch('3', '0', resistor('R2', 2)),
    ])
    nodes = SuperNodes(network)
    assert nodes.is_reference('0')
    assert nodes.is_reference('3')

def test_zero_node_is_passive() -> None:
    vs1 = voltage_source('Us1', 1)
    network = Network([
        Branch('1', '0', vs1),
    ])
    nodes = SuperNodes(network)
    assert nodes.is_reference('0')
    
def test_get_supernode_counterparts_identifies_all_counterparts() -> None:
    vs1 = voltage_source('Us1', 1)
    vs2 = voltage_source('Us2', 2)
    r1 = resistor('R1', 2)
    r2 = resistor('R2', 2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', r1),
        Branch('2', '3', vs2),
        Branch('3', '0', r2),
    ])
    nodes = SuperNodes(network)
    assert nodes.get_reference_node('1') == '0'
    assert nodes.get_reference_node('2') == '3'

def test_get_supernode_counterparts_returns_zero_node() -> None:
    vs1 = voltage_source('Us1', 1)
    network = Network([
        Branch('0', '1', vs1)
    ])
    nodes = SuperNodes(network)
    assert network.is_zero_node(nodes.get_reference_node('1'))
    
def test_get_counterparts_of_non_active_node_raises_value_error() -> None:
    vs1 = voltage_source('Us1', 1)
    vs2 = voltage_source('Us2', 2)
    r1 = resistor('R1', 2)
    r2 = resistor('R2', 2)
    r3 = resistor('R3', 2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', r1),
        Branch('2', '3', r2),
        Branch('3', '4', vs2),
        Branch('4', '0', r3),
    ])
    nodes = SuperNodes(network)
    with pytest.raises(ValueError):
        nodes.get_reference_node('2')

def test_nodes_belonging_to_one_supernode() -> None:
    vs = voltage_source('Us1', 1)
    r1 = resistor('R1', 2)
    r2 = resistor('R2', 2)
    network = Network([
        Branch('0', '1', r1),
        Branch('1', '2', vs),
        Branch('2', '0', r2),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='1', reference_node='2') == True

def test_nodes_belonging_to_one_supernode_but_given_in_incorrect_order() -> None:
    vs = voltage_source('Us1', 1)
    r1 = resistor('R1', 2)
    r2 = resistor('R2', 2)
    network = Network([
        Branch('0', '1', r1),
        Branch('1', '2', vs),
        Branch('2', '0', r2),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='2', reference_node='1') == False

def test_active_node_belonging_to_supernode_but_reference_node_not() -> None:
    vs = voltage_source('Us1', 1)
    r1 = resistor('R1', 2)
    r2 = resistor('R2', 2)
    r3 = resistor('R3', 2)
    network = Network([
        Branch('0', '1', r1),
        Branch('1', '2', vs),
        Branch('2', '3', r2),
        Branch('3', '0', r3),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='1', reference_node='3') == False

def test_reference_node_belonging_to_supernode_but_active_node_not() -> None:
    vs = voltage_source('Us1', 1)
    r1 = resistor('R1', 2)
    r2 = resistor('R2', 2)
    r3 = resistor('R3', 2)
    network = Network([
        Branch('0', '1', r1),
        Branch('1', '2', vs),
        Branch('2', '3', r2),
        Branch('3', '0', r3),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='3', reference_node='2') == False

def test_active_node_and_reference_node_belonging_to_one_supernode_and_reference_node_is_also_active() -> None:
    vs1 = voltage_source('Us1', 1)
    vs2 = voltage_source('Us2', 2)
    r1 = resistor('R1', 2)
    r2 = resistor('R2', 2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', vs2),
        Branch('2', '3', r1),
        Branch('3', '0', r2),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='2', reference_node='1') == True

def test_active_node_is_reference_node_of_another_supernode_and_its_active_node() -> None:
    vs1 = voltage_source('Us1', 1)
    vs2 = voltage_source('Us2', 2)
    r1 = resistor('R1', 2)
    r2 = resistor('R2', 2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', vs2),
        Branch('2', '3', r1),
        Branch('3', '0', r2),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='1', reference_node='2') == False