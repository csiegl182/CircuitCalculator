from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.components as ccp
from CircuitCalculator.Circuit.solution import DCSolution

if __name__ == '__main__':
    circuit = Circuit([
        ccp.dc_voltage_source(V=1, R=10, id='Vs', nodes=('1', '0')),
        ccp.resistor(R=10, id='R1', nodes=('1', '0')),
        ccp.resistor(R=20, id='R2', nodes=('1', '0'))
    ])

    solution = DCSolution(circuit)
    print(f'I(Vs)={solution.get_current("Vs"):2.2f}A')
    print(f'I(R1)={solution.get_current("R1"):2.2f}A')
    print(f'I(R2)={solution.get_current("R2"):2.2f}A')
    print(f'V(Vs)={solution.get_voltage("Vs"):2.2f}V')
    print(f'V(R1)={solution.get_voltage("R1"):2.2f}V')
    print(f'V(R2)={solution.get_voltage("R2"):2.2f}V')