import pytest
from CircuitCalculator.Network.circuit import Resistor, VoltageSource, transform

def test_weis_net() -> None:
    circuit = [VoltageSource(V=1, nodes=('1', '0'), id='V1'), Resistor(R=100, nodes=('0', '1'), id='R1')]

    network = transform(circuit)
    
    assert False