import pytest
from CircuitCalculator.Circuit.serializers import load_circuit, UnknownCircuitComponent, IncorrectComponentInformation, UnidentifiedComponent

def test_circuit_can_be_loaded_from_dict() -> None:
    test_circuit = [
        {
            'type': 'voltage_source',
            'id': 'Vs',
            'nodes': ('1', '0'),
            'value': {'V': 1}
        },
        {
            'type': 'resistor',
            'id': 'R1',
            'nodes': ('0', '1'),
            'value': {'R': 10}
        }
    ]
    circuit = load_circuit(test_circuit)
    assert circuit.components[0].type == test_circuit[0]['type']
    assert circuit.components[1].type == test_circuit[1]['type']

def test_undefined_component_type_leads_to_error() -> None:
    test_circuit = [
        {
            'type': 'not_a_voltage_source',
            'id': 'Vs',
            'nodes': ('1', '0'),
            'value': {'V': 1}
        },
        {
            'type': 'resistor',
            'id': 'R1',
            'nodes': ('0', '1'),
            'value': {'R': 10}
        }
    ]
    with pytest.raises(UnknownCircuitComponent):
        load_circuit(test_circuit)

def test_missing_component_type_leads_to_error() -> None:
    test_circuit = [
        {
            'id': 'Vs',
            'nodes': ('1', '0'),
            'value': {'V': 1}
        },
        {
            'type': 'resistor',
            'id': 'R1',
            'nodes': ('0', '1'),
            'value': {'R': 10}
        }
    ]
    with pytest.raises(IncorrectComponentInformation):
        load_circuit(test_circuit)

def test_missing_component_id_leads_to_error() -> None:
    test_circuit = [
        {
            'type': 'voltage_source',
            'nodes': ('1', '0'),
            'value': {'V': 10}
        },
        {
            'type': 'resistor',
            'id': 'R1',
            'nodes': ('0', '1'),
            'value': {'R': 10}
        }
    ]
    with pytest.raises(UnidentifiedComponent):
        load_circuit(test_circuit)

def test_odd_value_information_leads_to_error() -> None:
    test_circuit = [
        {
            'type': 'voltage_source',
            'id': 'Vs',
            'nodes': ('1', '0'),
            'value': {'R': 1}
        },
        {
            'type': 'resistor',
            'id': 'R1',
            'nodes': ('0', '1'),
            'value': {'R': 1}
        }
    ]
    with pytest.raises(IncorrectComponentInformation):
        load_circuit(test_circuit)