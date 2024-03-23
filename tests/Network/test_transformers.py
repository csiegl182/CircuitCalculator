import pytest
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import voltage_source, current_source, resistor, is_ideal_current_source, is_ideal_voltage_source
from CircuitCalculator.Network.transformers import remove_ideal_current_sources, remove_ideal_voltage_sources, remove_element

def test_remove_ideal_current_sources_removes_all_voltage_sources() -> None:
    network = Network(
        branches=[
            Branch('0', '1', voltage_source('Us1', V=1)),
            Branch('1', '2', resistor('R1', R=1)),
            Branch('2', '3', resistor('R2', R=2)),
            Branch('3', '4', current_source('Is1', I=1)),
            Branch('4', '5', current_source('Is2', I=2)),
            Branch('5', '0', resistor('R3', R=4))
        ]
    )
    network = remove_ideal_current_sources(network)
    assert any([is_ideal_current_source(b.element) for b in network.branches]) == False

def test_remove_ideal_current_sources_keeps_desired_current_sources() -> None:
    cs1 = current_source('Is1', I=1)
    cs2 = current_source('Is2', I=2)
    network = Network(
        branches=[
            Branch('0', '1', voltage_source('Us1', V=1)),
            Branch('1', '2', resistor('R1', R=1)),
            Branch('2', '3', resistor('R2', R=2)),
            Branch('3', '4', cs1),
            Branch('4', '5', cs2),
            Branch('5', '0', resistor('R3', R=4))
        ]
    )
    network = remove_ideal_current_sources(network, keep=[cs1])
    assert cs1 in [b.element for b in network.branches]
    assert cs2 not in [b.element for b in network.branches]

def test_remove_ideal_current_sources_ignores_other_elements_in_keep_elements() -> None:
    cs1 = current_source('Is1', I=1)
    cs2 = current_source('Is2', I=2)
    r1 = resistor('R1', R=1)
    network = Network(
        branches=[
            Branch('0', '1', voltage_source('Us1', V=1)),
            Branch('1', '2', r1),
            Branch('2', '3', resistor('R2', R=2)),
            Branch('3', '4', cs1),
            Branch('4', '5', cs2),
            Branch('5', '0', resistor('R3', R=4))
        ]
    )
    network = remove_ideal_current_sources(network, keep=[cs1, r1])
    assert r1 in [b.element for b in network.branches]
    assert cs1 in [b.element for b in network.branches]
    assert cs2 not in [b.element for b in network.branches]
    
def test_remove_ideal_voltage_sources_removes_all_voltage_sources() -> None:
    network = Network(
        branches=[
            Branch('0', '1', current_source('Is1', I=1)),
            Branch('1', '2', resistor('R1', R=1)),
            Branch('2', '3', resistor('R2', R=2)),
            Branch('3', '4', voltage_source('Us1', V=1)),
            Branch('4', '5', voltage_source('Us2', V=2)),
            Branch('5', '0', resistor('R3', R=4))
        ]
    )
    network = remove_ideal_voltage_sources(network)
    assert any([is_ideal_voltage_source(b.element) for b in network.branches]) == False

def test_remove_ideal_voltage_sources_keeps_desired_voltage_sources() -> None:
    vs1 = voltage_source('Us1', V=1)
    vs2 = voltage_source('Us2', V=2)
    network = Network(
        branches=[
            Branch('0', '1', current_source('Is1', I=1)),
            Branch('1', '2', resistor('R1', R=1)),
            Branch('2', '3', resistor('R2', R=2)),
            Branch('3', '4', vs1),
            Branch('4', '5', vs2),
            Branch('5', '0', resistor('R3', R=4))
        ]
    )
    network = remove_ideal_voltage_sources(network, keep=[vs1])
    assert vs1 in [b.element for b in network.branches]
    assert vs2 not in [b.element for b in network.branches]

def test_remove_ideal_voltage_sources_ignores_other_elements_in_keep_elements() -> None:
    vs1 = voltage_source('Us1', V=1)
    vs2 = voltage_source('Us2', V=2)
    r1 = resistor('R1', R=1)
    network = Network(
        branches=[
            Branch('0', '1', voltage_source('Us3', V=1)),
            Branch('1', '2', r1),
            Branch('2', '3', resistor('R2', R=2)),
            Branch('3', '4', vs1),
            Branch('4', '5', vs2),
            Branch('5', '0', resistor('R3', R=4))
        ]
    )
    network = remove_ideal_voltage_sources(network, keep=[vs1, r1])
    assert r1 in [b.element for b in network.branches]
    assert vs1 in [b.element for b in network.branches]
    assert vs2 not in [b.element for b in network.branches]

def test_remove_ideal_voltage_sources_keeps_passives_connected_to_keep_elements() -> None:
    vs1 = voltage_source('Us1', V=1)
    vs2 = voltage_source('Us2', V=2)
    r1 = resistor('R1', R=1)
    r2 = resistor('R2', R=2)
    network = Network(
        branches=[
            Branch('0', '1', vs1),
            Branch('1', '2', r1),
            Branch('2', '0', r2),
        ]
    )
    network = remove_ideal_voltage_sources(network, keep=[vs1])
    assert r1 in [b.element for b in network.branches_between('1', '2')]

def test_remove_network_element_removes_element() -> None:
    vs1 = voltage_source('Us1', V=1)
    vs2 = voltage_source('Us2', V=2)
    r1 = resistor('R1', R=1)
    r2 = resistor('R2', R=2)
    network = Network(
        branches=[
            Branch('4', '1', vs1),
            Branch('1', '2', vs2),
            Branch('2', '3', r1),
            Branch('3', '4', r2),
        ],
        node_zero_label='4'
    )
    network = remove_element(network, 'Us1')
    with pytest.raises(KeyError):
        network['Us1']


def test_remove_network_element_removes_unknown_element() -> None:
    vs1 = voltage_source('Us1', V=1)
    vs2 = voltage_source('Us2', V=2)
    r1 = resistor('R1', R=1)
    r2 = resistor('R2', R=2)
    network = Network(
        branches=[
            Branch('0', '1', vs1),
            Branch('1', '2', vs2),
            Branch('2', '3', r1),
            Branch('3', '0', r2),
        ]
    )
    with pytest.raises(KeyError):
        remove_element(network, 'Usx')