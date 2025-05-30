import pytest
from CircuitCalculator.Circuit import circuit
import CircuitCalculator.Circuit.Components.components as ccp

def test_circuit_can_be_instantiated() -> None:
    c = circuit.Circuit([])
    assert c is not None

def test_circuit_can_be_instantiated_with_components() -> None:
    c = circuit.Circuit([ccp.dc_voltage_source(V=1, nodes=('1', '0'), id='V1')])
    assert c is not None

def test_circuit_with_multiple_ground_nodes_raises_exception() -> None:
    with pytest.raises(circuit.MultipleGroundNodes):
        circuit.Circuit([ccp.dc_voltage_source(V=1, nodes=('1', '0'), id='V1'), ccp.ground(nodes=('0', )), ccp.ground(nodes=('1', ))])

def test_circuit_with_multiple_components_with_same_id_raises_exception() -> None:
    with pytest.raises(circuit.AmbiguousComponentID):
        circuit.Circuit([ccp.dc_voltage_source(V=1, nodes=('1', '0'), id='V1'), ccp.dc_voltage_source(V=1, nodes=('1', '0'), id='V1')])

def test_component_id_can_be_accessed_from_circuit() -> None:
    c = circuit.Circuit([ccp.dc_voltage_source(V=1, nodes=('1', '0'), id='V1'), ccp.dc_voltage_source(V=1, nodes=('1', '0'), id='V2')])
    assert c['V1'] == c.components[0]
    assert c['V2'] == c.components[1]