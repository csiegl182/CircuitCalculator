from typing import Any, Callable
from .circuit import Circuit, Component
from . import components as ccp
from dataclasses import asdict
import json

class UnidentifiedComponent(Exception):
    ...

class UnknownCircuitComponent(Exception):
    ...

class IncorrectComponentInformation(Exception):
    ...

circuit_component_translators : dict[str, Callable[..., ccp.Component]] = {
    "resistor" : ccp.resistor,
    "conductance" : ccp.conductance,
    "impedance" : ccp.impedance,
    "admittance" : ccp.admittance,
    "dc_voltage_source" : ccp.dc_voltage_source,
    "ac_voltage_source" : ccp.ac_voltage_source,
    "complex_voltage_source" : ccp.complex_voltage_source,
    "dc_current_source" : ccp.dc_current_source,
    "ac_current_source" : ccp.ac_current_source,
    "complex_current_source" : ccp.complex_current_source
}

def generate_component(component: dict[str, Any]) -> Component:
    component = component.copy()
    try:
        component_id = component['id']
    except KeyError:
        raise UnidentifiedComponent(f'Unidentified component')
    try:
        component_value = component.pop('value')
    except KeyError:
        raise IncorrectComponentInformation(f"Missing value of component '{component_id}'.")
    try:
        component_type = component.pop('type')
    except KeyError:
        raise IncorrectComponentInformation(f"Missing type information of component '{component_id}'.")
    try:
        component_nodes = component['nodes']
    except KeyError:
        raise IncorrectComponentInformation(f"Missing node information of component '{component_id}'.")
    try:
        component_factory = circuit_component_translators[component_type]
    except KeyError:
        raise UnknownCircuitComponent(f"Unknown type '{component_type}' of component '{component_id}' is unknown.")
    try:
        return component_factory(id=component_id, nodes=component_nodes, **component_value)
    except TypeError:
        raise IncorrectComponentInformation(f"Given value information for component '{component_id}' of type '{component_type}' is incorrect: '{component_value}'")

def load_circuit(circuit_dict: list[dict[str, Any]]) -> Circuit:
    return Circuit([generate_component(entry) for entry in circuit_dict])

def dump_circuit(circuit: Circuit) -> list[dict[str, Any]]:
    return [asdict(c) for c in circuit.components]

def load_circuit_from_json(filename: str) -> Circuit:
    with open(filename, 'r') as json_file:
        circuit_dict = json.load(json_file)
    return load_circuit(circuit_dict)

def dump_circuit_to_json(circuit: Circuit, filename: str) -> None:
    with open(filename, 'w') as json_file:
        json.dump(dump_circuit(circuit), json_file)