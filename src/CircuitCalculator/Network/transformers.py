from .network import Network, Branch
from .elements import NortenTheveninElement, is_current_source, is_voltage_source, is_short_circuit, is_open_circuit, impedance, admittance, is_open_circuit, is_short_circuit

def switch_ground_node(network: Network, new_ground: str) -> Network:
    return Network(network.branches, new_ground)

def remove_element(network: Network, element: str) -> Network:
    branches = list(network.branches)
    branches.remove(network[element])
    return Network(branches, node_zero_label=network.node_zero_label)

def remove_open_circuit_elements(network: Network) -> Network:
    return Network([b for b in network.branches if not is_open_circuit(b.element)], node_zero_label=network.node_zero_label)

def remove_short_circuit_elements(network: Network, keep: list[NortenTheveninElement] = []) -> Network:
    branches = network.branches
    short_circuits = [b for b in network.branches if is_short_circuit(b.element) and b.element not in keep]
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
        if is_voltage_source(branch.element):
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
        if is_current_source(branch.element):
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