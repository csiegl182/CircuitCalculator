from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import current_source, voltage_source
from CircuitCalculator.Network.transformers import open_circuitify_current_sources

def test_ideal_current_source_is_replaced_by_open_circuit() -> None:
    network = Network(
        branches=[
            Branch('1', '0', current_source('Is1', I=1))
        ]
    )
    network = open_circuitify_current_sources(network)
    assert any([b.element.is_open_circuit for b in network.branches]) == True

def test_linear_current_source_is_replaced_by_conductor() -> None:
    network = Network(
        branches=[
            Branch('1', '0', current_source('Is1', I=1, Y=1))
        ]
    )
    network = open_circuitify_current_sources(network)
    assert any([b.element.is_active for b in network.branches]) == False

def test_open_circuitify_keeps_desired_current_sources() -> None:
    cs1 = current_source('Is1', I=1)
    cs2 = current_source('Is2', I=2)
    network = Network(
        branches=[
            Branch('0', '1', current_source('Is3', I=1)),
            Branch('0', '1', current_source('Is4', I=1)),
            Branch('0', '1', current_source('Is5', I=1)),
            Branch('0', '1', cs1),
            Branch('0', '1', cs2),
            Branch('0', '1', current_source('Is6', I=1))
        ]
    )
    network = open_circuitify_current_sources(network, keep=[cs1])
    assert cs1 in [b.element for b in network.branches]
    assert cs2 not in [b.element for b in network.branches]

def test_linear_voltage_source_is_replaced_by_conductor() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vs1', V=1, Z=1))
        ]
    )
    network = open_circuitify_current_sources(network)
    assert any([b.element.is_active for b in network.branches]) == False

def test_ideal_voltage_source_is_not_touched() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vs1', V=1))
        ]
    )
    network = open_circuitify_current_sources(network)
    assert any([b.element.is_active for b in network.branches]) == True

def test_zero_node_label_is_kept() -> None:
    network = Network(
        branches=[
            Branch('1', '0', current_source('Is1', I=1, Y=1))
        ],
        node_zero_label='1'
    )
    network = open_circuitify_current_sources(network)
    assert network.node_zero_label == '1'