from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.elements import voltage_source, current_source, resistor, is_ideal_voltage_source
from CircuitCalculator.Network.transformers import remove_ideal_voltage_sources

def test_remove_ideal_voltage_sources_removes_all_voltage_sources() -> None:
    network = Network(
        branches=[
            Branch('0', '1', current_source(I=1)),
            Branch('1', '2', resistor(R=1)),
            Branch('2', '3', resistor(R=2)),
            Branch('3', '4', voltage_source(U=1)),
            Branch('4', '5', voltage_source(U=2)),
            Branch('5', '0', resistor(R=4))
        ]
    )
    network = remove_ideal_voltage_sources(network)
    assert any([is_ideal_voltage_source(b.element) for b in network.branches]) == False

def test_remove_ideal_voltage_sources_keeps_desired_voltage_sources() -> None:
    vs1 = voltage_source(U=1)
    vs2 = voltage_source(U=2)
    network = Network(
        branches=[
            Branch('0', '1', current_source(I=1)),
            Branch('1', '2', resistor(R=1)),
            Branch('2', '3', resistor(R=2)),
            Branch('3', '4', vs1),
            Branch('4', '5', vs2),
            Branch('5', '0', resistor(R=4))
        ]
    )
    network = remove_ideal_voltage_sources(network, keep=[vs1])
    assert vs1 in [b.element for b in network.branches]
    assert vs2 not in [b.element for b in network.branches]

def test_remove_ideal_voltage_sources_ignores_other_elements_in_keep_elements() -> None:
    vs1 = voltage_source(U=1)
    vs2 = voltage_source(U=2)
    r1 = resistor(R=1)
    network = Network(
        branches=[
            Branch('0', '1', voltage_source(U=1)),
            Branch('1', '2', r1),
            Branch('2', '3', resistor(R=2)),
            Branch('3', '4', vs1),
            Branch('4', '5', vs2),
            Branch('5', '0', resistor(R=4))
        ]
    )
    network = remove_ideal_voltage_sources(network, keep=[vs1, r1])
    assert r1 in [b.element for b in network.branches]
    assert vs1 in [b.element for b in network.branches]
    assert vs2 not in [b.element for b in network.branches]

def test_remove_ideal_voltage_sources_keeps_passives_connected_to_keep_elements() -> None:
    vs1 = voltage_source(U=1)
    vs2 = voltage_source(U=2)
    r1 = resistor(R=1)
    r2 = resistor(R=2)
    network = Network(
        branches=[
            Branch('0', '1', vs1),
            Branch('1', '2', r1),
            Branch('2', '0', r2),
        ]
    )
    network = remove_ideal_voltage_sources(network, keep=[vs1])
    assert r1 in [b.element for b in network.branches_between('1', '2')]