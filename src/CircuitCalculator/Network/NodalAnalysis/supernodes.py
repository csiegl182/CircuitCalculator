from ..network import Network, ideal_voltage_sources
from ..elements import is_ideal_voltage_source
from dataclasses import dataclass

class AmbiguousElectricalPotential(Exception): pass

class CorruptedNetworkStructure(Exception): pass

@dataclass(frozen=True)
class SuperNode:
    reference_node: str
    active_node: str
    voltage_source: str

class SuperNodes:
    def __init__(self, network: Network) -> None:
        self._super_nodes : list[SuperNode] = []
        for voltage_source in ideal_voltage_sources(network):
            node, other_node = voltage_source.node1, voltage_source.node2
            if network.is_zero_node(node) or node in self.active_nodes:
                node, other_node = other_node, node
            if network.is_zero_node(node) or node in self.active_nodes:
                raise AmbiguousElectricalPotential
            self._super_nodes.append(
                SuperNode(
                    reference_node=other_node,
                    active_node=node,
                    voltage_source=voltage_source.id
                )
            )

    @property
    def active_nodes(self) -> list[str]:
        return [sn.active_node for sn in self._super_nodes]

    @property
    def reference_nodes(self) -> list[str]:
        return [sn.reference_node for sn in self._super_nodes]

    @property
    def voltage_sources(self) -> list[str]:
        return [sn.voltage_source for sn in self._super_nodes]

    def is_active(self, node: str) -> bool:
        return node in self.active_nodes
    
    def is_reference(self, node: str) -> bool:
        return node in self.reference_nodes

    def belong_to_same(self, active_node: str, reference_node: str) -> bool:
        if self.is_active(active_node):
            if self.is_reference(reference_node):
                return self.reference_node(active_node) == reference_node
        return False

    def active_node(self, reference_node: str) -> str:
        return self.active_nodes[self.reference_nodes.index(reference_node)]

    def reference_node(self, active_node: str) -> str:
        return self.reference_nodes[self.active_nodes.index(active_node)]

    def non_active_reference_node(self, active_node: str) -> str:
        return self.nodes_to_non_active_reference_node(active_node)[-1]

    def nodes_to_non_active_reference_node(self, active_node: str) -> list[str]:
        nodes = [active_node]
        while self.is_active(nodes[-1]):
            nodes.append(self.reference_node(nodes[-1]))
            if len(nodes) > len(self._super_nodes)+1:
                raise CorruptedNetworkStructure
        return nodes

def voltage_to_next_reference(network: Network, super_nodes: SuperNodes, active_node: str) -> complex:
    def voltage_between(node1: str, node2: str) -> complex:
        branches = network.branches_between(node1, node2)
        voltage_sources = [b for b in branches if is_ideal_voltage_source(b.element)]
        if len(voltage_sources) != 1:
            raise AmbiguousElectricalPotential
        voltage_source = voltage_sources[0]
        if voltage_source.node1 == node2:
            return -voltage_source.element.V
        return voltage_source.element.V
    voltage_source_node_pairs = zip(super_nodes.nodes_to_non_active_reference_node(active_node)[:-1], super_nodes.nodes_to_non_active_reference_node(active_node)[1:])
    return sum([voltage_between(n1, n2) for n1, n2 in voltage_source_node_pairs])

def voltage_source_labels_to_next_reference(network: Network, super_nodes: SuperNodes, active_node: str) -> list[str]:
    def voltage_source_between(node1: str, node2: str) -> str:
        branches = network.branches_between(node1, node2)
        voltage_sources = [b for b in branches if is_ideal_voltage_source(b.element)]
        if len(voltage_sources) != 1:
            raise AmbiguousElectricalPotential
        return voltage_sources[0].id
    voltage_source_node_pairs = zip(super_nodes.nodes_to_non_active_reference_node(active_node)[:-1], super_nodes.nodes_to_non_active_reference_node(active_node)[1:])
    return [voltage_source_between(n1, n2) for n1, n2 in voltage_source_node_pairs]