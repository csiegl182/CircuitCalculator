from ..network import Network
from .solution import NodalAnalysisSolution
from .state_space_model import NodalStateSpaceModel, BranchValues
from scipy import signal
from typing import Any, Callable
from . import labelmapper as map
import numpy as np
from dataclasses import dataclass, field

@dataclass
class TransientAnalysisSolution(NodalAnalysisSolution):
    source_index_mapper: map.SourceIndexMapper = map.default_source_mapper
    c_values: list[BranchValues] = field(default_factory=list)
    t_lim: tuple[float, float] = (0, 1)
    Ts: float = 1e-3
    input: dict[str, Callable[[np.ndarray], np.ndarray]] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        sources = map.default_source_mapper(self.network)
        ss = NodalStateSpaceModel(network=self.network, c_values=self.c_values, node_index_mapper=self.node_mapper, source_index_mapper=self.source_index_mapper)
        sys = signal.StateSpace(ss.A, ss.B, ss.C, ss.D)
        t = np.arange(self.t_lim[0], self.t_lim[1], self.Ts)
        self.time, self.phi, _ = signal.lsim(sys, np.column_stack([self.input[s](t) for s in sources]), t)

    def get_potential(self, node_id: str) -> Any:
        V_active = np.zeros(shape=self.time.shape)
        if self._super_nodes.is_active(node_id):
            V_active = self._super_nodes.voltage_to_next_reference(node_id)
            node_id = self._super_nodes.non_active_reference_node(node_id)
        if self.network.is_zero_node(node_id):
            return V_active
        return self.phi[:,self._node_mapping[node_id]] + V_active

    def get_current(self, branch_id: str) -> Any:
        return 0

# def transient_analysis_solver(network: Network) -> NetworkSolution:
#     return TransientAnalysisSolution(network)