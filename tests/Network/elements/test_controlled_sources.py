import CircuitCalculator.Network.elements as elm


def test_voltage_controlled_current_source_is_a_controlled_current_source() -> None:
    source = elm.voltage_controlled_current_source('Gm', G=2, control_nodes=('1', '0'))

    assert source.is_controlled_source
    assert source.is_controlled_current_source
    assert not source.is_controlled_voltage_source
    assert source.is_voltage_controlled_current_source
    assert not source.is_current_controlled_current_source


def test_current_controlled_current_source_is_a_controlled_current_source() -> None:
    source = elm.current_controlled_current_source('F', current_gain=2, control_branch='Vs')

    assert source.is_controlled_source
    assert source.is_controlled_current_source
    assert not source.is_controlled_voltage_source
    assert not source.is_voltage_controlled_current_source
    assert source.is_current_controlled_current_source
    assert not source.is_voltage_controlled_voltage_source
    assert not source.is_current_controlled_voltage_source


def test_voltage_controlled_voltage_source_is_a_controlled_voltage_source() -> None:
    source = elm.voltage_controlled_voltage_source('E', voltage_gain=2, control_nodes=('1', '0'))

    assert source.is_controlled_source
    assert not source.is_controlled_current_source
    assert source.is_controlled_voltage_source
    assert not source.is_voltage_controlled_current_source
    assert not source.is_current_controlled_current_source
    assert source.is_voltage_controlled_voltage_source
    assert not source.is_current_controlled_voltage_source


def test_current_controlled_voltage_source_is_a_controlled_voltage_source() -> None:
    source = elm.current_controlled_voltage_source('H', transresistance=2, control_branch='Rcontrol')

    assert source.is_controlled_source
    assert not source.is_controlled_current_source
    assert source.is_controlled_voltage_source
    assert not source.is_voltage_controlled_current_source
    assert not source.is_current_controlled_current_source
    assert not source.is_voltage_controlled_voltage_source
    assert source.is_current_controlled_voltage_source


def test_controlled_current_sources_are_not_independent_sources() -> None:
    source = elm.current_controlled_current_source('F', current_gain=2, control_branch='Vs')

    assert not source.is_voltage_source
    assert not source.is_current_source
    assert not source.is_ideal_voltage_source
    assert not source.is_ideal_current_source


def test_controlled_voltage_sources_are_not_independent_sources() -> None:
    source = elm.current_controlled_voltage_source('H', transresistance=2, control_branch='Rcontrol')

    assert not source.is_voltage_source
    assert not source.is_current_source
    assert not source.is_ideal_voltage_source
    assert not source.is_ideal_current_source


def test_controlled_current_sources_are_not_norten_thevenin_elements() -> None:
    source = elm.current_controlled_current_source('F', current_gain=2, control_branch='Vs')

    assert not hasattr(source, 'Z')
    assert not hasattr(source, 'Y')
    assert not hasattr(source, 'V')
    assert not hasattr(source, 'I')


def test_voltage_controlled_current_sources_are_not_norten_thevenin_elements() -> None:
    source = elm.voltage_controlled_current_source('Gm', G=2, control_nodes=('1', '0'))

    assert not hasattr(source, 'Z')
    assert not hasattr(source, 'Y')
    assert not hasattr(source, 'V')
    assert not hasattr(source, 'I')


def test_controlled_voltage_sources_are_not_norten_thevenin_elements() -> None:
    source = elm.voltage_controlled_voltage_source('E', voltage_gain=2, control_nodes=('1', '0'))

    assert not hasattr(source, 'Z')
    assert not hasattr(source, 'Y')
    assert not hasattr(source, 'V')
    assert not hasattr(source, 'I')


def test_controlled_current_source_with_zero_factor_is_open_circuit() -> None:
    source = elm.current_controlled_current_source('F', current_gain=0, control_branch='Vs')

    assert not source.is_active
    assert source.is_open_circuit
    assert not source.is_short_circuit


def test_controlled_voltage_source_with_zero_factor_is_short_circuit() -> None:
    source = elm.current_controlled_voltage_source('H', transresistance=0, control_branch='Rcontrol')

    assert not source.is_active
    assert not source.is_open_circuit
    assert source.is_short_circuit
