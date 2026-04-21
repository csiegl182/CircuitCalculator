import sympy as sp

import CircuitCalculator.Network.symbolic_elements as elm


def test_symbolic_current_controlled_current_source_is_a_controlled_current_source() -> None:
    source = elm.current_controlled_current_source(
        'F',
        current_gain=sp.Symbol('beta'),
        control_branch='Vs',
    )

    assert source.is_controlled_source
    assert source.is_controlled_current_source
    assert source.is_current_controlled_current_source
    assert not source.is_voltage_controlled_current_source


def test_symbolic_controlled_current_sources_are_not_norten_thevenin_elements() -> None:
    source = elm.current_controlled_current_source(
        'F',
        current_gain=sp.Symbol('beta'),
        control_branch='Vs',
    )

    assert not hasattr(source, 'Z')
    assert not hasattr(source, 'Y')
    assert not hasattr(source, 'V')
    assert not hasattr(source, 'I')


def test_symbolic_voltage_controlled_current_sources_are_not_norten_thevenin_elements() -> None:
    source = elm.voltage_controlled_current_source(
        'Gm',
        G=sp.Symbol('gm'),
        control_nodes=('1', '0'),
    )

    assert not hasattr(source, 'Z')
    assert not hasattr(source, 'Y')
    assert not hasattr(source, 'V')
    assert not hasattr(source, 'I')
