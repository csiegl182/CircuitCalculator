from CircuitCalculator.Network.NodalAnalysis.label_mapping import LabelMapping, DistinctValues
import pytest

def test_label_mapping_returns_single_values() -> None:
    d = {'a': 1, 'b': 2, 'c': 3}

    label_mapping = LabelMapping(d)

    assert label_mapping['a'] == 1

def test_label_mapping_returns_multiple_values() -> None:
    d = {'a': 1, 'b': 2, 'c': 3}

    label_mapping = LabelMapping(d)

    assert label_mapping('a', 'b', 'c') == (1, 2, 3)

def test_label_mapping_returns_multiple_values_in_different_order() -> None:
    d = {'a': 1, 'b': 2, 'c': 3}

    label_mapping = LabelMapping(d)

    assert label_mapping('c', 'a', 'b') == (3, 1, 2)

def test_label_mapping_returns_key_error_on_single_value() -> None:
    d = {'a': 1, 'b': 2, 'c': 3}

    label_mapping = LabelMapping(d)

    with pytest.raises(KeyError):
        label_mapping['d']

def test_label_mapping_returns_key_error_on_multiple_values() -> None:
    d = {'a': 1, 'b': 2, 'c': 3}

    label_mapping = LabelMapping(d)

    with pytest.raises(KeyError):
        label_mapping('a', 'b', 'c', 'd')

def test_label_mapping_ensures_distinct_values() -> None:
    d = {'a': 1, 'b': 2, 'c': 1}

    with pytest.raises(DistinctValues):
        LabelMapping(d)

def test_label_mapping_returns_all_keys() -> None:
    d = {'a': 1, 'b': 2, 'c': 3}

    label_mapping = LabelMapping(d)

    assert list(label_mapping.keys) == list(d.keys())

def test_label_mappper_returns_number_of_entries() -> None:
    d = {'a': 1, 'b': 2, 'c': 3}

    label_mapping = LabelMapping(d)

    assert label_mapping.N == len(d)

def test_label_mapping_can_iterate_over_the_keys_of_its_mapping() -> None:
    d = {'a': 1, 'b': 2, 'c': 3}

    label_mapping = LabelMapping(d)

    assert [k for k in label_mapping] == list(d.keys())
