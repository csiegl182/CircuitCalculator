import numpy as np
import pytest
import CircuitCalculator.Circuit.Components.components as ccp
from CircuitCalculator.Circuit.circuit import Circuit, transform
from CircuitCalculator.Circuit.solution import dc_solution


def test_voltage_controlled_voltage_source_component_can_be_created() -> None:
    component = ccp.voltage_controlled_voltage_source(
        id='Eout',
        voltage_gain=3,
        nodes=('2', '0'),
        control_nodes=('1', '0')
    )

    assert component.type == 'voltage_controlled_voltage_source'
    assert component.id == 'Eout'
    assert component.nodes == ('2', '0')
    assert component.value['voltage_gain'] == 3
    assert component.value['control_nodes'] == ('1', '0')


def test_voltage_controlled_voltage_source_component_requires_two_output_nodes() -> None:
    with pytest.raises(ValueError):
        ccp.voltage_controlled_voltage_source(id='Eout', voltage_gain=3, nodes=('2', '0', '3'), control_nodes=('1', '0'))  # type: ignore[arg-type]


def test_voltage_controlled_voltage_source_component_requires_two_control_nodes() -> None:
    with pytest.raises(ValueError):
        ccp.voltage_controlled_voltage_source(id='Eout', voltage_gain=3, nodes=('2', '0'), control_nodes=('1', '0', '3'))  # type: ignore[arg-type]


def test_current_controlled_voltage_source_component_can_be_created() -> None:
    component = ccp.current_controlled_voltage_source(
        id='Hout',
        transresistance=3,
        nodes=('2', '0'),
        control_branch='Rcontrol'
    )

    assert component.type == 'current_controlled_voltage_source'
    assert component.id == 'Hout'
    assert component.nodes == ('2', '0')
    assert component.value['transresistance'] == 3
    assert component.value['control_branch'] == 'Rcontrol'


def test_current_controlled_voltage_source_component_requires_two_output_nodes() -> None:
    with pytest.raises(ValueError):
        ccp.current_controlled_voltage_source(id='Hout', transresistance=3, nodes=('2', '0', '3'), control_branch='Rcontrol')  # type: ignore[arg-type]


def test_current_controlled_voltage_source_component_requires_control_branch() -> None:
    with pytest.raises(ValueError):
        ccp.current_controlled_voltage_source(id='Hout', transresistance=3, nodes=('2', '0'), control_branch='')


def test_voltage_controlled_voltage_source_component_is_transformed_to_network_element() -> None:
    circuit = Circuit([
        ccp.dc_voltage_source(id='Vctrl', V=2, nodes=('1', '0')),
        ccp.voltage_controlled_voltage_source(id='Eout', voltage_gain=3, nodes=('2', '0'), control_nodes=('1', '0')),
        ccp.resistor(id='Rout', R=1, nodes=('2', '0')),
    ], ground_node='0')

    network = transform(circuit)[0]

    assert network['Eout'].node1 == '2'
    assert network['Eout'].node2 == '0'
    assert network['Eout'].element.is_voltage_controlled_voltage_source
    assert not network['Eout'].element.is_voltage_source
    assert network['Eout'].element.control_node1 == '1'
    assert network['Eout'].element.control_node2 == '0'
    assert network['Eout'].element.voltage_gain == 3


def test_current_controlled_voltage_source_component_is_transformed_to_network_element() -> None:
    circuit = Circuit([
        ccp.dc_voltage_source(id='Vctrl', V=1, nodes=('1', '0')),
        ccp.resistor(id='Rcontrol', R=1, nodes=('1', '0')),
        ccp.current_controlled_voltage_source(id='Hout', transresistance=3, nodes=('2', '0'), control_branch='Rcontrol'),
        ccp.resistor(id='Rout', R=1, nodes=('2', '0')),
    ], ground_node='0')

    network = transform(circuit)[0]

    assert network['Hout'].node1 == '2'
    assert network['Hout'].node2 == '0'
    assert network['Hout'].element.is_current_controlled_voltage_source
    assert not network['Hout'].element.is_voltage_source
    assert network['Hout'].element.control_branch == 'Rcontrol'
    assert network['Hout'].element.transresistance == 3


def test_voltage_controlled_voltage_source_is_solved_from_control_voltage() -> None:
    circuit = Circuit(
        components=[
            ccp.dc_voltage_source(id='Vctrl', V=2, nodes=('1', '0')),
            ccp.voltage_controlled_voltage_source(id='Eout', voltage_gain=3, nodes=('2', '0'), control_nodes=('1', '0')),
            ccp.resistor(id='Rout', R=1, nodes=('2', '0')),
        ],
        ground_node='0'
    )

    solution = dc_solution(circuit)

    np.testing.assert_almost_equal(solution.get_voltage('Eout'), 6)
    np.testing.assert_almost_equal(solution.get_current('Eout'), -6)
    np.testing.assert_almost_equal(solution.get_voltage('Rout'), 6)


def test_current_controlled_voltage_source_is_solved_from_control_current() -> None:
    circuit = Circuit(
        components=[
            ccp.dc_voltage_source(id='Vctrl', V=1, nodes=('1', '0')),
            ccp.resistor(id='Rcontrol', R=1, nodes=('1', '0')),
            ccp.current_controlled_voltage_source(id='Hout', transresistance=3, nodes=('2', '0'), control_branch='Rcontrol'),
            ccp.resistor(id='Rout', R=1, nodes=('2', '0')),
        ],
        ground_node='0'
    )

    solution = dc_solution(circuit)

    np.testing.assert_almost_equal(solution.get_current('Rcontrol'), 1)
    np.testing.assert_almost_equal(solution.get_voltage('Hout'), 3)
    np.testing.assert_almost_equal(solution.get_current('Hout'), -3)
    np.testing.assert_almost_equal(solution.get_voltage('Rout'), 3)
