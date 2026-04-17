import numpy as np
import pytest
import CircuitCalculator.Circuit.Components.components as ccp
from CircuitCalculator.Circuit.circuit import Circuit, transform
from CircuitCalculator.Circuit.solution import dc_solution


def test_current_controlled_current_source_component_can_be_created() -> None:
    component = ccp.current_controlled_current_source(
        id='Fout',
        current_gain=2,
        nodes=('2', '0'),
        control_branch='Vctrl'
    )

    assert component.type == 'current_controlled_current_source'
    assert component.id == 'Fout'
    assert component.nodes == ('2', '0')
    assert component.value['current_gain'] == 2
    assert component.value['control_branch'] == 'Vctrl'


def test_current_controlled_current_source_component_requires_two_output_nodes() -> None:
    with pytest.raises(ValueError):
        ccp.current_controlled_current_source(id='Fout', current_gain=2, nodes=('0', '2', '3'), control_branch='Vctrl')  # type: ignore[arg-type]


def test_current_controlled_current_source_component_requires_control_branch() -> None:
    with pytest.raises(ValueError):
        ccp.current_controlled_current_source(id='Fout', current_gain=2, nodes=('2', '0'), control_branch='')


def test_current_controlled_current_source_component_is_transformed_to_network_element() -> None:
    circuit = Circuit([
        ccp.dc_voltage_source(id='Vctrl', V=1, nodes=('1', '0')),
        ccp.resistor(id='R1', R=1, nodes=('1', '0')),
        ccp.current_controlled_current_source(id='Fout', current_gain=2, nodes=('2', '0'), control_branch='Vctrl'),
        ccp.resistor(id='R2', R=1, nodes=('2', '0')),
    ], ground_node='0')

    network = transform(circuit)[0]

    assert network['Fout'].node1 == '2'
    assert network['Fout'].node2 == '0'
    assert network['Fout'].element.is_current_controlled_current_source
    assert not network['Fout'].element.is_current_source
    assert network['Fout'].element.control_branch == 'Vctrl'
    assert network['Fout'].element.current_gain == 2


def test_current_controlled_current_source_is_solved_from_control_current() -> None:
    circuit = Circuit(
        components=[
            ccp.dc_voltage_source(id='Vctrl', V=1, nodes=('1', '0')),
            ccp.resistor(id='R1', R=1, nodes=('1', '0')),
            ccp.current_controlled_current_source(id='Fout', current_gain=2, nodes=('2', '0'), control_branch='Vctrl'),
            ccp.resistor(id='R2', R=1, nodes=('2', '0')),
        ],
        ground_node='0'
    )

    solution = dc_solution(circuit)

    np.testing.assert_almost_equal(solution.get_potential('1'), 1)
    np.testing.assert_almost_equal(solution.get_potential('2'), 2)
    np.testing.assert_almost_equal(solution.get_current('Vctrl'), -1)
    np.testing.assert_almost_equal(solution.get_current('Fout'), -2)
    np.testing.assert_almost_equal(solution.get_voltage('R1'), 1)
    np.testing.assert_almost_equal(solution.get_voltage('R2'), 2)


def test_current_controlled_current_source_can_be_controlled_by_resistor_branch() -> None:
    circuit = Circuit(
        components=[
            ccp.dc_voltage_source(id='Vctrl', V=1, nodes=('1', '0')),
            ccp.resistor(id='R1', R=1, nodes=('1', '0')),
            ccp.current_controlled_current_source(id='Fout', current_gain=2, nodes=('0', '2'), control_branch='R1'),
            ccp.resistor(id='R2', R=1, nodes=('2', '0')),
        ],
        ground_node='0'
    )

    solution = dc_solution(circuit)

    np.testing.assert_almost_equal(solution.get_current('R1'), 1)
    np.testing.assert_almost_equal(solution.get_current('Fout'), 2)
    np.testing.assert_almost_equal(solution.get_voltage('R2'), 2)
