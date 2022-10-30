import CircuitCalculator.ClassicNodalAnalysis as cna
import numpy as np
from .Network import Network, Branch, Element, NetworkSolution
from typing import Dict, List

class AmbiguousElectricalPotential(Exception): pass

def is_ideal_voltage_source(element: Element) -> bool:
    return element.active and element.Z==0 and np.isfinite(element.U)

def is_ideal_current_source(element: Element) -> bool:
    return element.active and element.Y==0 and np.isfinite(element.I)

def get_ideal_voltage_sources(network: Network) -> Network:
    return Network([b for b in network.branches if is_ideal_voltage_source(b.element)])

def remove_ideal_voltage_sources(network: Network) -> Network:
    return Network([b for b in network.branches if not is_ideal_voltage_source(b.element)])

def get_supernodes(network: Network) -> Dict[int, Branch]:
    voltage_sources = get_ideal_voltage_sources(network)
    supernodes = {}
    for vs in voltage_sources.branches:
        node = vs.node1
        if node == 0 or node in supernodes.keys():
            node = vs.node2
        if node == 0 or node in supernodes.keys():
            raise AmbiguousElectricalPotential
        supernodes.update({node: vs})
    return supernodes

def get_supernode_counterparts(network: Network) -> Dict[int, Branch]:
    counterparts = {}
    for sn, b in get_supernodes(network).items():
        if b.node1 == sn and b.node2 not in get_supernodes(network).keys():
            counterparts.update({b.node2: b})
        if b.node2 == sn and b.node1 not in get_supernodes(network).keys():
            counterparts.update({b.node1: b})
    counterparts.pop(0, None)
    return counterparts

def get_non_supernodes(network: Network) -> List[int]:
    return list(set(range(1, network.number_of_nodes)).difference(get_supernodes(network).keys()))

def create_node_matrix_from_network(network: Network) -> np.ndarray:
    def fill_supernode_part(Y: np.ndarray) -> np.ndarray:
        for super_node, b in get_supernodes(network).items():
            sign = np.sign(b.element.U)
            opposite_node = b.node1
            if super_node == b.node1: # voltage arrow points out of super node
                sign *= -1
                opposite_node = b.node2
            Y[super_node-1, super_node-1] = sign
            if opposite_node > 0:
                Y[opposite_node-1, super_node-1] = -sign
        return Y
    def fill_non_supernode_part(Y: np.ndarray) -> np.ndarray:
        non_supernode_indices = [node-1 for node in get_non_supernodes(network)]
        Y_cna = cna.create_node_admittance_matrix_from_network(remove_ideal_voltage_sources(network))
        Y[:, non_supernode_indices] = Y_cna[:, non_supernode_indices]
        for cp, b in get_supernode_counterparts(network).items():
            if b.node1 == cp:
                Y[:,cp-1] += Y_cna[:,b.node2-1]
            else:
                Y[:,cp-1] += Y_cna[:,b.node1-1]
        return Y
    Y = np.zeros((network.number_of_nodes-1, network.number_of_nodes-1))
    Y = fill_non_supernode_part(Y)
    Y = fill_supernode_part(Y)
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
        I[sn-1] += full_admittance_connected_to(sn)*signed_voltage(vs, sn)
    for node in range(1,network.number_of_nodes):
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
    
    def get_voltage(self, branch: Branch) -> complex:
        return cna.calculate_branch_voltage(self.node_potentials, branch.node1, branch.node2)

    def get_current(self, branch: Branch) -> complex:
        if is_ideal_voltage_source(branch.element):
            sn = list(self.super_nodes.keys())[list(self.super_nodes.values()).index(branch)]
            return self.solution_vector[sn-1]
        elif is_ideal_current_source(branch.element):
            return branch.element.I
        else:
            return self.get_voltage(branch)/branch.element.Z.real

def nodal_analysis_solver(network) -> NetworkSolution:
    return NodalAnalysisSolution(network)
