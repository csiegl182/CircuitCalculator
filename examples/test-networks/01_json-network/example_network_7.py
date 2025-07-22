from CircuitCalculator.Network.loaders import load_network_from_json
from CircuitCalculator.Network.NodalAnalysis.network_analysis import numeric_nodal_analysis_bias_point_solution

if __name__ == '__main__':
    network = load_network_from_json('./examples/test-networks/01_json-network/example_network_7.json')
    solution = numeric_nodal_analysis_bias_point_solution(network)
    for id in network.branch_ids:
        print(f'I({id})={solution.get_current(id):2.2f}A')
    for id in network.branch_ids:
        print(f'V({id})={solution.get_voltage(id):2.2f}V')