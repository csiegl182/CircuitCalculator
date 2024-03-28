from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import voltage_source, current_source, is_short_circuit, is_active
from CircuitCalculator.Network.transformers import short_circuitify_voltage_sources

def test_ideal_voltage_source_is_replaced_by_short_circuit() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vs1', V=1))
        ]
    )
    network = short_circuitify_voltage_sources(network)
    assert any([is_short_circuit(b.element) for b in network.branches]) == True

def test_linear_voltage_source_is_replaced_by_resistor() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vs1', V=1, Z=1))
        ]
    )
    network = short_circuitify_voltage_sources(network)
    assert any([is_active(b.element) for b in network.branches]) == False

def test_short_circuitify_keeps_desired_voltage_sources() -> None:
    vs1 = voltage_source('Vs1', V=1)
    vs2 = voltage_source('Vs2', V=2)
    network = Network(
        branches=[
            Branch('0', '1', voltage_source('Vs3', V=1)),
            Branch('0', '1', voltage_source('Vs4', V=1)),
            Branch('0', '1', voltage_source('Vs5', V=1)),
            Branch('0', '1', vs1),
            Branch('0', '1', vs2),
            Branch('0', '1', voltage_source('Vs6', V=1))
        ]
    )
    network = short_circuitify_voltage_sources(network, keep=[vs1])
    assert vs1 in [b.element for b in network.branches]
    assert vs2 not in [b.element for b in network.branches]

def test_linear_current_source_is_replaced_by_resistor() -> None:
    network = Network(
        branches=[
            Branch('1', '0', current_source('Is1', I=1, Y=1))
        ]
    )
    network = short_circuitify_voltage_sources(network)
    assert any([is_active(b.element) for b in network.branches]) == False

def test_ideal_current_source_is_not_touched() -> None:
    network = Network(
        branches=[
            Branch('1', '0', current_source('Is1', I=1))
        ]
    )
    network = short_circuitify_voltage_sources(network)
    assert any([is_active(b.element) for b in network.branches]) == True

def test_zero_node_label_is_kept() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vs1', V=1, Z=1))
        ],
        node_zero_label='1'
    )
    network = short_circuitify_voltage_sources(network)
    assert network.node_zero_label == '1'