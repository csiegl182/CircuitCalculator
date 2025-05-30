from typing import Any, Callable
from .circuit import Circuit, Component
from .Components import components as cp
from .Components import symbolic_components as s_cp
from dataclasses import asdict
from .. import dump_load
import functools

class UnidentifiedComponent(Exception):
    ...

class UnknownCircuitComponent(Exception):
    ...

class IncorrectComponentInformation(Exception):
    ...

def numeric_component_factory(*_, factory_fcn: tuple[Callable[..., cp.Component], Callable[..., cp.Component]], numeric_keys: tuple[str, ...], **kwargs) -> cp.Component:
    def is_numeric(value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False
    numeric_values = [kwargs.get(key, '') for key in numeric_keys]
    if all(is_numeric(value) for value in numeric_values):
        return factory_fcn[0](**kwargs)
    return factory_fcn[1](**kwargs)

circuit_component_translators : dict[str, Callable[..., cp.Component]] = {
    "resistor" : functools.partial(numeric_component_factory, factory_fcn=(cp.resistor, s_cp.resistor), numeric_keys=('R',)),
    "conductance" : functools.partial(numeric_component_factory, factory_fcn=(cp.conductance, s_cp.conductance), numeric_keys=('G',)),
    "impedance" : functools.partial(numeric_component_factory, factory_fcn=(cp.impedance, s_cp.impedance), numeric_keys=('Z',)),
    "admittance" : functools.partial(numeric_component_factory, factory_fcn=(cp.admittance, s_cp.admittance), numeric_keys=('Y',)),
    "dc_voltage_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.dc_voltage_source, s_cp.voltage_source), numeric_keys=('V',)),
    "ac_voltage_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.ac_voltage_source, s_cp.voltage_source), numeric_keys=('V', 'f')),
    "complex_voltage_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.complex_voltage_source, s_cp.voltage_source), numeric_keys=('V',)),
    "dc_current_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.dc_current_source, s_cp.current_source), numeric_keys=('I',)),
    "ac_current_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.ac_current_source, s_cp.current_source), numeric_keys=('I', 'f')),
    "complex_current_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.complex_current_source, s_cp.current_source), numeric_keys=('I',)),
}

def generate_component(component: dict[str, Any]) -> Component:
    component = component.copy()
    try:
        component_id = component['id']
    except KeyError:
        raise UnidentifiedComponent(f'Unidentified component')
    try:
        component_value = component.pop('value', {})
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
    return component_factory(id=component_id, nodes=component_nodes, **component_value)

def undictify_circuit(circuit: dict) -> Circuit:
    return Circuit([generate_component(entry) for entry in circuit['components']])

deserialize = functools.partial(dump_load.deserialize, dict_preprocessor=undictify_circuit)
load = functools.partial(dump_load.load, deserialize_fcn=deserialize)

def dictify_circuit(circuit: Circuit) -> dict:
    return {'components' : [asdict(c) for c in circuit.components]}

serialize = functools.partial(dump_load.serialize, dict_processor=dictify_circuit)
save = functools.partial(dump_load.dump, dump_fcn=serialize)
