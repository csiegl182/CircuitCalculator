from CircuitCalculator.Network import load_network_from_json
from CircuitCalculator.AdvancedNodalAnalysis import nodal_analysis_solver
from CircuitCalculator.EquivalentSources import *

if __name__ == '__main__':
    network = load_network_from_json('./examples/example_network_10.json')
    solution = nodal_analysis_solver(network)
    for branch in network.branches:
        print(f'{branch.node1}->{branch.node2} U={solution.get_voltage(branch):2.2f}V')
        print(f'{branch.node1}->{branch.node2} I={solution.get_current(branch):2.2f}A')

    thevenin_source = TheveninEquivalentSource(network, node1=0, node2=3)
    