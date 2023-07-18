from .network import Network
from .supernodes import SuperNodes
from typing import Callable

NodeIndexMapper = Callable[[Network], dict[str, int]]

def alphabetic_mapper(network: Network) -> dict[str, int]:
    super_nodes = SuperNodes(network=network)
    node_labels_without_zero = [label for label in sorted(network.node_labels) if label != network.node_zero_label and not super_nodes.is_active(label)] 
    return {k: v for v, k in enumerate(node_labels_without_zero)}

default = alphabetic_mapper