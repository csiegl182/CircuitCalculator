from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.components as ccp
from CircuitCalculator.Circuit.solution import DCSolution

if __name__ == '__main__':
    circuit = Circuit([
        ccp.dc_current_source(I=1, id='Is', nodes=('0', '1')),
        ccp.resistor(R=1, id='R', nodes=('1', '0'))
    ])

    solution = DCSolution(circuit)
    print(f'I(R)={solution.get_current("R"):2.2f}A')
    print(f'V(R)={solution.get_voltage("R"):2.2f}V')