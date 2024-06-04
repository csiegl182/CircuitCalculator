import numpy as np
from .circuit import Circuit, transform_circuit
from ..Network.NodalAnalysis import node_analysis as ntw_imp

def open_circuit_impedance(circuit: Circuit, node1: str, node2: str, w: np.ndarray = np.array([0])) -> np.ndarray:
    return np.array([ntw_imp.open_circuit_impedance(transform_circuit(circuit, w0), node1, node2) for w0 in w])

def element_impedance(circuit: Circuit, element_id: str, w: np.ndarray = np.array([0])) -> np.ndarray:
    return np.array([ntw_imp.element_impedance(transform_circuit(circuit, w0), element_id) for w0 in w])

def open_circuit_dc_resistance(circuit: Circuit, node1: str, node2: str) -> float:
    return open_circuit_impedance(circuit, node1, node2, w=np.array([0]))[0].real

def element_dc_resistance(circuit: Circuit, element_id: str) -> float:
    return element_impedance(circuit, element_id, w=np.array([0]))[0].real
