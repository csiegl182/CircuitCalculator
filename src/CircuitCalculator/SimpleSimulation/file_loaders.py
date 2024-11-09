from pathlib import Path
import json
import yaml

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

def load_simulation_data(file: str) -> dict:
    suffix = Path(file).suffix
    loader = file_loaders.get(suffix, None)
    if loader is None:
        raise ValueError('File has unknown data format')
    try:
        return loader(file)
    except json.JSONDecodeError or yaml.YAMLError as e:
        raise ValueError(f'Error loading file: {e}')