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

def numeric_component_factory(*_, factory_fcn: tuple[Callable[..., cp.Component], Callable[..., cp.Component]], numeric_keys: dict[str, type], **kwargs) -> cp.Component:
    def is_numeric(value: str) -> bool:
        try:
            complex(value)
            return True
        except ValueError:
            return False
    def probe_conversion(value: Any, target_type: type) -> Any:
        try:
            value = value.replace(' ', '').replace('\t', '')
        except AttributeError:
            pass
        try:
            return target_type(value)
        except (ValueError, TypeError):
            return value
    for key in numeric_keys.keys():
        kwargs[key] = probe_conversion(kwargs[key], numeric_keys[key])
    values = [kwargs[key] for key in numeric_keys]
    if all(is_numeric(value) for value in values):
        return factory_fcn[0](**kwargs)
    return factory_fcn[1](**kwargs)

circuit_component_translators : dict[str, Callable[..., cp.Component]] = {
    "resistor" : functools.partial(numeric_component_factory, factory_fcn=(cp.resistor, s_cp.resistor), numeric_keys={'R': float}),
    "conductance" : functools.partial(numeric_component_factory, factory_fcn=(cp.conductance, s_cp.conductance), numeric_keys={'G': float}),
    "impedance" : functools.partial(numeric_component_factory, factory_fcn=(cp.impedance, s_cp.impedance), numeric_keys={'Z': float}),
    "admittance" : functools.partial(numeric_component_factory, factory_fcn=(cp.admittance, s_cp.admittance), numeric_keys={'Y': float}),
    "dc_voltage_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.dc_voltage_source, s_cp.voltage_source), numeric_keys={'V': float}),
    "ac_voltage_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.ac_voltage_source, s_cp.voltage_source), numeric_keys={'V': float,  'f': float}),
    "open_circuit" : functools.partial(numeric_component_factory, factory_fcn=(cp.open_circuit, s_cp.open_circuit), numeric_keys={}),
    "short_circuit" : functools.partial(numeric_component_factory, factory_fcn=(cp.short_circuit, s_cp.short_circuit), numeric_keys={}),
    "complex_voltage_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.complex_voltage_source, s_cp.voltage_source), numeric_keys={'V': complex}),
    "dc_current_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.dc_current_source, s_cp.current_source), numeric_keys={'I': float}),
    "ac_current_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.ac_current_source, s_cp.current_source), numeric_keys={'I': float, 'f': float}),
    "complex_current_source" : functools.partial(numeric_component_factory, factory_fcn=(cp.complex_current_source, s_cp.current_source), numeric_keys={'I': complex})
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
    try:
        return component_factory(id=component_id, nodes=component_nodes, **component_value)
    except KeyError as e:
        raise IncorrectComponentInformation(f"Missing information '{e.args[0]}' for component '{component_id}' of type '{component_type}'.") from e

def undictify_circuit(circuit: dict) -> Circuit:
    return Circuit([generate_component(entry) for entry in circuit['components']], ground_node=circuit.get('ground_node', ''))

deserialize = functools.partial(dump_load.deserialize, dict_preprocessor=undictify_circuit)
load = functools.partial(dump_load.load, deserialize_fcn=deserialize)

def dictify_circuit(circuit: Circuit) -> dict:
    return {'components' : [asdict(c) for c in circuit.components], 'ground_node' : circuit.ground_node}

serialize = functools.partial(dump_load.serialize, dict_processor=dictify_circuit)
save = functools.partial(dump_load.dump, dump_fcn=serialize)
