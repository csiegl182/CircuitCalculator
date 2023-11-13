from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.components as ccp
from CircuitCalculator.Circuit.solution import DCSolution

if __name__ == '__main__':
    circuit = Circuit([
        ccp.dc_current_source(I=4, id='Is', nodes=('0', '1')),
        ccp.dc_voltage_source(V=120, id='Vs', nodes=('3', '2')),
        ccp.resistor(R=15, id='R1', nodes=('1', '0')),
        ccp.resistor(R=5, id='R2', nodes=('1', '2')),
        ccp.resistor(R=20, id='R3', nodes=('2', '0')),
        ccp.resistor(R=20, id='R4', nodes=('3', '0'))
    ])

    solution = DCSolution(circuit)
    print(f'I(Is)={solution.get_current("Is"):2.2f}A')
    print(f'I(Vs)={solution.get_current("Vs"):2.2f}A')
    print(f'I(R1)={solution.get_current("R1"):2.2f}A')
    print(f'I(R2)={solution.get_current("R2"):2.2f}A')
    print(f'I(R3)={solution.get_current("R3"):2.2f}A')
    print(f'I(R4)={solution.get_current("R4"):2.2f}A')
    print(f'V(Is)={solution.get_voltage("Is"):2.2f}V')
    print(f'V(Vs)={solution.get_voltage("Vs"):2.2f}V')
    print(f'V(R1)={solution.get_voltage("R1"):2.2f}V')
    print(f'V(R2)={solution.get_voltage("R2"):2.2f}V')
    print(f'V(R3)={solution.get_voltage("R3"):2.2f}V')
    print(f'V(R4)={solution.get_voltage("R4"):2.2f}V')