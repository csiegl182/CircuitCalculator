from NodalAnalysis import *
import numpy as np
from typing import Callable, Any, Dict

branch_types : Dict[str, Callable[..., Element]] = {
    "resistor" : resistor,
    "real_current_source" : real_current_source
}

def load_network_from_json(filename) -> Network:
    import json
    with open(filename, 'r') as json_file:
        network_dict = json.load(json_file)

    network = Network()
    for branch in network_dict:
        n1 = branch.pop('N1')
        n2 = branch.pop('N2')
        element_factory = branch_types[branch.pop('type')]
        element = element_factory(**branch)
        network.add_branch(Branch(n1, n2, element))
    return network

if __name__ == '__main__':

    network = load_network_from_json('./example_network_1.json')
    Y = create_node_admittance_matrix_from_network(network)
    I = create_current_vector_from_network(network)
    U = calculate_node_voltages(Y, I)

    n1, n2 = 1, 0
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2)}')
    n1, n2 = 1, 2
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2)}')
    n1, n2 = 2, 0
    print(f'V({n1}->{n2}) = {calculate_branch_voltage(U, n1, n2)}')
