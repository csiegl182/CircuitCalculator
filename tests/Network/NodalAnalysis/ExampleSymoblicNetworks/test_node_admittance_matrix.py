from CircuitCalculator.Network.NodalAnalysis.node_analysis import node_admittance_matrix
from CircuitCalculator.Network.matrix_operations import SymPyMatrixOperations
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.symbolic_elements import resistor, voltage_source, current_source
import sympy as sp

def test_node_matrix_from_reference_network_1() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Vq', V=sp.Symbol('Vq'))),
            Branch('1', '0', resistor('R', R=sp.Symbol('R')))
        ]
    )
    Y = node_admittance_matrix(network, matrix_ops=SymPyMatrixOperations())
    Y_ref = sp.Matrix([
        ['1/R']
        ])
    assert Y == Y_ref

def test_node_matrix_from_reference_network_2() -> None:
    network = Network(
        [
            Branch('0', '1', current_source('Iq', I=sp.Symbol('Iq'))),
            Branch('1', '0', resistor('R1', R=sp.Symbol('R')))
        ]
    )
    Y = node_admittance_matrix(network, matrix_ops=SymPyMatrixOperations())
    Y_ref = sp.Matrix([
        ['1/R']
        ])
    assert Y == Y_ref

def test_node_matrix_from_reference_network_3() -> None:
    network = Network(
        [
            Branch('0', '1', current_source('Is', I=sp.Symbol('Iq'), Y=sp.sympify('1/Ri'))),
            Branch('1', '2', resistor('R1', R=sp.Symbol('R1'))),
            Branch('2', '0', resistor('R2', R=sp.Symbol('R2')))
        ]
    )
    Y = node_admittance_matrix(network, matrix_ops=SymPyMatrixOperations())
    Y_ref = sp.Matrix([
        ['1/R1+1/Ri',     '-1/R1'],
        [    '-1/R1', '1/R1+1/R2']
        ])
    assert Y == Y_ref

def test_node_matrix_from_reference_network_4() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Vs', V=sp.Symbol('Vs'))),
            Branch('1', '0', resistor('R1', R=sp.Symbol('R1'))),
            Branch('1', '2', resistor('R2', R=sp.Symbol('R2'))),
            Branch('2', '0', resistor('R3', R=sp.Symbol('R3')))
        ]
    )
    Y = node_admittance_matrix(network, matrix_ops=SymPyMatrixOperations())
    Y_ref = sp.Matrix([
        ['1/R1+1/R2',     '-1/R2'],
        [    '-1/R2', '1/R2+1/R3']
        ])
    assert Y == Y_ref

def test_node_matrix_from_reference_network_5() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Vs1', V=sp.Symbol('Vs1'))),
            Branch('1', '2', resistor('R1', R=sp.Symbol('R1'))),
            Branch('2', '0', resistor('R2', R=sp.Symbol('R2'))),
            Branch('2', '3', resistor('R3', R=sp.Symbol('R3'))),
            Branch('3', '4', resistor('R4', R=sp.Symbol('R4'))),
            Branch('4', '0', resistor('R5', R=sp.Symbol('R5'))),
            Branch('0', '4', voltage_source('Vs2', V=sp.Symbol('Vs2')))
        ]
    )
    Y = node_admittance_matrix(network, matrix_ops=SymPyMatrixOperations())
    Y_ref = sp.Matrix([
        [ '1/R1',          '-1/R1',           0,           0],
        ['-1/R1', '1/R1+1/R2+1/R3',     '-1/R3',           0],
        [      0,          '-1/R3', '1/R3+1/R4',     '-1/R4'],
        [      0,                0,     '-1/R4', '1/R4+1/R5']
        ])
    assert Y == Y_ref

def test_node_matrix_from_reference_network_6() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Vs1', V=sp.Symbol('V1'))),
            Branch('1', '2', resistor('R1', R=sp.Symbol('R1'))),
            Branch('2', '0', resistor('R2', R=sp.Symbol('R2'))),
            Branch('2', '3', resistor('R3', R=sp.Symbol('R3'))),
            Branch('3', '4', resistor('R4', R=sp.Symbol('R4'))),
            Branch('4', '0', resistor('R5', R=sp.Symbol('R5'))),
            Branch('3', '2', voltage_source('Vs2', V=sp.Symbol('V2')))
        ]
    )
    Y = node_admittance_matrix(network, matrix_ops=SymPyMatrixOperations())
    Y_ref = sp.Matrix([
        [ '1/R1',          '-1/R1',           0,           0],
        ['-1/R1', '1/R1+1/R2+1/R3',     '-1/R3',           0],
        [      0,          '-1/R3', '1/R3+1/R4',     '-1/R4'],
        [      0,                0,     '-1/R4', '1/R4+1/R5']
        ])
    assert Y == Y_ref

def test_node_matrix_from_reference_network_7() -> None:
    network = Network(
        [
            Branch('1', '0', resistor('R1', R=sp.Symbol('R1'))),
            Branch('2', '1', voltage_source('Vs2', V=sp.Symbol('V2'))),
            Branch('1', '3', resistor('R2', R=sp.Symbol('R2'))),
            Branch('4', '3', voltage_source('Vs3', V=sp.Symbol('V3'))),
            Branch('0', '5', voltage_source('Vs1', V=sp.Symbol('V1'))),
            Branch('2', '5', resistor('R3', R=sp.Symbol('R3'))),
            Branch('4', '5', resistor('R4', R=sp.Symbol('R4'))),
            Branch('3', '5', current_source('Is4', I=sp.Symbol('I4')))
        ]
    )
    Y = node_admittance_matrix(network, matrix_ops=SymPyMatrixOperations())
    Y_ref = sp.Matrix([
        ['1/R1+1/R2',       0, '-1/R2',       0,           0],
        [          0,  '1/R3',       0,       0,     '-1/R3'],
        [    '-1/R2',       0,  '1/R2',       0,           0],
        [          0,       0,       0,  '1/R4',     '-1/R4'],
        [          0, '-1/R3',       0, '-1/R4', '1/R3+1/R4']
        ])
    assert Y == Y_ref

def test_node_matrix_from_reference_network_10() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Vs1', V=sp.Symbol('V1'))),
            Branch('1', '0', resistor('R1', R=sp.Symbol('R1'))),
            Branch('2', '1', voltage_source('Vs2', V=sp.Symbol('V2'))),
            Branch('2', '1', resistor('R2', R=sp.Symbol('R2'))),
            Branch('0', '4', resistor('R3', R=sp.Symbol('R3'))),
            Branch('4', '3', current_source('Is3', I=sp.Symbol('I3'))),
            Branch('3', '2', resistor('R4', R=sp.Symbol('R4'))),
            Branch('2', '4', resistor('R5', R=sp.Symbol('R5'))),
        ]
    )
    Y = node_admittance_matrix(network, matrix_ops=SymPyMatrixOperations())
    Y_ref = sp.Matrix([
        ['1/R1+1/R2',          '-1/R2',       0,           0],
        [    '-1/R2', '1/R2+1/R4+1/R5', '-1/R4',     '-1/R5'],
        [          0,          '-1/R4',  '1/R4',           0],
        [          0,          '-1/R5',       0, '1/R3+1/R5']
        ])
    assert Y == Y_ref

def test_node_matrix_from_reference_network_11() -> None:
    network = Network(
        branches=[
            Branch('0', '1', current_source('Is', I=sp.Symbol('I'))),
            Branch('1', '0', resistor('R1', R=sp.Symbol('R1'))),
            Branch('2', '1', resistor('R2', R=sp.Symbol('R2'))),
            Branch('2', '0', resistor('R3', R=sp.Symbol('R3'))),
            Branch('3', '2', voltage_source('Vs', V=sp.Symbol('V'))),
            Branch('3', '0', resistor('R4', R=sp.Symbol('R4')))
        ],
        node_zero_label='0'
    )
    Y = node_admittance_matrix(network, matrix_ops=SymPyMatrixOperations())
    Y_ref = sp.Matrix([
        ['1/R1+1/R2',     '-1/R2',      0],
        [    '-1/R2', '1/R2+1/R3',      0],
        [          0,           0, '1/R4']
        ])
    assert Y == Y_ref

def test_node_matrix_from_reference_network_13() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('V', V=sp.Symbol('V'))),
            Branch('1', '2', resistor('R1', R=sp.Symbol('R1'))),
            Branch('1', '2', resistor('R2', R=sp.Symbol('R2'))),
            Branch('2', '0', resistor('R3', R=sp.Symbol('R3')))
        ],
        node_zero_label='0'
    )
    Y = node_admittance_matrix(network, matrix_ops=SymPyMatrixOperations())
    Y_ref = sp.Matrix([
        [ '1/R1+1/R2',     '-1/R1-1/R2'],
        ['-1/R1-1/R2', '1/R1+1/R2+1/R3']
        ])
    assert Y == Y_ref