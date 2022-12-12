from CircuitCalculator.Network import Network, Branch, voltage_source, current_source, resistor, remove_ideal_current_sources, is_ideal_current_source

def test_remove_ideal_current_sources_removes_all_voltage_sources() -> None:
    network = Network(
        branches=[
            Branch('0', '1', voltage_source(U=1)),
            Branch('1', '2', resistor(R=1)),
            Branch('2', '3', resistor(R=2)),
            Branch('3', '4', current_source(I=1)),
            Branch('4', '5', current_source(I=2)),
            Branch('5', '0', resistor(R=4))
        ]
    )
    network = remove_ideal_current_sources(network)
    assert any([is_ideal_current_source(b.element) for b in network.branches]) == False

def test_remove_ideal_current_sources_keeps_desired_current_sources() -> None:
    cs1 = current_source(I=1)
    cs2 = current_source(I=2)
    network = Network(
        branches=[
            Branch('0', '1', voltage_source(U=1)),
            Branch('1', '2', resistor(R=1)),
            Branch('2', '3', resistor(R=2)),
            Branch('3', '4', cs1),
            Branch('4', '5', cs2),
            Branch('5', '0', resistor(R=4))
        ]
    )
    network = remove_ideal_current_sources(network, keep=[cs1])
    assert cs1 in [b.element for b in network.branches]
    assert cs2 not in [b.element for b in network.branches]

def test_remove_ideal_current_sources_ignores_other_elements_in_keep_elements() -> None:
    cs1 = current_source(I=1)
    cs2 = current_source(I=2)
    r1 = resistor(R=1)
    network = Network(
        branches=[
            Branch('0', '1', voltage_source(U=1)),
            Branch('1', '2', r1),
            Branch('2', '3', resistor(R=2)),
            Branch('3', '4', cs1),
            Branch('4', '5', cs2),
            Branch('5', '0', resistor(R=4))
        ]
    )
    network = remove_ideal_current_sources(network, keep=[cs1, r1])
    assert r1 in [b.element for b in network.branches]
    assert cs1 in [b.element for b in network.branches]
    assert cs2 not in [b.element for b in network.branches]
    