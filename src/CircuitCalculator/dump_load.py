from pathlib import Path
import json
import yaml
import yaml.parser, yaml.scanner
import functools


def as_complex(dct):
    if "__complex__" in dct:
        return complex(dct["real"], dct["imag"])
    return dct

def complex_constructor(loader, node):
    value = loader.construct_scalar(node)
    return complex(value)

yaml.SafeLoader.add_constructor("!complex", complex_constructor)

deserializers = {
    'json': functools.partial(json.loads, object_hook=as_complex),
    'yaml': yaml.safe_load,
    'yml': yaml.safe_load
}

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return {'__complex__': True, 'real': obj.real, 'imag': obj.imag}
        return super().default(obj)

def complex_representer(dumper, data):
    return dumper.represent_scalar("!complex", str(data).strip('()'))

yaml.SafeDumper.add_representer(complex, complex_representer)

serializers = {
    'json': functools.partial(json.dumps, cls=JSONEncoder),
    'yaml': functools.partial(yaml.dump, Dumper=yaml.SafeDumper),
    'yml': functools.partial(yaml.dump, Dumper=yaml.SafeDumper)
}

class ParseError(Exception):
    def __init__(self, format: str) -> None:
        super().__init__(f'Cannot parse data as {format}.')
        self.format = format

format_errors : tuple[type[Exception], ...] = (
    json.JSONDecodeError,
    yaml.parser.ParserError,
    yaml.scanner.ScannerError
)

def serialize(data: dict, format: str, **kwargs) -> str:
    serializer = serializers.get(format, None)
    if serializer is None:
        raise ValueError('Unknown data format {format}.')
    return serializer(data, **kwargs)

def dump(file: str, data: dict, **kwargs) -> None:
    file_name = Path(file)
    suffix = file_name.suffix[1:]
    with open(file_name, 'w') as f:
        f.write(serialize(data=data, format=suffix, **kwargs))

def deserialize(data: str, format: str, **kwargs) -> dict:
    deserializer = deserializers.get(format, None)
    if deserializer is None:
        raise ValueError('Unknown data format {format}.')
    try:
        return deserializer(data, **kwargs)
    except format_errors as e:
        raise ParseError(format) from e

def load(file: str, **kwargs) -> dict:
    file_name = Path(file)
    suffix = file_name.suffix[1:]
    with open(file_name) as f:
        return deserialize(data=f.read(), format=suffix, **kwargs)
