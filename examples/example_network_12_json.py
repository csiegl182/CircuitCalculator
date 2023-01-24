from CircuitCalculator.Network.loaders import load_network_from_json
from CircuitCalculator.NodalAnalysis import nodal_analysis_solver
from CircuitCalculator.SimpleAnalysis.PointerDiagram import VoltagePointerDiagram

if __name__ == '__main__':
    network = load_network_from_json('./examples/example_network_12.json')
    solution = nodal_analysis_solver(network)
    for id in network.branch_ids:
        print(f'{network[id].node1}->{network[id].node2} U={solution.get_voltage(id):2.2f}V')
        print(f'{network[id].node1}->{network[id].node2} I={solution.get_current(id):2.2f}A')

    with VoltagePointerDiagram(solution, conductor = 10) as pointer_diagram:
        pointer_diagram.add_voltage_pointer('R')
        pointer_diagram.add_voltage_pointer('I', origin='R')
        pointer_diagram.add_voltage_pointer('Z', origin='I', color='black')
        pointer_diagram.add_current_pointer('I')
