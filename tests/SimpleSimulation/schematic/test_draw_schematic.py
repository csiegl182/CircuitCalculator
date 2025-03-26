import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot
import pytest
from CircuitCalculator.SimpleSimulation.schematic import draw_schematic
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
        draw_schematic(simulation_data, ax)

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
        draw_schematic(simulation_data, ax)

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
    draw_schematic(simulation_data)

def test_when_providing_empty_simulation_data_empty_circuit_error_is_raised() -> None:
    _, ax = matplotlib.pyplot.subplots()
    with pytest.raises(errors.EmptyCircuit):
        draw_schematic({}, ax)

def test_when_providing_empty_solution_list_no_error_occurs() -> None:
    _, ax = matplotlib.pyplot.subplots()
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
            ],
            "solution": {
                "type": "none",
                "voltages": [],
                "currents": [],
                "potentials": [],
                "powers": []
            }
        }
    }
    draw_schematic(simulation_data, ax)