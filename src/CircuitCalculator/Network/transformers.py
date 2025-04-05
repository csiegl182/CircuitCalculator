from .network import Network, Branch
from .elements import NortenTheveninElement, impedance, admittance

def switch_ground_node(network: Network, new_ground: str) -> Network:
    return Network(network.branches, new_ground)

def remove_element(network: Network, element: str) -> Network:
    branch_to_remove = network[element]
    if branch_to_remove.node1 == network.node_zero_label and len(network.branches_connected_to(branch_to_remove.node1)) == 1:
       network = rename_node(network, branch_to_remove.node2, network.node_zero_label) 
    if branch_to_remove.node2 == network.node_zero_label and len(network.branches_connected_to(branch_to_remove.node2)) == 1:
       network = rename_node(network, branch_to_remove.node1, network.node_zero_label) 
    branches = [b for b in network.branches if b.element.name != element]
    return Network(branches, node_zero_label=network.node_zero_label)
    
def remove_elements(network: Network, elements: list[str]) -> Network:
    for element in elements:
        network = remove_element(network, element)
    return network

def rename_node(network: Network, old_node: str, new_node: str) -> Network:
    def rename(branch: Branch) -> Branch:
        if branch.node1 == old_node:
            branch = Branch(new_node, branch.node2, branch.element)
        if branch.node2 == old_node:
            branch = Branch(branch.node1, new_node, branch.element)
        return branch
    branches = [rename(b) for b in network.branches]
    return Network(branches, node_zero_label=network.node_zero_label)

def remove_open_circuit_elements(network: Network) -> Network:
    return Network([b for b in network.branches if not b.element.is_open_circuit], node_zero_label=network.node_zero_label)

def remove_short_circuit_elements(network: Network, keep: list[NortenTheveninElement] = []) -> Network:
    branches = network.branches
    short_circuits = [b for b in network.branches if b.element.is_short_circuit and b.element not in keep]
    short_circuit_nodes = [(vs.node1, vs.node2) if not network.is_zero_node(vs.node1) else (vs.node2, vs.node1) for vs in short_circuits]
    for an, rn in short_circuit_nodes:
        branches = [Branch(rn, b.node2, b.element) if b.node1 == an else b for b in branches]
        branches = [Branch(b.node1, rn, b.element) if b.node2 == an else b for b in branches]
        branches = [b for b in branches if b.node1 != b.node2]
    return Network(branches, node_zero_label=network.node_zero_label)

def short_circuitify_voltage_sources(network: Network, keep: list[NortenTheveninElement] = []) -> Network:
    def zero_in_voltage(branch: Branch) -> Branch:
        return Branch(branch.node1, branch.node2, impedance(branch.element.name, branch.element.Z))
    def is_intended_voltage_source(branch: Branch) -> bool:
        if branch.element in keep:
            return False
        if branch.element.is_voltage_source:
            return True
        return False
    return Network(
        branches=[zero_in_voltage(b) if is_intended_voltage_source(b) else b for b in network.branches],
        node_zero_label=network.node_zero_label
    )

def open_circuitify_current_sources(network: Network, keep: list[NortenTheveninElement] = []) -> Network:
    def zero_in_current(branch: Branch) -> Branch:
        return Branch(branch.node1, branch.node2, admittance(branch.element.name, branch.element.Y))
    def is_intended_current_source(branch: Branch) -> bool:
        if branch.element in keep:
            return False
        if branch.element.is_current_source:
            return True
        return False
    return Network(
        branches=[zero_in_current(b) if is_intended_current_source(b) else b for b in network.branches],
        node_zero_label=network.node_zero_label
    )

def remove_ideal_current_sources(network: Network, keep: list[NortenTheveninElement] = []) -> Network:
    return remove_open_circuit_elements(open_circuitify_current_sources(network, keep=keep))

def remove_ideal_voltage_sources(network: Network, keep: list[NortenTheveninElement] = []) -> Network:
    return remove_short_circuit_elements(short_circuitify_voltage_sources(network, keep=keep), keep=keep)

def passive_network(network: Network, keep: list[NortenTheveninElement] = []) -> Network:
    return remove_ideal_voltage_sources(remove_ideal_current_sources(network, keep=keep), keep=keep)