from pathlib import Path
import json
import yaml
import numpy as np

serializers = {
    'json': json.loads,
    'yaml': yaml.safe_load,
    'yml': yaml.safe_load
}

def dump_complex_value(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, complex):
            data[key] = {'real': value.real, 'imag': value.imag}
    return data

def restore_complex_value(data: dict) -> dict:
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

def dump_complex_values(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = dump_complex_values(value)
    return data

def restore_complex_values(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = restore_complex_values(value)
        if isinstance(value, list):
            data[key] = [restore_complex_values(v) for v in value]
    return restore_complex_value(data)

def restore(data: str, format: str) -> dict:
    restorer = serializers.get(format, None)
    if restorer is None:
        raise ValueError('Unknown data format {format}.')
    return restore_complex_values(restorer(data))

def load(file: str) -> dict:
    file_name = Path(file)
    suffix = file_name.suffix[1:]
    with open(file_name) as f:
        return restore(f.read(), suffix)
