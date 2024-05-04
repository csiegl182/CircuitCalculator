from CircuitCalculator.Network.NodalAnalysis.labelmapper import LabelMapping, filter_mapping
import pytest

def test_label_mapper_returns_filtered_object() -> None:
    d = {'a': 1, 'b': 2, 'c': 3}

    filtered_label_mapper = filter_mapping(LabelMapping(d), lambda x: x > 'a')

    with pytest.raises(KeyError):
        filtered_label_mapper['a']
    assert filtered_label_mapper['b'] == 2
    assert filtered_label_mapper['c'] == 3