from .Components.components import Component
from .transformers import transformers
from .symbolic_transformers import transformers as symbolic_transformers
from ..Network.network import Network
import numpy as np
import sympy as sp
from dataclasses import dataclass, field

class MultipleGroundNodes(Exception): pass
class AmbiguousComponentID(Exception): pass
class CircuitTransformationError(Exception): pass

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
        if len(set([component.id for component in self.components])) != len(self.components):
            raise AmbiguousComponentID(f'Component list contains multiple components with the same ID.')

    def __getitem__(self, key: str) -> Component:
        if key == self.ground_node:
            raise KeyError('Ground node is not a component.')
        index = [component.id for component in self.components].index(key)
        return self.components[index]

    def __iter__(self):
        return (component for component in self.components if component.type != 'ground')

def w(f: float) -> float:
    return 2*np.pi*f

def transform_circuit(circuit: Circuit, w: float, w_resolution: float = 1e-3, rms: bool = True) -> Network:
    try:
        return Network(
            branches=[transformers[component.type](component, w, w_resolution, rms) for component in circuit],
            node_zero_label=circuit.ground_node
        )
    except (ValueError, KeyError) as e:
        raise CircuitTransformationError from e

def transform(circuit: Circuit, w: list[float] = [0], w_resolution: float = 1e-3, rms: bool = True) -> list[Network]:
    return [transform_circuit(circuit, w_, w_resolution, rms) for w_ in w]

def frequency_components(circuit: Circuit, w_max: float) -> list[float]:
    def frequencies(component: Component) -> list[float]:
        try:
            w = float(component.value['w'])
        except KeyError:
            return []
        if component.type == 'periodic_voltage_source' or component.type == 'periodic_current_source':
            n_max = np.floor(w_max/w)
            return [w*n for n in np.arange(n_max+1)]
        return [w]
    return sorted(list(set([w for c in circuit.components for w in frequencies(c)])))

def transform_symbolic_circuit(circuit: Circuit, s: sp.Symbol = sp.Symbol('s', complex=True)) -> Network:
    try:
        return Network(
            branches=[symbolic_transformers[component.type](component, s) for component in circuit],
            node_zero_label=circuit.ground_node
        )   
    except (ValueError, KeyError) as e:
        raise CircuitTransformationError from e