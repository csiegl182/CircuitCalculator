from CircuitCalculator.Circuit.circuit import Circuit, transform_circuit
import CircuitCalculator.Circuit.components as ccp
from CircuitCalculator.Network.NodalAnalysis import open_circuit_impedance

if __name__ == '__main__':
    circuit = Circuit([
        ccp.resistor(R=1, id='R1', nodes=('1', '3')),
        ccp.resistor(R=2, id='R2', nodes=('1', '4')),
        ccp.resistor(R=3, id='R3', nodes=('3', '4')),
        ccp.resistor(R=4, id='R4', nodes=('3', '0')),
        ccp.resistor(R=5, id='R5', nodes=('0', '4')),
        ccp.resistor(R=6, id='R6', nodes=('0', '2')),
        ccp.resistor(R=7, id='R7', nodes=('4', '2'))
    ])
    network = transform_circuit(circuit, w=0)
    Rges = open_circuit_impedance(network, '1', '2').real
    print(f'{Rges=:4.2f}Ω')