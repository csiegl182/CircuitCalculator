from typing import Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from ..network import Network
from . import label_mapping as map

@dataclass
class NodalAnalysisSolution(ABC):
    network: Network
    node_mapper: map.NetworkMapper = map.default_node_mapper
    current_source_mapper: map.SourceIndexMapper = map.alphabetic_current_source_mapper
    voltage_source_mapper: map.SourceIndexMapper = map.alphabetic_voltage_source_mapper

    @property
    def _node_mapping(self) -> map.LabelMapping:
        return self.node_mapper(self.network)

    @property
    def _current_source_mapping(self) -> map.LabelMapping:
        return self.current_source_mapper(self.network)

    @property
    def _voltage_source_mapping(self) -> map.LabelMapping:
        return self.voltage_source_mapper(self.network)

    @abstractmethod
    def get_potential(self, node_id: str) -> Any:
        ...

    @abstractmethod
    def get_current(self, branch_id: str) -> Any:
        ...

    def get_voltage(self, branch_id: str) -> Any:
        phi1 = self.get_potential(self.network[branch_id].node1)
        phi2 = self.get_potential(self.network[branch_id].node2)
        return phi1-phi2

    def get_power(self, branch_id: str) -> Any:
        return self.get_voltage(branch_id)*self.get_current(branch_id).conjugate()