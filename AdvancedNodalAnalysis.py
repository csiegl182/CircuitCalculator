import ClassicNodalAnalysis as cna
import numpy as np
from Network import Network, Branch
from typing import List

class AmbiguousElectricalPotential(Exception): pass

def get_ideal_voltage_sources(network: Network) -> Network:
    return Network([b for b in network.branches if b.element.active and b.element.Z==0 and np.isfinite(b.element.U)])

def get_supernodes(network: Network) -> List[int]:
    voltage_sources = get_ideal_voltage_sources(network)
    node_zero_voltage_sources = voltage_sources.branches_connected_to(node=0)
    supernodes = [b.node1 if b.node1 != 0 else b.node2 for b in node_zero_voltage_sources]
    if len(supernodes) != len(set(supernodes)): raise AmbiguousElectricalPotential
    voltage_sources = Network([vs for vs in voltage_sources.branches if vs not in node_zero_voltage_sources])
    for vs in voltage_sources.branches:
        if vs.node1 in supernodes and vs.node2 in supernodes: raise AmbiguousElectricalPotential
        if vs.node1 not in supernodes:
            supernodes.append(vs.node1)
        else:
            supernodes.append(vs.node2)
    return supernodes

def create_node_matrix_from_network(network: Network) -> np.ndarray:
    Y = cna.create_node_admittance_matrix_from_network(network)
    voltage_source_branches = [b for b in network.branch_list if b.element.active and b.element.Z == 0]
    for vs in voltage_source_branches:
        substituted_node = vs.node1 if vs.node1 != 0 else vs.node2
        n_cols = Y.shape[0]
        Y[:,substituted_node-1] = np.append(-1, np.zeros(n_cols-1))
    return Y

def create_current_vector_from_network(network: Network) -> np.ndarray:
    I = cna.create_current_vector_from_network(network)
    voltage_source_branches = [b for b in network.branch_list if b.element.active and b.element.Z == 0]
    for vs in voltage_source_branches:
        substituted_node = vs.node1 if vs.node1 != 0 else vs.node2
        Y_all = sum([b.element.Y for b in network.branches_connected_to(substituted_node) if np.isfinite(b.element.Y)])
        I[substituted_node-1] = -vs.element.U*Y_all
        I[1] = vs.element.U*network.branches[1].element.Y
    return I

def calculate_node_voltages_from_network(network: Network) -> np.ndarray:
    Y = create_node_matrix_from_network(network)
    I = create_current_vector_from_network(network)
    return cna.calculate_node_voltages(Y, I)

class NodalAnalysisSolution:
    def __init__(self, node_voltages = np.ndarray) -> None:
        self.node_voltages = node_voltages
    
    def get_voltage(self, branch: Branch) -> float:
        return calculate_branch_voltage(self.node_voltages, branch.node1, branch.node2)

    def get_current(self, branch: Branch) -> float:
        return self.get_voltage(branch)/branch.element.Z.real

def nodal_analysis_solver(network):
    return NodalAnalysisSolution(calculate_node_voltages_from_network(network))
    

if __name__ == '__main__':
    from Network import load_network_from_json
    network = load_network_from_json('example_network_2.json')
    print(network)
    Y = create_node_matrix_from_network(network)
    print(Y)
    I = create_current_vector_from_network(network)
    print(I)
    V = calculate_node_voltages_from_network(network)
    print(V)
    vs = get_ideal_voltage_sources(network)
    print(vs)
    print(get_supernodes(network))
