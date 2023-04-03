from .components import Component
from .transformers import transformers
from ..Network.network import Network
import numpy as np

Circuit = list[Component]

def w(f: float) -> float:
    return 2*np.pi*f

def transform(circuit: Circuit, w: float = 0, w_resolution: float = 1e-3) -> Network:
    ground_nodes = [component for component in circuit if component.type == 'ground']
    return Network(
        [transformers[type(component)](component, w, w_resolution) for component in circuit if type(component) in transformers.keys()],
        zero_node_label=ground_nodes[0].nodes[0]
    )