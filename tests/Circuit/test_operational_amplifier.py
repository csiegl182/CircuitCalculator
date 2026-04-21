import numpy as np
import pytest

import CircuitCalculator.Circuit.Components.components as ccp
from CircuitCalculator.Circuit.circuit import Circuit, transform
from CircuitCalculator.Circuit.solution import dc_solution


def test_operational_amplifier_component_can_be_created_with_default_gain() -> None:
    component = ccp.operational_amplifier(
        id='U1',
        nodes=('out', '0'),
        input_nodes=('plus', 'minus')
    )

    assert component.type == 'operational_amplifier'
    assert component.id == 'U1'
    assert component.nodes == ('out', '0')
    assert component.value['gain'] == 100_000
    assert component.value['input_nodes'] == ('plus', 'minus')


def test_operational_amplifier_component_can_override_gain() -> None:
    component = ccp.operational_amplifier(
        id='U1',
        gain=10_000,
        nodes=('out', '0'),
        input_nodes=('plus', 'minus')
    )

    assert component.value['gain'] == 10_000


def test_operational_amplifier_component_requires_two_output_nodes() -> None:
    with pytest.raises(ValueError):
        ccp.operational_amplifier(id='U1', nodes=('out', '0', 'x'), input_nodes=('plus', 'minus'))  # type: ignore[arg-type]


def test_operational_amplifier_component_requires_two_input_nodes() -> None:
    with pytest.raises(ValueError):
        ccp.operational_amplifier(id='U1', nodes=('out', '0'), input_nodes=('plus', 'minus', 'x'))  # type: ignore[arg-type]


def test_operational_amplifier_is_transformed_to_voltage_controlled_voltage_source() -> None:
    circuit = Circuit(
        components=[
            ccp.operational_amplifier(id='U1', gain=50_000, nodes=('out', '0'), input_nodes=('plus', 'minus')),
            ccp.resistor(id='Rload', R=1_000, nodes=('out', '0')),
        ],
        ground_node='0'
    )

    network = transform(circuit)[0]

    assert network['U1'].node1 == 'out'
    assert network['U1'].node2 == '0'
    assert network['U1'].element.is_voltage_controlled_voltage_source
    assert network['U1'].element.voltage_gain == 50_000
    assert network['U1'].element.control_node1 == 'plus'
    assert network['U1'].element.control_node2 == 'minus'


def test_non_inverting_operational_amplifier_uses_finite_gain() -> None:
    gain = 100_000
    feedback_ratio = 1 / 10
    expected_output_voltage = gain / (1 + gain*feedback_ratio)
    circuit = Circuit(
        components=[
            ccp.dc_voltage_source(id='Vin', V=1, nodes=('plus', '0')),
            ccp.operational_amplifier(id='U1', nodes=('out', '0'), input_nodes=('plus', 'minus')),
            ccp.resistor(id='Rf', R=9_000, nodes=('out', 'minus')),
            ccp.resistor(id='Rg', R=1_000, nodes=('minus', '0')),
            ccp.resistor(id='Rload', R=10_000, nodes=('out', '0')),
        ],
        ground_node='0'
    )

    solution = dc_solution(circuit)

    np.testing.assert_allclose(solution.get_voltage('U1'), expected_output_voltage, rtol=1e-10, atol=1e-10)
    np.testing.assert_allclose(solution.get_potential('minus'), expected_output_voltage*feedback_ratio, rtol=1e-10, atol=1e-10)
    np.testing.assert_allclose(
        solution.get_potential('plus') - solution.get_potential('minus'),
        expected_output_voltage/gain,
        rtol=1e-10,
        atol=1e-10,
    )
