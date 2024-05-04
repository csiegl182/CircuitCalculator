from ..network import Network
from ..elements import is_current_source, is_ideal_voltage_source
from .supernodes import SuperNodes
from typing import Callable

NodeIndexMapper = Callable[[Network], dict[str, int]]
SourceIndexMapper = Callable[[Network], list[str]]

def alphabetic_node_mapper(network: Network) -> dict[str, int]:
    super_nodes = SuperNodes(network=network)
    node_labels_without_zero = [label for label in sorted(network.node_labels) if label != network.node_zero_label and not super_nodes.is_active(label)] 
    return {k: v for v, k in enumerate(node_labels_without_zero)}

default_node_mapper = alphabetic_node_mapper

def alphabetic_source_mapper(network: Network) -> list[str]:
    current_source_labels = sorted([b.id for b in network.branches if is_current_source(b.element)])
    voltage_source_labels = sorted([b.id for b in network.branches if is_ideal_voltage_source(b.element)])
    return current_source_labels+voltage_source_labels

default_source_mapper = alphabetic_source_mapper

