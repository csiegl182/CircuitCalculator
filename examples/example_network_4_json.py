from CircuitCalculator.Network import load_network_from_json
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver

if __name__ == '__main__':
    network = load_network_from_json('./examples/example_network_4.json')
    solution = nodal_analysis_solver(network)
    for branch in network.branches:
        print(f'{branch.node1}->{branch.node2} U={solution.get_voltage(branch):2.2f}V')
        print(f'{branch.node1}->{branch.node2} I={solution.get_current(branch):2.2f}A')