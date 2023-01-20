from CircuitCalculator.Network.loaders import load_network_from_json
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver
from CircuitCalculator.PointerDiagram import PointerDiagram

if __name__ == '__main__':
    network = load_network_from_json('./examples/example_network_12.json')
    solution = nodal_analysis_solver(network)
    for branch in network.branches:
        print(f'{branch.node1}->{branch.node2} U={solution.get_voltage(branch):2.2f}V')
        print(f'{branch.node1}->{branch.node2} I={solution.get_current(branch):2.2f}A')

    with PointerDiagram() as pointer_diagram:
        pointer_diagram.add_pointer(1+1j)