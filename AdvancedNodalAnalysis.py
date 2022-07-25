import ClassicNodalAnalysis as cna
import numpy as np
from Network import Network, Branch, voltage_source
from typing import List, Dict

class AmbiguousElectricalPotential(Exception): pass

def get_ideal_voltage_sources(network: Network) -> Network:
    return Network([b for b in network.branches if b.element.active and b.element.Z==0 and np.isfinite(b.element.U)])

def get_supernodes(network: Network) -> Dict[int, Branch]:
    voltage_sources = get_ideal_voltage_sources(network)
    node_zero_voltage_sources = voltage_sources.branches_connected_to(node=0)
    voltage_source_nodes = [tuple(sorted([b.node1, b.node2])) for b in node_zero_voltage_sources]
    if len(voltage_source_nodes) != len(set(voltage_source_nodes)):
        raise AmbiguousElectricalPotential
    supernodes = {b.node1 if b.node1 != 0 else b.node2 : b for b in node_zero_voltage_sources}
    voltage_sources = Network([vs for vs in voltage_sources.branches if vs not in node_zero_voltage_sources])
    for vs in voltage_sources.branches:
        if vs.node1 in supernodes.keys() and vs.node2 in supernodes.keys():
            raise AmbiguousElectricalPotential
        if vs.node1 not in supernodes.keys():
            supernodes.update({vs.node1: vs})
        else:
            supernodes.update({vs.node2: vs})
    return supernodes

def create_node_matrix_from_network(network: Network) -> np.ndarray:
    Y = cna.create_node_admittance_matrix_from_network(network)
    for sn, b in get_supernodes(network).items():
        Y[:,sn-1] = 0
        if b.node1 > 0:
            Y[b.node1-1, sn-1] = -1
        if b.node2 > 0:
            Y[b.node2-1, sn-1] = +1
    return Y

def create_current_vector_from_network(network: Network) -> np.ndarray:
    I = cna.create_current_vector_from_network(network)
    voltage_sources = get_ideal_voltage_sources(network)
    for sn in get_supernodes(network):
        I[sn-1] = 0
        for vs in voltage_sources.branches_connected_to(sn):
            Y_all = sum([b.element.Y for b in network.branches_connected_to(sn) if np.isfinite(b.element.Y)])
            I[sn-1] += vs.element.U*Y_all
    I[1] = vs.element.U*network.branches[1].element.Y
    return I

class NodalAnalysisSolution:
    def __init__(self, network : Network) -> None:
        Y = create_node_matrix_from_network(network)
        I = create_current_vector_from_network(network)
        self.solution_vector = cna.calculate_node_voltages(Y, I)
        self.super_nodes = get_supernodes(network)
        self.super_node_voltages = 0###
        self.node_potentials = self.solution_vector
        for i in self.super_nodes:
            self.node_potentials[i-1] = 0
    
    def get_voltage(self, branch: Branch) -> float:
        return 0

    def get_current(self, branch: Branch) -> float:
        return self.get_voltage(branch)/branch.element.Z.real

def nodal_analysis_solver(network):
    return NodalAnalysisSolution(network)
    

if __name__ == '__main__':
    from Network import load_network_from_json
    network = load_network_from_json('example_network_2.json')
    print(network)
    Y = create_node_matrix_from_network(network)
    print(Y)
    I = create_current_vector_from_network(network)
    print(I)
    # V = calculate_node_voltages_from_network(network)
    # print(V)
