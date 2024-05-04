from ..network import Network
from . import labelmapper as map
from .node_analysis import create_node_matrix_from_network, create_source_incidence_matrix_from_network
import numpy as np
from typing import TypedDict
import itertools

class BranchValues(TypedDict):
    value: float
    node1: str
    node2: str

def create_element_incidence_matrix(values: list[BranchValues], node_mapping: dict[str, int]) -> np.ndarray:
    Delta = np.zeros((len(values), len(node_mapping)))
    for (k, value), (i_label, i) in itertools.product(enumerate(values), node_mapping.items()):
        if i_label == value['node1']:
            Delta[k][i] = +1
        if i_label == value['node2']:
            Delta[k][i] = -1
    return Delta

def create_state_space_input_update_matrix(network: Network, Cvalues: list[BranchValues], node_index_mapper: map.NodeIndexMapper = map.default) -> tuple[np.ndarray, np.ndarray]:
    node_mapping = node_index_mapper(network)
    Y = create_node_matrix_from_network(network=network, node_index_mapper=node_index_mapper).real
    Q = create_source_incidence_matrix_from_network(network=network, node_index_mapper=node_index_mapper).real
    Delta = create_element_incidence_matrix(Cvalues, node_mapping)
    Delta = np.matrix(Delta)
    invC = np.array([-1/float(C['value']) for C in Cvalues])
    A = np.linalg.inv(Delta*np.linalg.inv(Y)*Delta.T)*np.diag(invC)
    B = -A*Delta*np.linalg.inv(Y)*Q
    return A, B