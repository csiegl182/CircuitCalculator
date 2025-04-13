import numpy as np
from .circuit import Circuit, transform_circuit, transform_symbolic_circuit
from ..Network.NodalAnalysis import node_analysis as na
from ..Network import matrix_operations as mo

def open_circuit_impedance(circuit: Circuit, node1: str, node2: str, w: np.ndarray = np.array([0])) -> np.ndarray:
    return np.array([na.open_circuit_impedance(transform_circuit(circuit, w0), node1, node2) for w0 in w])

def element_impedance(circuit: Circuit, element_id: str, w: np.ndarray = np.array([0])) -> np.ndarray:
    return np.array([na.element_impedance(transform_circuit(circuit, w0), element_id) for w0 in w])

def open_circuit_dc_resistance(circuit: Circuit, node1: str, node2: str) -> float:
    return open_circuit_impedance(circuit, node1, node2, w=np.array([0]))[0].real

def element_dc_resistance(circuit: Circuit, element_id: str) -> float:
    return element_impedance(circuit, element_id, w=np.array([0]))[0].real

def symbolic_open_circuit_impedance(circuit: Circuit, node1: str, node2: str) -> mo.symbolic:
    return na.open_circuit_impedance(transform_symbolic_circuit(circuit), node1, node2, matrix_ops = mo.SymPyMatrixOperations())

def symbolic_element_impedance(circuit: Circuit, element_id: str) -> mo.symbolic:
    return na.element_impedance(transform_symbolic_circuit(circuit), element_id, matrix_ops = mo.SymPyMatrixOperations())