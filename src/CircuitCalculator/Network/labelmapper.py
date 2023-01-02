from .network import Network
from typing import Callable

NodeIndexMapper = Callable[[Network], dict[str, int]]

def alphabetic_mapper(network: Network) -> dict[str, int]:
    node_labels_without_zero = [label for label in sorted(network.node_labels) if label != network.zero_node_label] 
    return {k: v for v, k in enumerate(node_labels_without_zero)}

default = alphabetic_mapper