import numpy as np
import pytest
import sympy as sp

from CircuitCalculator.Network.NodalAnalysis.label_mapping import default_label_mappings_factory
from CircuitCalculator.Network.NodalAnalysis.matrix_operations import NumPyMatrixOperations, SymPyMatrixOperations
from CircuitCalculator.Network.NodalAnalysis.node_analysis_calculations import (
    current_controlled_current_source_admittance_matrix,
    current_controlled_current_source_incidence_matrix,
    InvalidControlledSource,
    nodal_analysis_coefficient_matrix,
)
from CircuitCalculator.Network.NodalAnalysis.solution import numeric_nodal_analysis_bias_point_solution
from CircuitCalculator.Network.elements import (
    admittance as numeric_admittance,
    conductance,
    current_controlled_current_source,
    current_source,
    impedance,
    resistor,
    voltage_controlled_current_source,
    voltage_source,
)
from CircuitCalculator.Network.network import Branch, Network
from CircuitCalculator.Network.symbolic_elements import (
    admittance,
    current_controlled_current_source as symbolic_cccs,
    voltage_source as symbolic_voltage_source,
)


def test_current_controlled_current_source_stamps_voltage_source_current_block() -> None:
    current_gain = 2
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vs', 1)),
            Branch('1', '0', conductance('Gin', 1)),
            Branch('0', '2', current_controlled_current_source('F', current_gain, control_branch='Vs')),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    B = current_controlled_current_source_incidence_matrix(
        network,
        NumPyMatrixOperations(),
        default_label_mappings_factory(network),
    )

    B_ref = np.array([
        [0],
        [-current_gain],
    ], dtype=complex)
    np.testing.assert_almost_equal(B, B_ref)


def test_current_controlled_current_source_only_changes_top_right_mna_block() -> None:
    current_gain = 2
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vs', 1)),
            Branch('1', '0', conductance('Gin', 1)),
            Branch('0', '2', current_controlled_current_source('F', current_gain, control_branch='Vs')),
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
        [1, 0, 1],
        [0, 1, -current_gain],
        [1, 0, 0],
    ], dtype=complex)
    np.testing.assert_almost_equal(A, A_ref)


def test_current_controlled_current_source_solution_current_follows_control_branch_current() -> None:
    current_gain = 2
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vs', 1)),
            Branch('1', '0', conductance('Gin', 1)),
            Branch('0', '2', current_controlled_current_source('F', current_gain, control_branch='Vs')),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    solution = numeric_nodal_analysis_bias_point_solution(network)

    np.testing.assert_almost_equal(solution.get_current('Vs'), -1)
    np.testing.assert_almost_equal(solution.get_current('F'), -current_gain)
    np.testing.assert_almost_equal(solution.get_potential('2'), -current_gain)


def test_current_controlled_current_source_can_be_controlled_by_conductance_branch() -> None:
    current_gain = 2
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vs', 1)),
            Branch('1', '0', conductance('Gcontrol', 1)),
            Branch('0', '2', current_controlled_current_source('F', current_gain, control_branch='Gcontrol')),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    solution = numeric_nodal_analysis_bias_point_solution(network)

    np.testing.assert_almost_equal(solution.get_current('Gcontrol'), 1)
    np.testing.assert_almost_equal(solution.get_current('F'), current_gain)
    np.testing.assert_almost_equal(solution.get_potential('2'), current_gain)


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
                Branch('1', '0', numeric_admittance('Ycontrol', 1)),
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
def test_current_controlled_current_source_accepts_norten_thevenin_control_branch(
    control_branch_id: str,
    branches: list[Branch],
) -> None:
    current_gain = 2
    network = Network(
        branches=[
            *branches,
            Branch('0', '2', current_controlled_current_source('F', current_gain, control_branch=control_branch_id)),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    solution = numeric_nodal_analysis_bias_point_solution(network)

    np.testing.assert_almost_equal(
        solution.get_current('F'),
        current_gain*solution.get_current(control_branch_id),
    )


def test_current_controlled_current_source_stamps_control_branch_admittance() -> None:
    current_gain = 2
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vs', 1)),
            Branch('1', '0', conductance('Gcontrol', 1)),
            Branch('0', '2', current_controlled_current_source('F', current_gain, control_branch='Gcontrol')),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    Y = current_controlled_current_source_admittance_matrix(
        network,
        NumPyMatrixOperations(),
        default_label_mappings_factory(network),
    )

    Y_ref = np.array([
        [0, 0],
        [-current_gain, 0],
    ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref)


def test_symbolic_current_controlled_current_source_stamps_mna_matrix() -> None:
    current_gain = sp.Symbol('beta')
    network = Network(
        branches=[
            Branch('1', '0', symbolic_voltage_source('Vs', sp.sympify(1))),
            Branch('1', '0', admittance('Yin', sp.sympify(1))),
            Branch('0', '2', symbolic_cccs('F', current_gain, control_branch='Vs')),
            Branch('2', '0', admittance('Yout', sp.sympify(1))),
        ],
        reference_node_label='0',
    )

    A = nodal_analysis_coefficient_matrix(
        network,
        SymPyMatrixOperations(),
        default_label_mappings_factory(network),
    )

    assert A == sp.Matrix([
        [1, 0, 1],
        [0, 1, -current_gain],
        [1, 0, 0],
    ])


def test_symbolic_current_controlled_current_source_can_be_controlled_by_admittance_branch() -> None:
    current_gain = sp.Symbol('beta')
    network = Network(
        branches=[
            Branch('1', '0', symbolic_voltage_source('Vs', sp.sympify(1))),
            Branch('1', '0', admittance('Yin', sp.sympify('Yin'))),
            Branch('0', '2', symbolic_cccs('F', current_gain, control_branch='Yin')),
            Branch('2', '0', admittance('Yout', sp.sympify(1))),
        ],
        reference_node_label='0',
    )

    A = nodal_analysis_coefficient_matrix(
        network,
        SymPyMatrixOperations(),
        default_label_mappings_factory(network),
    )

    assert A == sp.Matrix([
        [sp.sympify('Yin'), 0, 1],
        [-current_gain*sp.sympify('Yin'), 1, 0],
        [1, 0, 0],
    ])


def test_current_controlled_current_source_requires_existing_control_branch() -> None:
    network = Network(
        branches=[
            Branch('1', '0', conductance('Gcontrol', 1)),
            Branch('0', '2', current_controlled_current_source('F', 2, control_branch='Missing')),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0',
    )

    with pytest.raises(InvalidControlledSource):
        current_controlled_current_source_incidence_matrix(
            network,
            NumPyMatrixOperations(),
            default_label_mappings_factory(network),
        )


def test_current_controlled_current_source_requires_norten_thevenin_control_branch() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('Vin', 1)),
            Branch('1', '0', voltage_controlled_current_source('Gcontrol', 1, control_nodes=('1', '0'))),
            Branch('0', '2', current_controlled_current_source('F', 2, control_branch='Gcontrol')),
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
