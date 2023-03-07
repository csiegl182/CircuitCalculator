from CircuitCalculator.Network.loaders import load_network_from_json
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

if __name__ == '__main__':
    network = load_network_from_json('./examples/example_network_2.json')
    solution = nodal_analysis_solver(network)
    for branch in network.branches:
        print(f'{branch.node1}->{branch.node2} U={solution.get_voltage(branch.id):2.2f}V')
        print(f'{branch.node1}->{branch.node2} I={solution.get_current(branch.id):2.2f}A')