from pathlib import Path
import json
import yaml
import numpy as np

def json_loader(file: str) -> dict:
    with open(file) as f:
        return json.load(f)

def yaml_loader(file: str) -> dict:
    with open(file) as f:
        return yaml.safe_load(f)

file_loaders = {
    '.json': json_loader,
    '.yaml': yaml_loader,
    '.yml': yaml_loader,
}

def dump_complex(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, complex):
            data[key] = {'real': value.real, 'imag': value.imag}
    return data

def restore_complex(data: dict) -> dict:
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

def load(file: str) -> dict:
    suffix = Path(file).suffix
    loader = file_loaders.get(suffix, None)
    if loader is None:
        raise ValueError('File has unknown data format')
    try:
        return loader(file)
    except json.JSONDecodeError or yaml.YAMLError as e:
        raise ValueError(f'Error loading file: {e}')