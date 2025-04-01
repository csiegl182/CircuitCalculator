from typing import Any, Callable
from .circuit import Circuit, Component
from .Components import components as cp
from dataclasses import asdict
from .. import dump_load
import functools

class UnidentifiedComponent(Exception):
    ...

class UnknownCircuitComponent(Exception):
    ...

class IncorrectComponentInformation(Exception):
    ...

circuit_component_translators : dict[str, Callable[..., cp.Component]] = {
    "resistor" : cp.resistor,
    "conductance" : cp.conductance,
    "impedance" : cp.impedance,
    "admittance" : cp.admittance,
    "dc_voltage_source" : cp.dc_voltage_source,
    "ac_voltage_source" : cp.ac_voltage_source,
    "complex_voltage_source" : cp.complex_voltage_source,
    "dc_current_source" : cp.dc_current_source,
    "ac_current_source" : cp.ac_current_source,
    "complex_current_source" : cp.complex_current_source
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

def undictify_circuit(circuit: dict) -> Circuit:
    return Circuit([generate_component(entry) for entry in circuit['components']])

deserialize = functools.partial(dump_load.deserialize, dict_preprocessor=undictify_circuit)
load = functools.partial(dump_load.load, deserialize_fcn=deserialize)

def dictify_circuit(circuit: Circuit) -> dict:
    return {'components' : [asdict(c) for c in circuit.components]}

serialize = functools.partial(dump_load.serialize, dict_processor=dictify_circuit)
save = functools.partial(dump_load.dump, dump_fcn=serialize)
