from CircuitCalculator.Network.loaders import load_network_from_json
from CircuitCalculator.Network.NodalAnalysis.bias_point_analysis import nodal_analysis_bias_point_solver
from CircuitCalculator.Network.matrix_operations import MatrixInversionException

if __name__ == '__main__':
    network = load_network_from_json('examples/test-networks/01_json-network/example_network_17.json')
    solution = nodal_analysis_bias_point_solver(network)
    for id in network.branch_ids:
        print(f'V({id})={solution.get_voltage(id):2.2f}V')
    for id in network.branch_ids:
        print(f'I({id})={solution.get_current(id):2.2f}A')
    for id in network.node_labels:
        print(f'V({id})={solution.get_potential(id):2.2f}V')