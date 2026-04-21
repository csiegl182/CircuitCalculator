import numpy as np
import pytest
import CircuitCalculator.Circuit.Components.components as ccp
from CircuitCalculator.Circuit.circuit import Circuit, transform
from CircuitCalculator.Circuit.solution import dc_solution


def test_voltage_controlled_current_source_component_can_be_created() -> None:
    component = ccp.voltage_controlled_current_source(id='Gm', G=0.5, nodes=('0', '2'), control_nodes=('1', '0'))

    assert component.type == 'voltage_controlled_current_source'
    assert component.id == 'Gm'
    assert component.nodes == ('0', '2')
    assert component.value['G'] == 0.5
    assert component.value['control_nodes'] == ('1', '0')


def test_voltage_controlled_current_source_component_requires_two_output_nodes() -> None:
    with pytest.raises(ValueError):
        ccp.voltage_controlled_current_source(id='Gm', G=0.5, nodes=('0', '2', '3'), control_nodes=('1', '0'))  # type: ignore[arg-type]


def test_voltage_controlled_current_source_component_requires_two_control_nodes() -> None:
    with pytest.raises(ValueError):
        ccp.voltage_controlled_current_source(id='Gm', G=0.5, nodes=('0', '2'), control_nodes=('1', '0', '3'))  # type: ignore[arg-type]


def test_voltage_controlled_current_source_component_is_transformed_to_network_element() -> None:
    circuit = Circuit([
        ccp.dc_voltage_source(id='Vctrl', V=2, nodes=('1', '0')),
        ccp.voltage_controlled_current_source(id='Gm', G=0.5, nodes=('0', '2'), control_nodes=('1', '0')),
        ccp.resistor(id='R', R=1, nodes=('2', '0')),
    ], ground_node='0')

    network = transform(circuit)[0]

    assert network['Gm'].node1 == '0'
    assert network['Gm'].node2 == '2'
    assert network['Gm'].element.is_voltage_controlled_current_source
    assert not network['Gm'].element.is_current_source
    assert network['Gm'].element.control_node1 == '1'
    assert network['Gm'].element.control_node2 == '0'
    assert network['Gm'].element.transconductance == 0.5


def test_voltage_controlled_current_source_is_solved_from_control_voltage() -> None:
    circuit = Circuit(
        components=[
            ccp.dc_voltage_source(id='Vctrl', V=2, nodes=('1', '0')),
            ccp.voltage_controlled_current_source(id='Gm', G=0.5, nodes=('0', '2'), control_nodes=('1', '0')),
            ccp.resistor(id='R', R=1, nodes=('2', '0')),
        ],
        ground_node='0'
    )

    solution = dc_solution(circuit)

    np.testing.assert_almost_equal(solution.get_potential('1'), 2)
    np.testing.assert_almost_equal(solution.get_potential('2'), 1)
    np.testing.assert_almost_equal(solution.get_current('Gm'), 1)
    np.testing.assert_almost_equal(solution.get_voltage('R'), 1)
    np.testing.assert_almost_equal(solution.get_current('R'), 1)
