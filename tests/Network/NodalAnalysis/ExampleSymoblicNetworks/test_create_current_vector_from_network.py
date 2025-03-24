from CircuitCalculator.Network.NodalAnalysis.node_analysis import current_source_incidence_vector, SymPyMatrixOperations
from CircuitCalculator.Network.network import Network, Branch
from CircuitCalculator.Network.symbolic_elements import resistor, voltage_source, current_source
import sympy as sp

def test_create_current_vector_from_reference_network_1() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Vq', V=sp.Symbol('Vq'))),
            Branch('1', '0', resistor('R1', R=sp.Symbol('R')))
        ]
    )
    I = current_source_incidence_vector(network, matrix_ops=SymPyMatrixOperations())
    I_ref = sp.Matrix([0])
    assert I == I_ref

def test_create_current_vector_from_reference_network_2() -> None:
    network = Network(
        [
            Branch('0', '1', current_source('Iq', I=sp.Symbol('Iq'))),
            Branch('1', '0', resistor('R1', R=sp.Symbol('R')))
        ]
    )
    I = current_source_incidence_vector(network, matrix_ops=SymPyMatrixOperations())
    I_ref = sp.Matrix(['1.0*Iq'])
    assert sp.simplify(I) == I_ref

def test_create_current_vector_from_reference_network_3() -> None:
    network = Network(
        [
            Branch('0', '1', current_source('Iq1', I=sp.Symbol('Iq'), Y=sp.Symbol('1/Ri'))),
            Branch('1', '2', resistor('R1', R=sp.Symbol('R1'))),
            Branch('2', '0', resistor('R2', R=sp.Symbol('R2')))
        ]
    )
    I = current_source_incidence_vector(network, matrix_ops=SymPyMatrixOperations())
    I_ref = sp.Matrix([['1.0*Iq'],
                       ['0']])
    assert I == I_ref

def test_create_current_vector_from_reference_network_4() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Uq', V=sp.Symbol('Uq'))),
            Branch('1', '0', resistor('R1', R=sp.Symbol('R1'))),
            Branch('1', '2', resistor('R2', R=sp.Symbol('R2'))),
            Branch('2', '0', resistor('R3', R=sp.Symbol('R3')))
        ]
    )
    I = current_source_incidence_vector(network, matrix_ops=SymPyMatrixOperations())
    I_ref = sp.Matrix([[0], [0]])
    assert I == I_ref

def test_create_current_vector_from_reference_network_5() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Vs1', V=sp.Symbol('U1'))),
            Branch('1', '2', resistor('R1', R=sp.Symbol('R1'))),
            Branch('3', '4', resistor('R4', R=sp.Symbol('R4'))),
            Branch('4', '0', resistor('R5', R=sp.Symbol('R5'))),
            Branch('0', '4', voltage_source('Vs2', V=sp.Symbol('V2')))
        ]
    )
    I = current_source_incidence_vector(network, matrix_ops=SymPyMatrixOperations())
    I_ref = sp.Matrix([[0], [0], [0], [0]])
    assert I == I_ref

def test_create_current_vector_from_reference_network_6() -> None:
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
    I = current_source_incidence_vector(network, matrix_ops=SymPyMatrixOperations())
    I_ref = sp.Matrix([[0], [0], [0], [0]])
    assert I == I_ref

def test_create_current_vector_from_reference_network_7() -> None:
    network = Network(
        [
            Branch('0', '1', resistor('R1', R=sp.Symbol('R1'))),
            Branch('2', '1', voltage_source('Vs2', V=sp.Symbol('V2'))),
            Branch('1', '3', resistor('R2', R=sp.Symbol('R2'))),
            Branch('4', '3', voltage_source('Vs3', V=sp.Symbol('V3'))),
            Branch('2', '5', resistor('R3', R=sp.Symbol('R3'))),
            Branch('4', '5', resistor('R4', R=sp.Symbol('R4'))),
            Branch('3', '5', current_source('Is4', I=sp.Symbol('I4'))),
            Branch('0', '5', voltage_source('Vs1', V=sp.Symbol('V1')))
        ]
    )
    I = current_source_incidence_vector(network, matrix_ops=SymPyMatrixOperations())
    I_ref = sp.Matrix([[0], [0], ['-1.0*I4'], [0], ['1.0*I4']])
    assert I == I_ref

def test_create_current_vector_from_reference_network_10() -> None:
    network = Network(
        [
            Branch('1', '0', voltage_source('Vs1', V=sp.Symbol('V1'))),
            Branch('1', '0', resistor('R1', R=sp.Symbol('R1'))),
            Branch('2', '1', voltage_source('Vs2', V=sp.Symbol('V2'))),
            Branch('2', '1', resistor('R2', R=sp.Symbol('R2'))),
            Branch('0', '4', resistor('R3', R=sp.Symbol('R3'))),
            Branch('4', '3', current_source('Is4', I=sp.Symbol('I4'))),
            Branch('3', '2', resistor('R4', R=sp.Symbol('R4'))),
            Branch('2', '4', resistor('R5', R=sp.Symbol('R5'))),
        ]
    )
    I = current_source_incidence_vector(network, matrix_ops=SymPyMatrixOperations())
    I_ref = sp.Matrix([[0], [0], ['1.0*I4'], ['-1.0*I4']])
    assert I == I_ref

def test_create_current_vector_from_reference_network_13() -> None:
    network = Network(
        branches=[
            Branch('1', '0', voltage_source('V', V=sp.Symbol('V'))),
            Branch('1', '2', resistor('R1', R=sp.Symbol('R1'))),
            Branch('1', '2', resistor('R2', R=sp.Symbol('R2'))),
            Branch('2', '0', resistor('R3', R=sp.Symbol('R3')))
        ],
        node_zero_label='0'
    )
    I = current_source_incidence_vector(network, matrix_ops=SymPyMatrixOperations())
    I_ref = sp.Matrix([[0], [0]], dtype=complex)
    assert I == I_ref