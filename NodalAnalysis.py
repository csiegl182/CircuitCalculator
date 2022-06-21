from anyio import DelimiterNotFound
import numpy as np

class DimensionError(Exception): pass

def calculate_node_voltages(Y : np.ndarray, I : np.ndarray) -> np.ndarray:
    if Y.ndim != 2:
        raise DimensionError('dim error')
    if I.ndim != 1:
        raise DimensionError('dim error')
    m, n = Y.shape
    if n != m:
        raise DimensionError('dim error')
    return np.linalg.solve(Y, I)

def create_node_admittance_matrix(zero_node_admittances, *node_admittances) ->  np.ndarray:
    [len(y_vec) for y_vec in node_admittances]
    if len(zero_node_admittances) != len(node_admittances)+1:
        raise DimensionError('dim error')
        
    Y = np.diag(zero_node_admittances)
    for n, admittances in enumerate(node_admittances):
        Y[n,n] += np.sum(admittances)
        for m, y in enumerate(admittances):
            Y[n+m+1,n+m+1] += y
            Y[n+m+1, n] = -y
    Y += np.tril(Y,-1).T

    return Y

def calculate_branch_voltage(V_node : np.ndarray, node1 : int, node2 : int) -> float:
    if node1 < 0 or node2 < 0:
        raise DimensionError('dim error')
    try:
        V1 = 0 if node1 == 0 else V_node[node1-1]
        V2 = 0 if node2 == 0 else V_node[node2-1]
    except IndexError:
        raise DimensionError('dim error')

    return V1 - V2
        