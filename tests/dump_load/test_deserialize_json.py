from CircuitCalculator.dump_load import deserialize, ParseError
import pytest
import json

def test_deserialize_strings_from_json() -> None:
    data = {
        'a': 'hello',
        'b': 'world'
    }
    serialized = json.dumps(data)
    loaded = deserialize(serialized, 'json')
    assert data == loaded

def test_deserialize_numbers_from_json() -> None:
    data = {
        'a': 1,
        'b': 2.5,
        'c': -3
    }
    serialized = json.dumps(data)
    loaded = deserialize(serialized, 'json')
    assert data == loaded

def test_deserialize_booleans_from_json() -> None:
    data = {
        'a': True,
        'b': False
    }
    serialized = json.dumps(data)
    loaded = deserialize(serialized, 'json')
    assert data == loaded

def test_deserialize_complex_numbers_from_json() -> None:
    a, b, c = 1 + 2j, -3 - 4j, 0 + 0j
    data = {
        'a': {'__complex__': True, 'real': a.real, 'imag': a.imag},
        'b': {'__complex__': True, 'real': b.real, 'imag': b.imag},
        'c': {'__complex__': True, 'real': c.real, 'imag': c.imag}
    }
    serialized = json.dumps(data, cls=json.JSONEncoder)
    loaded = deserialize(serialized, 'json')
    assert loaded['a'] == a
    assert loaded['b'] == b
    assert loaded['c'] == c

def test_deserialize_nested_dicts_from_json() -> None:
    data = {
        'a': {
            'b': {
                'c': 7.34,
                'd': 'test'
            }
        }
    }
    serialized = json.dumps(data, cls=json.JSONEncoder)
    loaded = deserialize(serialized, 'json')
    assert data['a']['b']['c'] == loaded['a']['b']['c']

def test_deserialize_nested_lists_from_json() -> None:
    data = {
        'a': [1, 2, 3],
        'b': ['hello', 'world', '!']
    }
    serialized = json.dumps(data, cls=json.JSONEncoder)
    loaded = deserialize(serialized, 'json')
    assert data['a'] == loaded['a']
    assert data['b'] == loaded['b']

def test_deserialize_empty_dict() -> None:
    data = {}
    serialized = json.dumps(data)
    loaded = deserialize(serialized, 'json')
    assert data == loaded

def test_deserialize_invalid_json_raises_format_error() -> None:
    invalid_json = '{"a": 1, "b": 2'  # Missing closing brace
    with pytest.raises(ParseError):
        deserialize(invalid_json, 'json')

def test_deserialize_unknown_format_raises_value_error() -> None:
    data = '{"a": 1, "b": 2}'
    with pytest.raises(ValueError):
        deserialize(data, 'xml')