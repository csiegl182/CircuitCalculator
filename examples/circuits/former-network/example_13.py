from CircuitCalculator.Circuit.circuit import Circuit
import CircuitCalculator.Circuit.components as ccp
from CircuitCalculator.Circuit.solution import ComplexSolution

if __name__ == '__main__':
    circuit = Circuit([
        ccp.complex_voltage_source(V=1-2j, id='Vs', nodes=('1', '0')),
        ccp.impedance(Z=10+10j, id='Z1', nodes=('1', '0')),
        ccp.impedance(Z=20, id='Z2', nodes=('1', '2')),
        ccp.impedance(Z=30, id='Z3', nodes=('2', '0'))
    ])

    solution = ComplexSolution(circuit)
    print(f'I(Vs)={solution.get_current("Vs"):2.2f}A')
    print(f'I(Z1)={solution.get_current("Z1"):2.2f}A')
    print(f'I(Z2)={solution.get_current("Z2"):2.2f}A')
    print(f'I(Z3)={solution.get_current("Z3"):2.2f}A')
    print(f'V(Vs)={solution.get_voltage("Vs"):2.2f}V')
    print(f'V(Z1)={solution.get_voltage("Z1"):2.2f}V')
    print(f'V(Z2)={solution.get_voltage("Z2"):2.2f}V')
    print(f'V(Z3)={solution.get_voltage("Z3"):2.2f}V')