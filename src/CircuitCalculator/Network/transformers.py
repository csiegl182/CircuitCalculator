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