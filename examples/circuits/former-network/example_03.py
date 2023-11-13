from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.components as ccp
from CircuitCalculator.Circuit.solution import DCSolution

if __name__ == '__main__':
    circuit = Circuit([
        ccp.dc_current_source(I=1, G=0.01, id='Is', nodes=('0', '1')),
        ccp.resistor(R=10, id='R1', nodes=('1', '2')),
        ccp.resistor(R=20, id='R2', nodes=('2', '0'))
    ])

    solution = DCSolution(circuit)
    print(f'I(R1)={solution.get_current("R1"):2.2f}A')
    print(f'I(R2)={solution.get_current("R2"):2.2f}A')
    print(f'I(Is)={solution.get_current("Is"):2.2f}A')
    print(f'V(R1)={solution.get_voltage("R1"):2.2f}V')
    print(f'V(R2)={solution.get_voltage("R2"):2.2f}V')
    print(f'V(Is)={solution.get_voltage("Is"):2.2f}V')