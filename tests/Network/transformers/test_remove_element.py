import pytest
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import voltage_source, resistor
from CircuitCalculator.Network.transformers import remove_element

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
        reference_node_label='4'
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

def test_remove_element_keeps_zero_node_label() -> None:
    r1 = resistor('R1', R=1)
    r2 = resistor('R2', R=2)
    network = Network(
        branches=[
            Branch('2', '1', r1),
            Branch('1', '0', r2)
        ]
    )
    new_network = remove_element(network, 'R2')
    assert new_network.reference_node_label == '0'
    assert new_network['R1'].node1 == '2'
    assert new_network['R1'].node2 == '0'
    