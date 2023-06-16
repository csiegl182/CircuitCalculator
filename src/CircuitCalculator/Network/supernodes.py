from .network import Network, ideal_voltage_sources
from .elements import NortenTheveninElement
from dataclasses import dataclass
import numpy as np

class AmbiguousElectricalPotential(Exception): pass

@dataclass(frozen=True)
class SuperNode:
    reference_node: str
    active_node: str
    voltage: complex
    voltage_source: NortenTheveninElement

class SuperNodes:
    def __init__(self, network: Network) -> None:
        self._super_nodes : list[SuperNode] = []
        self.voltage_sources: list[NortenTheveninElement] = []
        for voltage_source in ideal_voltage_sources(network):
            node, other_node = voltage_source.node1, voltage_source.node2
            if network.is_zero_node(node) or node in self.active_nodes:
                node, other_node = other_node, node
            if network.is_zero_node(node) or node in self.active_nodes:
                raise AmbiguousElectricalPotential
            self.voltage_sources.append(voltage_source.element)
            self._super_nodes.append(
                SuperNode(
                    reference_node=other_node,
                    active_node=node,
                    voltage=voltage_source.element.V if node == voltage_source.node1 else -voltage_source.element.V,
                    voltage_source=voltage_source.element
                )
            )

    @property
    def active_nodes(self) -> list[str]:
        return [sn.active_node for sn in self._super_nodes]

    @property
    def reference_nodes(self) -> list[str]:
        return [sn.reference_node for sn in self._super_nodes]

    @property
    def voltages(self) -> list[complex]:
        return [sn.voltage for sn in self._super_nodes]

    def is_active(self, node: str) -> bool:
        return node in self.active_nodes
    
    def is_reference(self, node: str) -> bool:
        return node in self.reference_nodes

    def belong_to_same(self, active_node: str, reference_node: str) -> bool:
        if self.is_active(active_node):
            if self.is_reference(reference_node):
                return self.get_reference_node(active_node) == reference_node
        return False

    def get_active_node(self, reference_node: str) -> str:
        return self.active_nodes[self.reference_nodes.index(reference_node)]

    def get_reference_node(self, active_node: str) -> str:
        return self.reference_nodes[self.active_nodes.index(active_node)]

    def get_voltage(self, active_node: str) -> complex:
        return self.voltages[self.active_nodes.index(active_node)]

    def sign(self, active_node: str) -> int:
        return np.sign(self.voltages[self.active_nodes.index(active_node)])

    def voltage_to_next_reference(self, active_node: str) -> complex:
        V = 0+0j
        while self.is_active(active_node):
            V += self.voltages[self.active_nodes.index(active_node)]
            active_node = self.get_reference_node(active_node)
        return V

    def next_reference(self, active_node: str) -> str:
        while self.is_active(active_node):
            active_node = self.get_reference_node(active_node)
        return active_node