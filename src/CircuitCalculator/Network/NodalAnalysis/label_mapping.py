from typing import Callable
from dataclasses import dataclass
from ..network import Network

class DistinctValues(Exception):
    ...

@dataclass(frozen=True)
class LabelMapping:
    mapping: dict[str, int]

    def __post_init__(self) -> None:
        if len(set(self.mapping.values())) != len(self.mapping):
            raise DistinctValues

    def __getitem__(self, label: str) -> int:
        return self.mapping[label]

    def __call__(self, *labels: str) -> tuple[int, ...]:
        return tuple(self[label] for label in labels)

    def filter_keys(self, filter_fcn: Callable[[str], bool]) -> "LabelMapping":
        return LabelMapping({k: self.mapping[k] for k in self.mapping.keys() if filter_fcn(k)})

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

def alphabetic_node_mapper(network: Network) -> LabelMapping:
    node_labels_without_zero = [label for label in sorted(network.node_labels) if label != network.reference_node_label] 
    return LabelMapping({k: v for v, k in enumerate(node_labels_without_zero)})

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

LabelMapper = Callable[[Network], LabelMapping]

@dataclass(frozen=True)
class NetworkLabelMappings:
    network: Network
    node_mapper: LabelMapper
    source_mapper: LabelMapper
    current_source_mapper: LabelMapper
    voltage_source_mapper: LabelMapper

    @property
    def node_mapping(self) -> LabelMapping:
        return self.node_mapper(self.network)

    @property
    def source_mapping(self) -> LabelMapping:
        return self.source_mapper(self.network)

    @property
    def current_source_mapping(self) -> LabelMapping:
        return self.current_source_mapper(self.network)

    @property
    def voltage_source_mapping(self) -> LabelMapping:
        return self.voltage_source_mapper(self.network)

LabelMappingsFactory = Callable[[Network], NetworkLabelMappings]

def default_label_mappings_factory(network: Network) -> NetworkLabelMappings:
    return NetworkLabelMappings(
        network=network,
        node_mapper=alphabetic_node_mapper,
        source_mapper = alphabetic_source_mapper,
        current_source_mapper=alphabetic_current_source_mapper,
        voltage_source_mapper=alphabetic_voltage_source_mapper
    )