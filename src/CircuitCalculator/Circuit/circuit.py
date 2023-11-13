from .components import Component, is_active
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
        branches=[transformers[component.type](component, w, w_resolution) for component in circuit.components if component.type in transformers.keys()],
        node_zero_label=circuit.ground_node
    )

def transform(circuit: Circuit, w: list[float] = [0], w_resolution: float = 1e-3) -> list[Network]:
    return [transform_circuit(circuit, w_, w_resolution) for w_ in w]

def frequency_components(circuit: Circuit, w_max: float) -> list[float]: # TODO
    active_components = [c for c in circuit.components if is_active(c)]
    w = []
    for ac in active_components:
        if ac.type == 'periodic_voltage_source' or ac.type == 'periodic_current_source':
            n_max = np.floor(w_max/float(ac.value['w']))
            w_vec = np.array([float(ac.value['w'])*n for n in np.arange(n_max)])
            w.extend(w_vec)
        else:
            w.append(ac.value['w'])
    w = list(set(w))
    w.sort()
    return w