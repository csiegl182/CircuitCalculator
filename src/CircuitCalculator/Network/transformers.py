from .network import Network, Branch
from .elements import NortenTheveninElement, is_ideal_current_source, is_ideal_voltage_source
from .supernodes import SuperNodes

def switch_ground_node(network: Network, new_ground: str) -> Network:
    return Network(network.branches, new_ground)

def remove_element(network: Network, element: str) -> Network:
    branches = list(network.branches)
    branches.remove(network[element])
    return Network(branches)

def remove_ideal_current_sources(network: Network, keep: list[NortenTheveninElement] = []) -> Network:
    return Network([b for b in network.branches if not is_ideal_current_source(b.element) or b.element in keep], node_zero_label=network.node_zero_label)

def remove_ideal_voltage_sources(network: Network, keep: list[NortenTheveninElement] = []) -> Network:
    branches = network.branches
    super_nodes = SuperNodes(network)
    voltage_sources = [b for b in network.branches if is_ideal_voltage_source(b.element)]
    voltage_sources = [vs for vs in voltage_sources if vs.element not in keep]
    short_circuit_nodes = [(vs.node1, vs.node2) if super_nodes.is_active(vs.node1) else (vs.node2, vs.node1) for vs in voltage_sources]
    for an, rn in short_circuit_nodes:
        branches = [Branch(rn, b.node2, b.element) if b.node1 == an else b for b in branches]
        branches = [Branch(b.node1, rn, b.element) if b.node2 == an else b for b in branches]
        branches = [b for b in branches if b.node1 != b.node2]
    return Network(branches, node_zero_label=network.node_zero_label)

def passive_network(network: Network, keep: list[NortenTheveninElement] = []) -> Network:
    return remove_ideal_voltage_sources(remove_ideal_current_sources(network, keep=keep), keep=keep)