from CircuitCalculator.Network.NodalAnalysis.label_mapping import LabelMapping
import pytest

def test_label_mapper_returns_filtered_object() -> None:
    lm = LabelMapping({'a': 1, 'b': 2, 'c': 3})

    filtered_label_mapper = lm.filter_keys(lambda x: x > 'a')

    with pytest.raises(KeyError):
        filtered_label_mapper['a']
    assert filtered_label_mapper['b'] == 2
    assert filtered_label_mapper['c'] == 3