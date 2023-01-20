from typing import Any, Callable
from .network import Network, Branch
from .elements import Element
from . import elements as elm

branch_types : dict[str, Callable[..., Element]] = {
    "resistor" : elm.resistor,
    "impedance" : elm.impedance,
    "linear_current_source" : elm.linear_current_source,
    "current_source" : elm.current_source,
    "linear_voltage_source" : elm.linear_voltage_source,
    "voltage_source" : elm.voltage_source,
}

def load_network(network_dict: list[dict[str, Any]]) -> Network:
    branches = []
    for branch in network_dict:
        n1 = branch.pop('N1')
        n2 = branch.pop('N2')
        branch['name'] = branch.pop('id')
        element_factory = branch_types[branch.pop('type')]
        element = element_factory(**branch)
        branches.append(Branch(n1, n2, element))
    return Network(branches)

def load_network_from_json(filename: str) -> Network:
    import json
    with open(filename, 'r') as json_file:
        network_dict = json.load(json_file)
    return load_network(network_dict)