import CircuitCalculator.Network.circuit as cct
import CircuitCalculator.Network.elements as elm

if __name__ == '__main__':
    circuit = [
        cct.Ground(nodes=('0',)),
        cct.VoltageSource(V=1, id='Uq', nodes=('0', '1')),
        cct.Resistor(R=1, id='R1', nodes=('0', '1'))
    ]