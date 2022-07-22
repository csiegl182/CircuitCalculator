import ClassicNodalAnalysis as cna
import numpy as np
from Network import Network

def create_node_matrix_from_network(network: Network) -> np.ndarray:
    Y = cna.create_node_admittance_matrix_from_network(network)
    voltage_source_branches = [b for b in network.branch_list if b.element.active and b.element.Z == 0]
    for vs in voltage_source_branches:
        substituted_node = vs.node1 if vs.node1 != 0 else vs.node2
        n_cols = Y.shape[0]
        Y[:,substituted_node-1] = np.append(1, np.zeros(n_cols-1))
    return Y

def create_current_vector_from_network(network: Network) -> np.ndarray:
    I = cna.create_current_vector_from_network(network)
    return I

def nodal_analysis_solver(network):
    return cna.NodalAnalysisSolution(cna.calculate_node_voltages_from_network(network))
    

if __name__ == '__main__':
    from Network import load_network_from_json
    network = load_network_from_json('example_network_2.json')
    print(network)
    Y = create_node_matrix_from_network(network)
    print(Y)
    I = create_current_vector_from_network(network)
    print(I)
