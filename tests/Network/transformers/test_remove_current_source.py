from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import voltage_source, current_source, resistor
from CircuitCalculator.Network.transformers import remove_ideal_current_sources

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
    assert any([b.element.is_ideal_current_source for b in network.branches]) == False

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