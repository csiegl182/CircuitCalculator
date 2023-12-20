from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import voltage_source, current_source
from CircuitCalculator.Network.NodalAnalysis.labelmapper import alphabetic_source_mapper

def test_alphabetic_source_mapping_sorts_current_sources_before_voltage_sources() -> None:
    network = Network([
        Branch(node1='0', node2='1', element=voltage_source('A', V=1)),
        Branch(node1='0', node2='1', element=current_source('B', I=1))
    ])
    sorted_sources = alphabetic_source_mapper(network)
    assert sorted_sources.index('B') < sorted_sources.index('A')

def test_alphabetic_source_mapping_sorts_voltage_sources() -> None:
    labels = ['C', 'D', 'A', 'B']
    network = Network([Branch(node1='0', node2='1', element=voltage_source(l, V=1)) for l in labels])
    assert alphabetic_source_mapper(network) == sorted(labels)

def test_alphabetic_source_mapping_sorts_linear_voltage_sources() -> None:
    labels = ['C', 'D', 'A', 'B']
    network = Network([Branch(node1='0', node2='1', element=voltage_source(l, V=1, Z=1)) for l in labels])
    assert alphabetic_source_mapper(network) == sorted(labels)

def test_alphabetic_source_mapping_sorts_current_sources() -> None:
    labels = ['C', 'D', 'A', 'B']
    network = Network([Branch(node1='0', node2='1', element=current_source(l, I=1)) for l in labels])
    assert alphabetic_source_mapper(network) == sorted(labels)

def test_alphabetic_source_mapping_sorts_linear_current_sources() -> None:
    labels = ['C', 'D', 'A', 'B']
    network = Network([Branch(node1='0', node2='1', element=current_source(l, I=1, Y=1)) for l in labels])
    assert alphabetic_source_mapper(network) == sorted(labels)