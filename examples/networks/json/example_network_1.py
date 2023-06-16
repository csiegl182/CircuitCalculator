from CircuitCalculator.Network.loaders import load_network_from_json
from CircuitCalculator.Network.NodalAnalysis import nodal_analysis_solver as solver

if __name__ == '__main__':
    network = load_network_from_json('./examples/networks/json/example_network_1.json')
    solution = solver(network)
    print(f'I={solution.get_current("Uq"):2.2f}A')
    print(f'I={solution.get_current("R"):2.2f}A')
    print(f'V={solution.get_voltage("R"):2.2f}V')
