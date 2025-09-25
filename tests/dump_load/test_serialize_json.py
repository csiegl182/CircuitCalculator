from CircuitCalculator.dump_load import serialize
import json

def test_dict_with_strings_can_be_serialized_to_json() -> None:
    data = {
        'a': 'hello',
        'b': 'world'
    }
    serialized = serialize(data, 'json')
    loaded = json.loads(serialized)
    assert data == loaded

def test_dict_with_numbers_can_be_serialized_to_json() -> None:
    data = {
        'a': 1,
        'b': 2.5,
        'c': -3
    }
    serialized = serialize(data, 'json')
    loaded = json.loads(serialized)
    assert data == loaded

def test_dict_with_booleans_can_be_serialized_to_json() -> None:
    data = {
        'a': True,
        'b': False
    }
    serialized = serialize(data, 'json')
    loaded = json.loads(serialized)
    assert data == loaded


def test_dict_with_complex_numbers_can_be_serialized_to_json() -> None:
    data = {
        'a': 1 + 2j,
        'b': -3 - 4j,
        'c': 0 + 0j
    }
    serialized = serialize(data, 'json')
    loaded = json.loads(serialized)
    assert loaded['a']['real'] == data['a'].real
    assert loaded['a']['imag'] == data['a'].imag
    assert loaded['b']['real'] == data['b'].real
    assert loaded['b']['imag'] == data['b'].imag
    assert loaded['c']['real'] == data['c'].real
    assert loaded['c']['imag'] == data['c'].imag

def test_dict_with_nested_dicts_can_be_serialized_to_json() -> None:
    data = {
        'a': {
            'b': {
                'c': 1 + 2j
            }
        }
    }
    serialized = serialize(data, 'json')
    loaded = json.loads(serialized)
    assert loaded['a']['b']['c']['real'] == data['a']['b']['c'].real
    assert loaded['a']['b']['c']['imag'] == data['a']['b']['c'].imag

def test_dict_with_lists_can_be_serialized_to_json() -> None:
    data = {
        'a': [1, 2, 3],
        'b': [1 + 2j, 3 + 4j]
    }
    serialized = serialize(data, 'json')
    loaded = json.loads(serialized)
    assert data['a'] == loaded['a']
    assert loaded['b'][0]['real'] == data['b'][0].real
    assert loaded['b'][0]['imag'] == data['b'][0].imag
    assert loaded['b'][1]['real'] == data['b'][1].real
    assert loaded['b'][1]['imag'] == data['b'][1].imag
