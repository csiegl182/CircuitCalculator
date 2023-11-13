from CircuitCalculator.Circuit.serializers import load_circuit_from_json
from CircuitCalculator.Circuit.solution import DCSolution

if __name__ == '__main__':
    circuit = load_circuit_from_json('./examples/circuits/json/example_circuit_1.json')
    solution = DCSolution(circuit)
    print(f'I(R)={solution.get_current("R"):2.2f}A')
    print(f'V(R)={solution.get_voltage("R"):2.2f}V')
