import pytest
from CircuitCalculator.Network import SuperNodes, AmbiguousElectricalPotential, Network, Branch, voltage_source, resistor

def test_parallel_voltage_sources_attached_to_node_zero_lead_to_error() -> None:
    network = Network([
        Branch('0', '1', voltage_source(1)),
        Branch('0', '1', voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        SuperNodes(network)

def test_parallel_voltage_sources_attached_to_node_zero_inverse_direction_lead_to_error() -> None:
    network = Network([
        Branch('0', '1', voltage_source(1)),
        Branch('1', '0', voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        SuperNodes(network)

def test_ambiguous_electrical_potential_leads_to_error() -> None:
    network = Network([
        Branch('0', '1', voltage_source(1)),
        Branch('1', '2', voltage_source(2)),
        Branch('2', '0', voltage_source(2))
    ])
    with pytest.raises(AmbiguousElectricalPotential):
        SuperNodes(network)
    
def test_get_supernodes_identifies_all_supernodes() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', resistor(2)),
        Branch('2', '3', vs2),
        Branch('3', '0', resistor(2)),
    ])
    nodes = SuperNodes(network)
    assert nodes.get_active_node(vs1) == '1'
    assert nodes.get_active_node(vs2) == '2'

def test_with_serial_voltage_source_one_source_may_be_connected_to_multiple_supernodes() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', vs2),
        Branch('2', '0', resistor(2)),
    ])
    nodes = SuperNodes(network)
    assert nodes.get_active_node(vs1) == '1'
    assert nodes.get_active_node(vs2) == '2'
    
def test_given_a_regular_network_all_active_nodes_are_identified() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', resistor(2)),
        Branch('2', '3', vs2),
        Branch('3', '0', resistor(2)),
    ])
    nodes = SuperNodes(network)
    assert nodes.is_active('1')
    assert nodes.is_active('2')
    
def test_given_a_regular_network_all_passive_nodes_are_identified() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', resistor(2)),
        Branch('2', '3', vs2),
        Branch('3', '0', resistor(2)),
    ])
    nodes = SuperNodes(network)
    assert nodes.is_reference('0')
    assert nodes.is_reference('3')

def test_zero_node_is_passive() -> None:
    vs1 = voltage_source(1)
    network = Network([
        Branch('1', '0', vs1),
    ])
    nodes = SuperNodes(network)
    assert nodes.is_reference('0')
    
def test_get_supernode_counterparts_identifies_all_counterparts() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    r1 = resistor(2)
    r2 = resistor(2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', r1),
        Branch('2', '3', vs2),
        Branch('3', '0', r2),
    ])
    nodes = SuperNodes(network)
    assert nodes.get_counterpart('1') == '0'
    assert nodes.get_counterpart('2') == '3'

def test_get_supernode_counterparts_returns_zero_node() -> None:
    vs1 = voltage_source(1)
    network = Network([
        Branch('0', '1', vs1)
    ])
    nodes = SuperNodes(network)
    assert network.is_zero_node(nodes.get_counterpart('1'))
    
def test_get_counterparts_of_non_active_node_raises_value_error() -> None:
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
    nodes = SuperNodes(network)
    with pytest.raises(ValueError):
        nodes.get_counterpart('2')

def test_defined_voltage_is_found() -> None:
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
    nodes = SuperNodes(network)
    assert nodes.voltage_source_between('0', '1') == True
    assert nodes.voltage_source_between('3', '4') == True

def test_passive_branches_are_found() -> None:
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
    nodes = SuperNodes(network)
    assert nodes.voltage_source_between('1', '2') == False
    assert nodes.voltage_source_between('2', '3') == False
    assert nodes.voltage_source_between('4', '0') == False

def test_nodes_belonging_to_one_supernode() -> None:
    vs = voltage_source(1)
    r1 = resistor(2)
    r2 = resistor(2)
    network = Network([
        Branch('0', '1', r1),
        Branch('1', '2', vs),
        Branch('2', '0', r2),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='1', reference_node='2') == True

def test_nodes_belonging_to_one_supernode_but_given_in_incorrect_order() -> None:
    vs = voltage_source(1)
    r1 = resistor(2)
    r2 = resistor(2)
    network = Network([
        Branch('0', '1', r1),
        Branch('1', '2', vs),
        Branch('2', '0', r2),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='2', reference_node='1') == False

def test_active_node_belonging_to_supernode_but_reference_node_not() -> None:
    vs = voltage_source(1)
    r1 = resistor(2)
    r2 = resistor(2)
    r3 = resistor(2)
    network = Network([
        Branch('0', '1', r1),
        Branch('1', '2', vs),
        Branch('2', '3', r2),
        Branch('3', '0', r3),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='1', reference_node='3') == False

def test_reference_node_belonging_to_supernode_but_active_node_not() -> None:
    vs = voltage_source(1)
    r1 = resistor(2)
    r2 = resistor(2)
    r3 = resistor(2)
    network = Network([
        Branch('0', '1', r1),
        Branch('1', '2', vs),
        Branch('2', '3', r2),
        Branch('3', '0', r3),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='3', reference_node='2') == False

def test_active_node_and_reference_node_belonging_to_one_supernode_and_reference_node_is_also_active() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    r1 = resistor(2)
    r2 = resistor(2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', vs2),
        Branch('2', '3', r1),
        Branch('3', '0', r2),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='2', reference_node='1') == True

def test_active_node_is_reference_node_of_another_supernode_and_its_active_node() -> None:
    vs1 = voltage_source(1)
    vs2 = voltage_source(2)
    r1 = resistor(2)
    r2 = resistor(2)
    network = Network([
        Branch('0', '1', vs1),
        Branch('1', '2', vs2),
        Branch('2', '3', r1),
        Branch('3', '0', r2),
    ])
    nodes = SuperNodes(network)
    assert nodes.belong_to_same(active_node='1', reference_node='2') == False