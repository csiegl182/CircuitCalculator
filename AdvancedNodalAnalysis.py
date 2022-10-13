import ClassicNodalAnalysis as cna
import numpy as np
from Network import Network, Branch, Element, NetworkSolution
from typing import Dict

class AmbiguousElectricalPotential(Exception): pass

def is_ideal_voltage_source(element: Element) -> bool:
    return element.active and element.Z==0 and np.isfinite(element.U)

def get_ideal_voltage_sources(network: Network) -> Network:
    return Network([b for b in network.branches if is_ideal_voltage_source(b.element)])

def remove_ideal_voltage_sources(network: Network) -> Network:
    return Network([b for b in network.branches if not is_ideal_voltage_source(b.element)])

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

def get_supernode_counterparts(network: Network) -> Dict[int, Branch]:
    counterparts = {b.node2 if b.node1 == sn else b.node1 : b for sn, b in get_supernodes(network).items()}
    counterparts.pop(0, None)
    return counterparts

def create_node_matrix_from_network(network: Network) -> np.ndarray:
    Y = cna.create_node_admittance_matrix_from_network(remove_ideal_voltage_sources(network))
    for cp, b in get_supernode_counterparts(network).items():
        if b.node1 == cp:
            Y[:,cp-1] += Y[:,b.node2-1]
        else:
            Y[:,cp-1] += Y[:,b.node1-1]
    for sn, b in get_supernodes(network).items():
        Y[:,sn-1] = 0
        if b.node1 > 0:
            Y[b.node1-1, sn-1] = -1
        if b.node2 > 0:
            Y[b.node2-1, sn-1] = +1
    return Y

def signed_voltage(branch: Branch, node: int) -> complex:
    if branch.node1 == node:
        return -branch.element.U
    else:
        return +branch.element.U

def create_current_vector_from_network(network: Network) -> np.ndarray:
    def full_admittance_between(node1: int, node2: int) -> complex:
        return sum(b.element.Y for b in network.branches_between(node1=node1, node2=node2) if np.isfinite(b.element.Y))
    def full_admittance_connected_to(node: int) -> complex:
        return sum(b.element.Y for b in network.branches_connected_to(node) if np.isfinite(b.element.Y))
    I = cna.create_current_vector_from_network(remove_ideal_voltage_sources(network))
    voltage_sources = get_ideal_voltage_sources(network)
    if len(voltage_sources.branches) == 0:
        return I
    for sn, vs in get_supernodes(network).items():
        I[sn-1] = full_admittance_connected_to(sn)*signed_voltage(vs, sn)
    for node in range(1,network.number_of_nodes):
        if node not in get_supernodes(network):
            for connected_supernode in network.nodes_connected_to(node).intersection(get_supernodes(network)):
                I[node-1] += full_admittance_between(node, connected_supernode)*-signed_voltage(get_supernodes(network)[connected_supernode], connected_supernode)
    return I

class NodalAnalysisSolution:
    def __init__(self, network : Network) -> None:
        Y = create_node_matrix_from_network(network)
        I = create_current_vector_from_network(network)
        self.solution_vector = cna.calculate_node_voltages(Y, I)
        self.super_nodes = get_supernodes(network)
        self.node_potentials = np.copy(self.solution_vector)
        for i, b in self.super_nodes.items():
            if i == b.node1:
                if b.node2 == 0:
                    self.node_potentials[i-1] = b.element.U
                else:
                    self.node_potentials[i-1] = b.element.U + self.node_potentials[b.node2-1]
            else:
                if b.node1 == 0:
                    self.node_potentials[i-1] = -b.element.U
                else:
                    self.node_potentials[i-1] = -b.element.U + self.node_potentials[b.node1-1]
        print('hello')
    
    def get_voltage(self, branch: Branch) -> complex:
        # if is_ideal_voltage_source(branch.element):
        #     return branch.element.U
        # if branch.node1 in self.super_nodes:
        #     return -(cna.calculate_branch_voltage(self.node_potentials, branch.node2, 0) + signed_voltage(self.super_nodes[branch.node1], branch.node1))
        # if branch.node2 in self.super_nodes:
        #     return cna.calculate_branch_voltage(self.node_potentials, branch.node1, 0) + signed_voltage(self.super_nodes[branch.node2], branch.node2)
        return cna.calculate_branch_voltage(self.node_potentials, branch.node1, branch.node2)

    def get_current(self, branch: Branch) -> complex:
        if is_ideal_voltage_source(branch.element):
            sn = list(self.super_nodes.keys())[list(self.super_nodes.values()).index(branch)]
            return self.solution_vector[sn-1]
        else:
            return self.get_voltage(branch)/branch.element.Z.real

def nodal_analysis_solver(network) -> NetworkSolution:
    return NodalAnalysisSolution(network)
