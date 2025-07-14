from .network import Network, Branch
from .norten_thevenin_elements import NortenTheveninElement
from . import elements as elm
from . import symbolic_elements as selm
import sympy as sp

def switch_ground_node(network: Network, new_ground: str) -> Network:
    return Network(network.branches, new_ground)

def remove_element(network: Network, element: str) -> Network:
    branch_to_remove = network[element]
    if branch_to_remove.node1 == network.reference_node_label and len(network.branches_connected_to(branch_to_remove.node1)) == 1:
       network = rename_node(network, branch_to_remove.node2, network.reference_node_label) 
    if branch_to_remove.node2 == network.reference_node_label and len(network.branches_connected_to(branch_to_remove.node2)) == 1:
       network = rename_node(network, branch_to_remove.node1, network.reference_node_label) 
    branches = [b for b in network.branches if b.element.name != element]
    return Network(branches, reference_node_label=network.reference_node_label)

def rename_node(network: Network, old_node: str, new_node: str) -> Network:
    def rename(branch: Branch) -> Branch:
        if branch.node1 == old_node:
            branch = Branch(new_node, branch.node2, branch.element)
        if branch.node2 == old_node:
            branch = Branch(branch.node1, new_node, branch.element)
        return branch
    branches = [rename(b) for b in network.branches]
    return Network(branches, reference_node_label=network.reference_node_label)

def remove_active_elements(network: Network) -> Network:
    def impedance(e: NortenTheveninElement) -> NortenTheveninElement:
        try:
            Z = complex(e.Z)
        except TypeError:
            return selm.impedance(name=e.name, Z=sp.sympify(e.Z))
        return elm.impedance(name=e.name, Z=Z)
    def admittance(e: NortenTheveninElement) -> NortenTheveninElement:
        try:
            Y = complex(e.Y)
        except TypeError:
            return selm.admittance(name=e.name, Y=sp.sympify(e.Y))
        return elm.admittance(name=e.name, Y=Y)
    def remove(b: Branch) -> Branch:
        if b.element.is_ideal_voltage_source:
            return Branch(b.node1, b.node2, elm.open_circuit(b.element.name))
        if b.element.is_ideal_current_source:
            return Branch(b.node1, b.node2, elm.open_circuit(b.element.name))
        if b.element.is_voltage_source:
            return Branch(b.node1, b.node2, impedance(b.element))
        if b.element.is_current_source:
            return Branch(b.node1, b.node2, admittance(b.element))
        return b
    return Network(
        branches=[remove(b) for b in network.branches],
        reference_node_label=network.reference_node_label
    )