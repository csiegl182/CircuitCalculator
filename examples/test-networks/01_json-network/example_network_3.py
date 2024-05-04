from CircuitCalculator.Network.loaders import load_network_from_json
from CircuitCalculator.Network.NodalAnalysis.node_analysis import nodal_analysis_solver

if __name__ == '__main__':
    network = load_network_from_json('./examples/networks/json/example_network_3.json')
    solution = nodal_analysis_solver(network)
    for id in network.branch_ids:
        print(f'I({id})={solution.get_current(id):2.2f}A')
    for id in network.branch_ids:
        print(f'V({id})={solution.get_voltage(id):2.2f}V')