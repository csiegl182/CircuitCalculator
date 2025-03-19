from CircuitCalculator.Network.NodalAnalysis.node_analysis import voltage_source_incidence_matrix, SymPyMatrixOperations
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.symbolic_elements import resistor, voltage_source, current_source
import sympy as sp

def test_voltage_source_incidence_matrix_from_reference_network_1() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Vs', V='Vs')),
            Branch('1', '0', resistor('R', R='R'))
        ]
    )
    A = voltage_source_incidence_matrix(network, matrix_ops=SymPyMatrixOperations())
    A_ref = sp.Matrix([
        [1]
        ])
    assert A == A_ref

def test_voltage_source_incidence_matrix_from_reference_network_2() -> None:
    network = Network(
        [
            Branch('0', '1', current_source('Iq', I='Iq')),
            Branch('1', '0', resistor('R1', R='R'))
        ]
    )
    A = voltage_source_incidence_matrix(network, matrix_ops=SymPyMatrixOperations())
    A_ref = sp.Matrix([]).reshape(1, 0)
    assert A == A_ref

def test_voltage_source_incidence_matrix_from_reference_network_3() -> None:
    network = Network(
        [
            Branch('0', '1', current_source('Is', I='Iq', Y='1/Ri')),
            Branch('1', '2', resistor('R1', R='R1')),
            Branch('2', '0', resistor('R2', R='R2'))
        ]
    )
    A = voltage_source_incidence_matrix(network, matrix_ops=SymPyMatrixOperations())
    A_ref = sp.Matrix([
        [],
        []
        ]).reshape(2,0)
    assert A == A_ref

def test_voltage_source_incidence_matrix_from_reference_network_4() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Uq', V='Uq')),
            Branch('1', '0', resistor('R1', R='R1')),
            Branch('1', '2', resistor('R2', R='R2')),
            Branch('2', '0', resistor('R3', R='R3'))
        ]
    )
    A = voltage_source_incidence_matrix(network, matrix_ops=SymPyMatrixOperations())
    A_ref = sp.Matrix([
        [1],
        [0]
        ])
    assert A == A_ref

def test_voltage_source_incidence_matrix_from_reference_network_5() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Vs1', V='Vs1')),
            Branch('1', '2', resistor('R1', R='R1')),
            Branch('2', '0', resistor('R2', R='R2')),
            Branch('2', '3', resistor('R3', R='R3')),
            Branch('3', '4', resistor('R4', R='R4')),
            Branch('4', '0', resistor('R5', R='R5')),
            Branch('0', '4', voltage_source('Vs2', V='Vs2'))
        ]
    )
    A = voltage_source_incidence_matrix(network, matrix_ops=SymPyMatrixOperations())
    A_ref = sp.Matrix([
        [1,  0],
        [0,  0],
        [0,  0],
        [0, -1]
        ])
    assert A == A_ref

def test_voltage_source_incidence_matrix_from_reference_network_6() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Uq1', V='V1')),
            Branch('1', '2', resistor('R1', R='R1')),
            Branch('2', '0', resistor('R2', R='R2')),
            Branch('2', '3', resistor('R3', R='R3')),
            Branch('3', '4', resistor('R4', R='R4')),
            Branch('4', '0', resistor('R5', R='R5')),
            Branch('3', '2', voltage_source('Uq2', V='V2'))
        ]
    )
    A = voltage_source_incidence_matrix(network, matrix_ops=SymPyMatrixOperations())
    A_ref = sp.Matrix([
        [1,  0],
        [0, -1],
        [0,  1],
        [0,  0]
        ])
    assert A == A_ref

def test_voltage_source_incidence_matrix_from_reference_network_7() -> None:
    network = Network(
        [
            Branch('1', '0', resistor('R1', R='R1')),
            Branch('2', '1', voltage_source('Vs2', V='V2')),
            Branch('1', '3', resistor('R2', R='R2')),
            Branch('4', '3', voltage_source('Vs3', V='V3')),
            Branch('0', '5', voltage_source('Us1', V='U1')),
            Branch('2', '5', resistor('R3', R='R3')),
            Branch('4', '5', resistor('R4', R='R4')),
            Branch('3', '5', current_source('Is4', I='I4'))
        ]
    )
    A = voltage_source_incidence_matrix(network, matrix_ops=SymPyMatrixOperations())
    A_ref = sp.Matrix([
        [ 0, -1,  0],
        [ 0,  1,  0],
        [ 0,  0, -1],
        [ 0,  0,  1],
        [-1,  0,  0]
        ])
    assert A == A_ref

def test_voltage_source_incidence_matrix_from_reference_network_10() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Us1', V='V1')),
            Branch('1', '0', resistor('R1', R='R1')),
            Branch('2', '1', voltage_source('Us2', V='V2')),
            Branch('2', '1', resistor('R2', R='R2')),
            Branch('0', '4', resistor('R3', R='R3')),
            Branch('4', '3', current_source('Is3', I='I3')),
            Branch('3', '2', resistor('R4', R='R4')),
            Branch('2', '4', resistor('R5', R='R5')),
        ]
    )
    A = voltage_source_incidence_matrix(network, matrix_ops=SymPyMatrixOperations())
    A_ref = sp.Matrix([
        [1, -1],
        [0,  1],
        [0,  0],
        [0,  0]
        ])
    assert A == A_ref

def test_voltage_source_incidence_matrix_from_reference_network_11() -> None:
    network = Network(
        branches=[
            Branch('0', '1', current_source('Is', I='I')),
            Branch('1', '0', resistor('R1', R='R1')),
            Branch('2', '1', resistor('R2', R='R2')),
            Branch('2', '0', resistor('R3', R='R3')),
            Branch('3', '2', voltage_source('Us', V='V')),
            Branch('3', '0', resistor('R4', R='R4'))
        ],
        node_zero_label='0'
    )
    A = voltage_source_incidence_matrix(network, matrix_ops=SymPyMatrixOperations())
    A_ref = sp.Matrix([
        [ 0],
        [-1],
        [ 1]
        ])
    assert A == A_ref

def test_voltage_source_incidence_matrix_from_reference_network_13() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('V', V='V')),
            Branch('1', '2', resistor('R1', R='R1')),
            Branch('1', '2', resistor('R2', R='R2')),
            Branch('2', '0', resistor('R3', R='R3'))
        ],
        node_zero_label='0'
    )
    A = voltage_source_incidence_matrix(network, matrix_ops=SymPyMatrixOperations())
    A_ref = sp.Matrix([
        [1],
        [0]
        ])
    assert A == A_ref
