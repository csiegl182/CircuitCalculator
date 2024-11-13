from pathlib import Path
import json
import yaml
import numpy as np
from typing import Callable, TypeVar

T = TypeVar('T')

serializers = {
    'json': json.loads,
    'yaml': yaml.safe_load,
    'yml': yaml.safe_load
}

deserializers = {
    'json': json.dumps,
    'yaml': yaml.dump,
    'yml': yaml.dump
}

def dictify_complex_values(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, complex):
            data[key] = {'real': value.real, 'imag': value.imag}
    return data

def undictify_complex_values(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, dict) and sorted(list(value.keys())) == sorted(['real', 'imag']):
            data[key] = complex(value['real'], value['imag'])
        if isinstance(value, dict) and sorted(list(value.keys())) == sorted(['abs', 'phase']):
            if value['abs'] < 0:
                raise ValueError("abs value of '{key}' may not be negative")
            data[key] = value['abs'] * complex(np.cos(value['phase']), np.sin(value['phase']))
        if isinstance(value, dict) and sorted(list(value.keys())) == sorted(['abs', 'phase_deg']):
            if value['abs'] < 0:
                raise ValueError("abs value of '{key}' may not be negative")
            data[key] = value['abs'] * complex(np.cos(value['phase_deg']/180*np.pi), np.sin(value['phase_deg']/180*np.pi))
    return data

def dictify_all_complex_values(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = dictify_all_complex_values(value)
    return data

def undictify_all_complex_values(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = undictify_all_complex_values(value)
        if isinstance(value, list):
            data[key] = [undictify_all_complex_values(v) for v in value]
    return undictify_complex_values(data)

def serialize(data: T, format: str, dict_processor: Callable[[T], dict] = dictify_all_complex_values) -> str:
    deserializer = deserializers.get(format, None)
    if deserializer is None:
        raise ValueError('Unknown data format {format}.')
    return deserializer(dict_processor(data))

def dump(file: str, data: T, dump_fcn: Callable[[T, str], str] = serialize) -> None:
    file_name = Path(file)
    suffix = file_name.suffix[1:]
    with open(file_name, 'w') as f:
        f.write(dump_fcn(data, suffix))

def deserialize(data: str, format: str, dict_preprocessor: Callable[[dict], T] = undictify_all_complex_values) -> T:
    serializer = serializers.get(format, None)
    if serializer is None:
        raise ValueError('Unknown data format {format}.')
    return dict_preprocessor(serializer(data))

def load(file: str, deserialize_fcn: Callable[[str, str], T] = deserialize) -> T:
    file_name = Path(file)
    suffix = file_name.suffix[1:]
    with open(file_name) as f:
        return deserialize_fcn(f.read(), suffix)
