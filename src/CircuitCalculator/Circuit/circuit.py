from .components import Component
from .transformers import transformers
from ..Network.network import Network
import numpy as np
from dataclasses import dataclass, field
from typing import List

class MultipleGroundNodes(Exception): pass

@dataclass
class Circuit:
    components : list[Component]
    ground_node : str = field(init=False, default='')

    def __post_init__(self) -> None:
        if len(self.components) == 0:
            self.ground_node = ''
            return
        ground_components = [component.nodes[0] for component in self.components if component.type == 'ground']
        if len(ground_components) > 1:
            raise MultipleGroundNodes(f'Component list contains multiple ground nodes: {[c.nodes[0] for c in ground_components]}')
        if len(ground_components) == 0:
            self.ground_node = self.components[0].nodes[0]
        else:
            self.ground_node = ground_components[0]

    @property
    def w(self) -> list[float]:
        return [component.w for component in self.components if component.is_active]

def w(f: float) -> float:
    return 2*np.pi*f

def transform_circuit(circuit: Circuit, w: float, w_resolution: float = 1e-3) -> Network:
    return Network(
        branches=[transformers[type(component)](component, w, w_resolution) for component in circuit.components if type(component) in transformers.keys()],
        node_zero_label=circuit.ground_node
    )

def transform(circuit: Circuit, w: List[float] = [0], w_resolution: float = 1e-3) -> List[Network]:
    return [transform_circuit(circuit, w_, w_resolution) for w_ in w]