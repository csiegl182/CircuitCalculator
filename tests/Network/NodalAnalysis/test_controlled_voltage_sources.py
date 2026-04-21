import numpy as np
import pytest
import sympy as sp

from CircuitCalculator.Network.NodalAnalysis.label_mapping import default_label_mappings_factory
from CircuitCalculator.Network.NodalAnalysis.matrix_operations import NumPyMatrixOperations, SymPyMatrixOperations
from CircuitCalculator.Network.NodalAnalysis.node_analysis_calculations import (
    InvalidControlledSource,
    nodal_analysis_coefficient_matrix,
)
from CircuitCalculator.Network.NodalAnalysis.solution import numeric_nodal_analysis_bias_point_solution
from CircuitCalculator.Network.elements import (
    admittance,
    conductance,
    current_controlled_voltage_source,
    current_source,
    impedance,
    resistor,
    voltage_controlled_current_source,
    voltage_controlled_voltage_source,
    voltage_source,
)
from CircuitCalculator.Network.network import Branch, Network
from CircuitCalculator.Network.symbolic_elements import (
    admittance as symbolic_admittance,
    voltage_controlled_voltage_source as symbolic_vcvs,
    voltage_source as symbolic_voltage_source,
)


def test_voltage_controlled_voltage_source_is_solved_from_control_voltage() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vctrl', 2)),
            Branch('2', '0', voltage_controlled_voltage_source('Eout', 3, control_nodes=('1', '0'))),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    solution = numeric_nodal_analysis_bias_point_solution(network)

    np.testing.assert_almost_equal(solution.get_voltage('Eout'), 6)
    np.testing.assert_almost_equal(solution.get_current('Eout'), -6)


def test_voltage_controlled_voltage_source_stamps_lower_mna_equation() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vctrl', 2)),
            Branch('2', '0', voltage_controlled_voltage_source('Eout', 3, control_nodes=('1', '0'))),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    A = nodal_analysis_coefficient_matrix(
        network,
        NumPyMatrixOperations(),
        default_label_mappings_factory(network),
    )

    A_ref = np.array([
        [0, 0, 0, 1],
        [0, 1, 1, 0],
        [-3, 1, 0, 0],
        [1, 0, 0, 0],
    ], dtype=complex)
    np.testing.assert_almost_equal(A, A_ref)


def test_current_controlled_voltage_source_is_solved_from_resistor_control_current() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vctrl', 1)),
            Branch('1', '0', resistor('Rcontrol', 1)),
            Branch('2', '0', current_controlled_voltage_source('Hout', 3, control_branch='Rcontrol')),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    solution = numeric_nodal_analysis_bias_point_solution(network)

    np.testing.assert_almost_equal(solution.get_current('Rcontrol'), 1)
    np.testing.assert_almost_equal(solution.get_voltage('Hout'), 3)
    np.testing.assert_almost_equal(solution.get_current('Hout'), -3)


def test_current_controlled_voltage_source_can_be_controlled_by_controlled_voltage_source_current() -> None:
    transresistance = 3
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vin', 1)),
            Branch('2', '0', voltage_controlled_voltage_source('Econtrol', 2, control_nodes=('1', '0'))),
            Branch('2', '0', conductance('Gcontrol_load', 1)),
            Branch('3', '0', current_controlled_voltage_source('Hout', transresistance, control_branch='Econtrol')),
            Branch('3', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    solution = numeric_nodal_analysis_bias_point_solution(network)

    np.testing.assert_almost_equal(solution.get_current('Econtrol'), -2)
    np.testing.assert_almost_equal(solution.get_voltage('Hout'), -transresistance*2)


@pytest.mark.parametrize(
    "control_branch_id, branches",
    [
        (
            'Rcontrol',
            [
                Branch('1', '0', voltage_source('Vin', 1)),
                Branch('1', '0', resistor('Rcontrol', 1)),
            ],
        ),
        (
            'Gcontrol',
            [
                Branch('1', '0', voltage_source('Vin', 1)),
                Branch('1', '0', conductance('Gcontrol', 1)),
            ],
        ),
        (
            'Zcontrol',
            [
                Branch('1', '0', voltage_source('Vin', 1)),
                Branch('1', '0', impedance('Zcontrol', 1)),
            ],
        ),
        (
            'Ycontrol',
            [
                Branch('1', '0', voltage_source('Vin', 1)),
                Branch('1', '0', admittance('Ycontrol', 1)),
            ],
        ),
        (
            'Vcontrol',
            [
                Branch('1', '0', voltage_source('Vcontrol', 1)),
                Branch('1', '0', conductance('Gin', 1)),
            ],
        ),
        (
            'Icontrol',
            [
                Branch('1', '0', current_source('Icontrol', 1)),
                Branch('1', '0', conductance('Gin', 1)),
            ],
        ),
        (
            'IVcontrol',
            [
                Branch('1', '0', voltage_source('Vin', 1)),
                Branch('1', '0', current_source('IVcontrol', 1, Y=1)),
            ],
        ),
        (
            'VVcontrol',
            [
                Branch('1', '0', voltage_source('Vin', 1)),
                Branch('1', '0', voltage_source('VVcontrol', 0, Z=1)),
            ],
        ),
    ],
)
def test_current_controlled_voltage_source_accepts_norten_thevenin_control_branch(
    control_branch_id: str,
    branches: list[Branch],
) -> None:
    transresistance = 3
    network = Network(
        branches=[
            *branches,
            Branch('2', '0', current_controlled_voltage_source('Hout', transresistance, control_branch=control_branch_id)),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    solution = numeric_nodal_analysis_bias_point_solution(network)

    np.testing.assert_almost_equal(
        solution.get_voltage('Hout'),
        transresistance*solution.get_current(control_branch_id),
    )


def test_current_controlled_voltage_source_requires_norten_thevenin_control_branch() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vin', 1)),
            Branch('1', '0', voltage_controlled_current_source('Gcontrol', 1, control_nodes=('1', '0'))),
            Branch('2', '0', current_controlled_voltage_source('Hout', 3, control_branch='Gcontrol')),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    with pytest.raises(InvalidControlledSource):
        nodal_analysis_coefficient_matrix(
            network,
            NumPyMatrixOperations(),
            default_label_mappings_factory(network),
        )


def test_symbolic_voltage_controlled_voltage_source_stamps_mna_matrix() -> None:
    voltage_gain = sp.Symbol('mu')
    network = Network(
        branches=[
            Branch('1', '0', symbolic_voltage_source('Vctrl', sp.sympify(1))),
            Branch('2', '0', symbolic_vcvs('Eout', voltage_gain, control_nodes=('1', '0'))),
            Branch('2', '0', symbolic_admittance('Yout', sp.sympify(1))),
        ],
        reference_node_label='0',
    )

    A = nodal_analysis_coefficient_matrix(
        network,
        SymPyMatrixOperations(),
        default_label_mappings_factory(network),
    )

    assert A == sp.Matrix([
        [0, 0, 0, 1],
        [0, 1, 1, 0],
        [-voltage_gain, 1, 0, 0],
        [1, 0, 0, 0],
    ])
