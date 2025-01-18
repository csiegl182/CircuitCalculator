from pathlib import Path
import json
import yaml
import yaml.parser, yaml.scanner
import re
import numpy as np
from typing import Callable, TypeVar

T = TypeVar('T')

# Define a custom constructor for scientific notation
def scientific_notation_constructor(loader, node):
    value = loader.construct_scalar(node)
    try:
        return float(value)
    except ValueError:
        return value

# Add the custom constructor to the SafeLoader
yaml.SafeLoader.add_implicit_resolver(
    'tag:yaml.org,2002:float',
    re.compile(r'''^(?:[-+]?(?:[0-9][0-9_]*(?:\.[0-9_]*)?|\.[0-9_]+)(?:[eE][-+]?[0-9]+)?)$'''),
    list('-+0123456789.')
)
yaml.SafeLoader.add_constructor('tag:yaml.org,2002:float', scientific_notation_constructor)

deserializers = {
    'json': json.loads,
    'yaml': yaml.safe_load,
    'yml': yaml.safe_load
}

serializers = {
    'json': json.dumps,
    'yaml': yaml.dump,
    'yml': yaml.dump
}

class FormatError(Exception):
    def __init__(self, format: str) -> None:
        super().__init__(f'Cannot parse data as {format}.')
        self.format = format

format_errors : tuple[type[Exception], ...] = (
    json.JSONDecodeError,
    yaml.parser.ParserError,
    yaml.scanner.ScannerError
)

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
            phase_rad = np.deg2rad(value['phase_deg'])
            data[key] = value['abs'] * complex(np.cos(phase_rad), np.sin(phase_rad))
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
    serializer = serializers.get(format, None)
    if serializer is None:
        raise ValueError('Unknown data format {format}.')
    return serializer(dict_processor(data))

def dump(file: str, data: T, dump_fcn: Callable[[T, str], str] = serialize) -> None:
    file_name = Path(file)
    suffix = file_name.suffix[1:]
    with open(file_name, 'w') as f:
        f.write(dump_fcn(data, suffix))

def deserialize(data: str, format: str, dict_preprocessor: Callable[[dict], T] = undictify_all_complex_values) -> T:
    deserializer = deserializers.get(format, None)
    if deserializer is None:
        raise ValueError('Unknown data format {format}.')
    try:
        return dict_preprocessor(deserializer(data))
    except format_errors as e:
        raise FormatError(format) from e

def load(file: str, deserialize_fcn: Callable[[str, str], T] = deserialize) -> T:
    file_name = Path(file)
    suffix = file_name.suffix[1:]
    with open(file_name) as f:
        return deserialize_fcn(f.read(), suffix)
