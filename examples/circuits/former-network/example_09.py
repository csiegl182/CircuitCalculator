from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.components as ccp
from CircuitCalculator.Circuit.solution import DCSolution

if __name__ == '__main__':
    circuit = Circuit([
        ccp.dc_voltage_source(V=1, id='Vs1', nodes=('1', '0')),
        ccp.dc_voltage_source(V=2, id='Vs2', nodes=('2', '1')),
        ccp.resistor(R=10, id='R', nodes=('2', '0'))
    ])

    solution = DCSolution(circuit)
    print(f'I(R)={solution.get_current("R"):2.2f}A')
    print(f'I(Vs1)={solution.get_current("Vs1"):2.2f}A')
    print(f'I(Vs2)={solution.get_current("Vs2"):2.2f}A')
    print(f'V(R)={solution.get_voltage("R"):2.2f}V')
    print(f'V(Vs1)={solution.get_voltage("Vs1"):2.2f}V')
    print(f'V(Vs2)={solution.get_voltage("Vs2"):2.2f}V')