from .components import Component
from .transformers import transformers
from ..Network.network import Network
import numpy as np
from dataclasses import dataclass
from typing import List

class MultipleGroundNodes(Exception): pass

@dataclass
class Circuit:
    components : list[Component]

    @property
    def w(self) -> list[float]:
        return [component.w for component in self.components if component.is_active]

def w(f: float) -> float:
    return 2*np.pi*f

def transform_circuit(circuit: Circuit, w: float, w_resolution: float = 1e-3) -> Network:
    ground_nodes = [component.nodes[0] for component in circuit.components if component.type == 'ground']
    if len(ground_nodes) > 1:
        raise MultipleGroundNodes
    if len(ground_nodes) == 0:
        ground_nodes = [circuit.components[0].nodes[0]]
    return Network(
        branches=[transformers[type(component)](component, w, w_resolution) for component in circuit.components if type(component) in transformers.keys()],
        node_zero_label=ground_nodes[0]
    )

def transform(circuit: Circuit, w: List[float] = [0], w_resolution: float = 1e-3) -> List[Network]:
    return [transform_circuit(circuit, w_, w_resolution) for w_ in w]