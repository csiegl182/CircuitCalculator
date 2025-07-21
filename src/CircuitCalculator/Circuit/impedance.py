import numpy as np
import sympy as sp
from .circuit import Circuit, transform_circuit, transform_symbolic_circuit
from ..Network.NodalAnalysis import node_analysis as na
from ..Network.NodalAnalysis import matrix_operations as mo

def open_circuit_impedance(circuit: Circuit, node1: str, node2: str, w: np.ndarray = np.array([0])) -> np.ndarray:
    return np.array([na.open_circuit_impedance(transform_circuit(circuit, w0), node1, node2) for w0 in w])

def element_impedance(circuit: Circuit, element_id: str, w: np.ndarray = np.array([0])) -> np.ndarray:
    return np.array([na.element_impedance(transform_circuit(circuit, w0), element_id) for w0 in w])

def open_circuit_dc_resistance(circuit: Circuit, node1: str, node2: str) -> float:
    return open_circuit_impedance(circuit, node1, node2, w=np.array([0]))[0].real

def element_dc_resistance(circuit: Circuit, element_id: str) -> float:
    return element_impedance(circuit, element_id, w=np.array([0]))[0].real

def symbolic_open_circuit_impedance(circuit: Circuit, node1: str, node2: str, s: sp.Symbol = sp.Symbol('s', complex=True)) -> mo.symbolic:
    return na.open_circuit_impedance(transform_symbolic_circuit(circuit, s=s), node1, node2, matrix_ops = mo.SymPyMatrixOperations())

def symbolic_element_impedance(circuit: Circuit, element_id: str, s: sp.Symbol = sp.Symbol('s', complex=True)) -> mo.symbolic:
    return na.element_impedance(transform_symbolic_circuit(circuit, s=s), element_id, matrix_ops = mo.SymPyMatrixOperations())

def symbolic_open_circuit_dc_resistance(circuit: Circuit, node1: str, node2: str) -> mo.symbolic:
    return symbolic_open_circuit_impedance(circuit, node1, node2, s=sp.sympify(0))

def symbolic_element_dc_resistance(circuit: Circuit, element_id: str) -> mo.symbolic:
    return symbolic_element_impedance(circuit, element_id, s=sp.sympify(0))