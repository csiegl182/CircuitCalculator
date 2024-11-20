import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot
import pytest
from CircuitCalculator.SimpleSimulation.simulator import simulate
from CircuitCalculator.SimpleSimulation import errors

def test_simulate_raises_missing_argument_error_when_no_element_type_is_defined_in_circuit_elements_definition() -> None:
    _, ax = matplotlib.pyplot.subplots()
    simulation_data = {
        'circuit': {
            'unit': 7,
            'elements': [
                {
                    'no_type': 'unknown_element_type'
                }
            ]
        }
    }
    with pytest.raises(errors.MissingArgument):
        simulate(simulation_data, ax)

def test_simulate_raises_unknown_circuit_element_error_when_element_type_is_unknown() -> None:
    _, ax = matplotlib.pyplot.subplots()
    simulation_data = {
        'circuit': {
            'unit': 7,
            'elements': [
                {
                    'type': 'unknown_element_type'
                }
            ]
        }
    }
    with pytest.raises(errors.UnknownCircuitElement):
        simulate(simulation_data, ax)

def test_when_providing_no_analysis_section_no_error_occurs() -> None:
    simulation_data = {
        "circuit": {
            "unit": 5,
            "elements": [
                {
                    "type": "voltage_source",
                    "V": 1,
                    "name": "Vq",
                },
                {
                    "type": "node",
                    "name": "b",
                    "id_loc": "SE"
                },
                {
                    "type": "line",
                    "direction": "right",
                    "length": 0.5
                },
            ]
        }
    }
    simulate(simulation_data)

def test_when_providing_element_with_insufficient_arguemnts_a_missing_argument_error_is_raised() -> None:
    _, ax = matplotlib.pyplot.subplots()
    simulation_data = {
        "circuit": {
            "unit": 5,
            "elements": [
                {
                    "type": "voltage_source",
                    "name": "Vq",
                    "V_insufficient": 1
                }
            ]
        }
    }
    with pytest.raises(errors.MissingArgument):
        simulate(simulation_data, ax)