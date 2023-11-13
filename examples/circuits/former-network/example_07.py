from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.components as ccp
from CircuitCalculator.Circuit.solution import DCSolution

if __name__ == '__main__':
    circuit = Circuit([
        ccp.dc_voltage_source(V=1, id='Vs1', nodes=('0', '5')),
        ccp.dc_voltage_source(V=2, id='Vs2', nodes=('2', '1')),
        ccp.dc_voltage_source(V=3, id='Vs3', nodes=('4', '3')),
        ccp.dc_current_source(I=0.1, id='Is', nodes=('3', '5')),
        ccp.resistor(R=10, id='R1', nodes=('1', '0')),
        ccp.resistor(R=20, id='R2', nodes=('1', '3')),
        ccp.resistor(R=30, id='R3', nodes=('2', '5')),
        ccp.resistor(R=40, id='R4', nodes=('4', '5'))
    ])

    solution = DCSolution(circuit)
    print(f'I(R1)={solution.get_current("R1"):2.2f}A')
    print(f'I(R2)={solution.get_current("R2"):2.2f}A')
    print(f'I(R3)={solution.get_current("R3"):2.2f}A')
    print(f'I(R4)={solution.get_current("R4"):2.2f}A')
    print(f'I(Vs1)={solution.get_current("Vs1"):2.2f}A')
    print(f'I(Vs2)={solution.get_current("Vs2"):2.2f}A')
    print(f'I(Vs3)={solution.get_current("Vs3"):2.2f}A')
    print(f'I(Is)={solution.get_current("Is"):2.2f}A')
    print(f'V(R1)={solution.get_voltage("R1"):2.2f}V')
    print(f'V(R2)={solution.get_voltage("R2"):2.2f}V')
    print(f'V(R3)={solution.get_voltage("R3"):2.2f}V')
    print(f'V(R4)={solution.get_voltage("R4"):2.2f}V')
    print(f'V(Vs1)={solution.get_voltage("Vs1"):2.2f}V')
    print(f'V(Vs2)={solution.get_voltage("Vs2"):2.2f}V')
    print(f'V(Vs3)={solution.get_voltage("Vs3"):2.2f}V')
    print(f'V(Is)={solution.get_voltage("Is"):2.2f}V')