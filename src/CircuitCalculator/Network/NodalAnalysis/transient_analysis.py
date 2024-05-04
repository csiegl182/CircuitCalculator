from ..network import Network
from ..solution import NetworkSolution
from .state_space_model import NodalStateSpaceModel, BranchValues
from scipy import signal
from typing import Any, Callable
from . import labelmapper as map
import numpy as np

class TransientAnalysisSolution:
    def __init__(self, network : Network, c_values: list[BranchValues], input: dict[str, Callable[[np.ndarray], np.ndarray]], t_lim: tuple[float, float] = (0, 1), Ts: float = 1e-3, node_mapper: map.NodeIndexMapper = map.default_node_mapper) -> None:
        self._network = network
        self._node_mapping = node_mapper(network)
        self._sources = map.default_source_mapper(network)
        ss = NodalStateSpaceModel(network=network, c_values=c_values, node_index_mapper=node_mapper, source_index_mapper=map.default_source_mapper)
        sys = signal.StateSpace(ss.A, ss.B, ss.C, ss.D)
        t = np.arange(t_lim[0], t_lim[1], Ts)
        self._time, self.phi, _ = signal.lsim(sys, np.column_stack([input[s](t) for s in self._sources]), t)

    def get_potential(self, node_id: str) -> Any:
        if self._network.is_zero_node(node_id):
            return np.zeros(self.time.size)
        return self.phi[:,self._node_mapping[node_id]]
    
    def get_voltage(self, branch_id: str) -> Any:
        phi1 = self.get_potential(self._network[branch_id].node1)
        phi2 = self.get_potential(self._network[branch_id].node2)
        return phi1-phi2

    def get_current(self, branch_id: str) -> Any:
        return 0

    def get_power(self, branch_id: str) -> Any:
        return 0

    @property
    def time(self) -> np.ndarray:
        return self._time

# def transient_analysis_solver(network: Network) -> NetworkSolution:
#     return TransientAnalysisSolution(network)