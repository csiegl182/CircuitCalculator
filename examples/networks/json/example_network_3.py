from CircuitCalculator.Network.loaders import load_network_from_json
from CircuitCalculator.Network.NodalAnalysis import nodal_analysis_solver

if __name__ == '__main__':
    network = load_network_from_json('./examples/networks/json/example_network_3.json')
    solution = nodal_analysis_solver(network)
    print(f'U(I1)={solution.get_voltage("I1"):2.2f}V')
    print(f'U(R1)={solution.get_voltage("R1"):2.2f}V')
    print(f'U(R2)={solution.get_voltage("R2"):2.2f}V')
    print(f'I(I1)={solution.get_current("I1"):2.2f}A')
    print(f'I(R1)={solution.get_current("R1"):2.2f}A')
    print(f'I(R2)={solution.get_current("R2"):2.2f}A')