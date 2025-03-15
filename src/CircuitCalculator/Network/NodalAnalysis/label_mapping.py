from typing import Callable
from dataclasses import dataclass
from ..network import Network

class DistinctValues(Exception):
    ...

@dataclass
class LabelMapping:
    mapping: dict[str, int]

    def __post_init__(self) -> None:
        if len(set(self.mapping.values())) != len(self.mapping):
            raise DistinctValues

    def __getitem__(self, label: str) -> int:
        return self.mapping[label]

    def __call__(self, *labels: str) -> tuple[int, ...]:
        return tuple(self[label] for label in labels)

    @property
    def keys(self) -> list[str]:
        return list(self.mapping.keys())

    @property
    def values(self) -> list[int]:
        return list(self.mapping.values())

    @property
    def N(self) -> int:
        return len(self.mapping)

    def __iter__(self):
        return iter(self.mapping.keys())

def filter(mapping: LabelMapping, filter_fcn: Callable[[str], bool]) -> LabelMapping:
    return LabelMapping({k: mapping[k] for k in mapping.keys if filter_fcn(k)})
    

NetworkMapper = Callable[[Network], LabelMapping]
SourceIndexMapper = Callable[[Network], LabelMapping]

def alphabetic_node_mapper(network: Network) -> LabelMapping:
    node_labels_without_zero = [label for label in sorted(network.node_labels) if label != network.node_zero_label] 
    return LabelMapping({k: v for v, k in enumerate(node_labels_without_zero)})

default_node_mapper = alphabetic_node_mapper

def alphabetic_source_mapper(network: Network) -> LabelMapping:
    current_source_labels = [b.id for b in network.branches if b.element.is_current_source]
    voltage_source_labels = [b.id for b in network.branches if b.element.is_ideal_voltage_source]
    sorted_soruce_labels = sorted(current_source_labels+voltage_source_labels)
    return LabelMapping({k: v for v, k in enumerate(sorted_soruce_labels)})

def alphabetic_current_source_mapper(network: Network) -> LabelMapping:
    current_source_labels = sorted([b.id for b in network.branches if b.element.is_current_source])
    return LabelMapping({k: v for v, k in enumerate(current_source_labels)})

def alphabetic_voltage_source_mapper(network: Network) -> LabelMapping:
    voltage_source_labels = sorted([b.id for b in network.branches if b.element.is_ideal_voltage_source])
    return LabelMapping({k: v for v, k in enumerate(voltage_source_labels)})

default_source_mapper = alphabetic_source_mapper