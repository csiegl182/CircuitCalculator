import pytest
from CircuitCalculator.Circuit.dump_load import undictify_circuit, UnknownCircuitComponent, IncorrectComponentInformation, UnidentifiedComponent

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



def test_passing_additional_arguments_to_circuit_components_does_not_lead_to_error() -> None:
    test_circuit = {
        "components": [
            {
                "type": "dc_voltage_source",
                "id": "Vs",
                "nodes": [ "a", "b" ],
                "value": {
                    "V": 1,
                    "I": -0.01,
                    "P": -0.01,
                    "phi1": 0,
                    "phi2": -1
                }
            },
            {
                "type": "resistor",
                "id": "R",
                "nodes": [ "a", "b"
                ],
                "value": {
                    "R": 100,
                    "V": 1,
                    "I": 0.01,
                    "P": 0.01,
                    "phi1": 0,
                    "phi2": -1
                }
            }
        ]
    }
    circuit = undictify_circuit(test_circuit)
    assert circuit.components[0].type == test_circuit['components'][0]['type']
    assert circuit.components[1].type == test_circuit['components'][1]['type']