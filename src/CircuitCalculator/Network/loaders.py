from typing import Any, Callable
from .network import Network, Branch
from . import elements as elm
import numpy as np

class FileFormatError(Exception):
    ...

def to_complex(z: dict[str, float], degree: bool = False) -> complex:
    try:
        return complex(z['real'], z['imag'])
    except (KeyError, TypeError):
        ...
    try:
        if degree:
            z['phase'] *= np.pi/180
        return z['abs']*complex(np.cos(z['phase']), np.sin(z['phase']))
    except (KeyError, TypeError):
        raise FileFormatError

def translate_to_complex(keys : list[str], **kwargs):
    for value in keys:
        kwargs.update({value : to_complex(kwargs[value])})
    return kwargs

network_branch_translators : dict[str, Callable[..., elm.NortenTheveninElement]] = {
    "resistor" : elm.resistor,
    "conductor" : elm.conductor,
    "impedance" : lambda **kwargs: elm.impedance(Z=to_complex(kwargs.pop('Z')), **kwargs),
    "admittance" : lambda **kwargs: elm.admittance(Y=to_complex(kwargs['Y']), **kwargs),
    "linear_current_source" : lambda **kwargs: elm.current_source(**translate_to_complex(keys=['I', 'Y'], **kwargs)),
    "current_source" : lambda **kwargs: elm.current_source(I=to_complex(kwargs.pop('I')), **kwargs),
    "real_current_source" : elm.current_source,
    "linear_voltage_source" : lambda **kwargs: elm.voltage_source(V=to_complex(kwargs.pop('V')), Z=to_complex(kwargs.pop('Z')), **kwargs),
    "voltage_source" : lambda **kwargs: elm.voltage_source(V=to_complex(kwargs.pop('V')), **kwargs),
    "real_voltage_source" : elm.voltage_source,
    "short_circuit" : elm.short_circuit,
    "open_circuit" : elm.open_circuit,
}

def load_network(network_dict: list[dict[str, Any]]) -> Network:
    def entry_to_branch(entry: dict[str, Any]) -> Branch:
        n1 = entry.pop('N1')
        n2 = entry.pop('N2')
        entry['name'] = entry.pop('id')
        element_factory = network_branch_translators[entry.pop('type')]
        element = element_factory(**entry)
        return Branch(n1, n2, element)
    try: 
        return Network([entry_to_branch(entry) for entry in network_dict])
    except KeyError:
        raise FileExistsError

def load_network_from_json(filename: str) -> Network:
    import json
    with open(filename, 'r') as json_file:
        network_dict = json.load(json_file)
    return load_network(network_dict)