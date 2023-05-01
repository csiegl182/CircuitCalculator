
from CircuitCalculator.Circuit.circuit import transform, w
import CircuitCalculator.Circuit.components as cmp
from CircuitCalculator.Network.NodalAnalysis import nodal_analysis_solver

if __name__ == '__main__':
    circuit = [
        cmp.Ground(nodes=('0',)),
        cmp.VoltageSource(V=1, id='Uq', w=w(f=1000), nodes=('1', '0')),
        cmp.Resistor(R=2, id='R1', nodes=('1', '2')),
        cmp.Capacitor(C=1e-4, id='C', nodes=('2', '0'))
    ]
    
    solution = nodal_analysis_solver(transform(circuit, w=w(f=1000))[0])

    U_R1 = solution.get_voltage('R1')
    U_C = solution.get_voltage('C')
    I = solution.get_current('Uq')
    print(f'{U_R1=:4.2f}V')
    print(f'{U_C=:4.2f}V')
    print(f'{I=:4.2f}A')