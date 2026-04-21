import numpy as np
import pytest
import sympy as sp
from CircuitCalculator.Network.NodalAnalysis.label_mapping import default_label_mappings_factory
from CircuitCalculator.Network.NodalAnalysis.matrix_operations import NumPyMatrixOperations, SymPyMatrixOperations
from CircuitCalculator.Network.NodalAnalysis.node_analysis_calculations import InvalidControlledSource, node_admittance_matrix
from CircuitCalculator.Network.network import Branch, Network
from CircuitCalculator.Network.elements import conductance, voltage_controlled_current_source
from CircuitCalculator.Network.symbolic_elements import admittance, voltage_controlled_current_source as symbolic_vccs


def test_voltage_controlled_current_source_stamps_node_admittance_matrix() -> None:
    transconductance = 0.5
    network = Network(
        branches=[
            Branch('1', '0', conductance('Gin', 1)),
            Branch('0', '2', voltage_controlled_current_source('Gm', transconductance, control_nodes=('1', '0'))),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0'
    )

    Y = node_admittance_matrix(network, NumPyMatrixOperations(), default_label_mappings_factory(network))

    Y_ref = np.array([
        [1, 0],
        [-transconductance, 1]
    ], dtype=complex)
    np.testing.assert_almost_equal(Y, Y_ref)


def test_symbolic_voltage_controlled_current_source_stamps_node_admittance_matrix() -> None:
    transconductance = sp.Symbol('gm')
    network = Network(
        branches=[
            Branch('1', '0', admittance('Yin', sp.sympify(1))),
            Branch('0', '2', symbolic_vccs('Gm', transconductance, control_nodes=('1', '0'))),
            Branch('2', '0', admittance('Yout', sp.sympify(1))),
        ],
        reference_node_label='0'
    )

    Y = node_admittance_matrix(network, SymPyMatrixOperations(), default_label_mappings_factory(network))

    assert Y == sp.Matrix([
        [1, 0],
        [-transconductance, 1]
    ])


def test_voltage_controlled_current_source_reports_unknown_control_node() -> None:
    network = Network(
        branches=[
            Branch('0', '2', voltage_controlled_current_source('Gm', 1, control_nodes=('missing', '0'))),
            Branch('2', '0', conductance('Gout', 1)),
        ],
        reference_node_label='0'
    )

    with pytest.raises(InvalidControlledSource, match="Control node 'missing' is not connected to the network."):
        node_admittance_matrix(network, NumPyMatrixOperations(), default_label_mappings_factory(network))
