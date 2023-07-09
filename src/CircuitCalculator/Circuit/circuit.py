from .components import Component, PeriodicCurrentSource, PeriodicVoltageSource
from .transformers import transformers
from ..Network.network import Network
import numpy as np
from dataclasses import dataclass, field

class MultipleGroundNodes(Exception): pass

@dataclass
class Circuit:
    components : list[Component]
    ground_node : str = field(init=False, default='')

    def __post_init__(self) -> None:
        if len(self.components) == 0:
            self.ground_node = ''
            return
        ground_nodes = [component.nodes[0] for component in self.components if component.type == 'ground']
        if len(ground_nodes) > 1:
            raise MultipleGroundNodes(f'Component list contains multiple ground nodes: {str(ground_nodes)}')
        if len(ground_nodes) == 0:
            self.ground_node = self.components[0].nodes[0]
        else:
            self.ground_node = ground_nodes[0]

def w(f: float) -> float:
    return 2*np.pi*f

def transform_circuit(circuit: Circuit, w: float, w_resolution: float = 1e-3) -> Network:
    return Network(
        branches=[transformers[type(component)](component, w, w_resolution) for component in circuit.components if type(component) in transformers.keys()],
        node_zero_label=circuit.ground_node
    )

def transform(circuit: Circuit, w: list[float] = [0], w_resolution: float = 1e-3) -> list[Network]:
    return [transform_circuit(circuit, w_, w_resolution) for w_ in w]

def frequency_components(circuit: Circuit, w_max: float) -> list[float]:
    active_components = [c for c in circuit.components if c.is_active]
    w = []
    for ac in active_components:
        if type(ac) == PeriodicVoltageSource or type(ac) == PeriodicCurrentSource:
            w.extend(ac.frequency_components(w_max))
        else:
            w.append(ac.w)
    w = list(set(w))
    w.sort()
    return w