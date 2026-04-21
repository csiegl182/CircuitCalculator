from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import current_source, voltage_controlled_voltage_source, voltage_source
from CircuitCalculator.Network.NodalAnalysis.label_mapping import (
    alphabetic_source_mapper,
    alphabetic_voltage_source_mapper,
)

def test_alphabetic_source_mapping_sorts_current_sources_before_voltage_sources() -> None:
    network = Network([
        Branch(node1='0', node2='1', element=voltage_source('A', V=1)),
        Branch(node1='0', node2='1', element=current_source('B', I=1))
    ])
    sorted_sources = alphabetic_source_mapper(network)
    assert sorted_sources['B'] == 0
    assert sorted_sources['A'] == 1

def test_alphabetic_source_mapping_sorts_voltage_sources() -> None:
    labels = ['C', 'D', 'A', 'B']
    network = Network([Branch(node1='0', node2='1', element=voltage_source(l, V=1)) for l in labels])
    label_mapper = alphabetic_source_mapper(network)
    assert label_mapper('A', 'B', 'C', 'D') == tuple(range(4))

def test_alphabetic_source_mapping_sorts_linear_voltage_sources() -> None:
    labels = ['C', 'D', 'A', 'B']
    network = Network([Branch(node1='0', node2='1', element=voltage_source(l, V=1, Z=1)) for l in labels])
    label_mapper = alphabetic_source_mapper(network)
    assert label_mapper('A', 'B', 'C', 'D') == tuple(range(4))

def test_alphabetic_source_mapping_sorts_current_sources() -> None:
    labels = ['C', 'D', 'A', 'B']
    network = Network([Branch(node1='0', node2='1', element=current_source(l, I=1)) for l in labels])
    label_mapper = alphabetic_source_mapper(network)
    assert label_mapper('A', 'B', 'C', 'D') == tuple(range(4))

def test_alphabetic_source_mapping_sorts_linear_current_sources() -> None:
    labels = ['C', 'D', 'A', 'B']
    network = Network([Branch(node1='0', node2='1', element=current_source(l, I=1, Y=1)) for l in labels])
    label_mapper = alphabetic_source_mapper(network)
    assert label_mapper('A', 'B', 'C', 'D') == tuple(range(4))


def test_source_mapping_excludes_controlled_voltage_sources_from_input_sources() -> None:
    network = Network([
        Branch(node1='1', node2='0', element=current_source('Iin', I=1)),
        Branch(node1='2', node2='0', element=voltage_controlled_voltage_source('Econtrol', 2, control_nodes=('1', '0'))),
        Branch(node1='3', node2='0', element=voltage_source('Vout', V=1)),
    ])

    source_mapper = alphabetic_source_mapper(network)
    voltage_source_mapper = alphabetic_voltage_source_mapper(network)

    assert source_mapper.keys == ['Iin', 'Vout']
    assert voltage_source_mapper.keys == ['Econtrol', 'Vout']
