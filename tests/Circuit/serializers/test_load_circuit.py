import pytest
from CircuitCalculator.Circuit.serializers import undictify_circuit, UnknownCircuitComponent, IncorrectComponentInformation, UnidentifiedComponent

def test_circuit_can_be_loaded_from_dict() -> None:
    test_circuit = { 'components':
        [
            {
                'type': 'dc_voltage_source',
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
    }
    circuit = undictify_circuit(test_circuit)
    assert circuit.components[0].type == test_circuit['components'][0]['type']
    assert circuit.components[1].type == test_circuit['components'][1]['type']

def test_undefined_component_type_leads_to_error() -> None:
    test_circuit = { 'components' :
        [
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
    }
    with pytest.raises(UnknownCircuitComponent):
        undictify_circuit(test_circuit)

def test_missing_component_type_leads_to_error() -> None:
    test_circuit = { 'components' : 
        [
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
    }
    with pytest.raises(IncorrectComponentInformation):
        undictify_circuit(test_circuit)

def test_missing_component_id_leads_to_error() -> None:
    test_circuit = { 'components' : 
        [
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
    }
    with pytest.raises(UnidentifiedComponent):
        undictify_circuit(test_circuit)

def test_odd_value_information_leads_to_error() -> None:
    test_circuit = { 'components' :
        [
            {
                'type': 'dc_voltage_source',
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
    }
    with pytest.raises(IncorrectComponentInformation):
        undictify_circuit(test_circuit)