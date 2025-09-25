from CircuitCalculator.dump_load import serialize, deserialize

def test_dict_with_strings_can_be_de_serialized_to_and_from_yaml() -> None:
    data = {
        'a': 'hello',
        'b': 'world'
    }
    serialized = serialize(data, 'yaml')
    loaded = deserialize(serialized, 'yaml')
    assert data == loaded

def test_dict_with_numbers_can_be_de_serialized_to_and_from_yaml() -> None:
    data = {
        'a': 1,
        'b': 2.5,
        'c': -3
    }
    serialized = serialize(data, 'yaml')
    loaded = deserialize(serialized, 'yaml')
    assert data == loaded

def test_dict_with_booleans_can_be_de_serialized_to_and_from_yaml() -> None:
    data = {
        'a': True,
        'b': False
    }
    serialized = serialize(data, 'yaml')
    loaded = deserialize(serialized, 'yaml')
    assert data == loaded


def test_dict_with_complex_numbers_can_be_de_serialized_to_and_from_yaml() -> None:
    data = {
        'a': 1 + 2j,
        'b': -3 - 4j,
        'c': 0 + 0j
    }
    serialized = serialize(data, 'yaml')
    loaded = deserialize(serialized, 'yaml')
    assert loaded['a'] == data['a']
    assert loaded['b'] == data['b']
    assert loaded['c'] == data['c']

def test_dict_with_nested_dicts_can_be_de_serialized_to_and_from_yaml() -> None:
    data = {
        'a': {
            'b': {
                'c': 'jklda',
                'd': 1.32
            }
        }
    }
    serialized = serialize(data, 'yaml')
    loaded = deserialize(serialized, 'yaml')
    assert loaded['a']['b']['c'] == data['a']['b']['c']
    assert loaded['a']['b']['d'] == data['a']['b']['d']

def test_dict_with_lists_can_be_de_serialized_to_and_from_yaml() -> None:
    data = {
        'a': [1, 2, 3],
        'b': ['hello', 'world', '!'],
    }
    serialized = serialize(data, 'yaml')
    loaded = deserialize(serialized, 'yaml')
    assert data['a'] == loaded['a']
    assert loaded['b'][0] == data['b'][0]
    assert loaded['b'][0] == data['b'][0]
    assert loaded['b'][1] == data['b'][1]
    assert loaded['b'][1] == data['b'][1]
