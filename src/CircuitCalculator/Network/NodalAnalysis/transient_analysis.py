from ..network import Network
from ..elements import is_ideal_voltage_source, is_ideal_current_source
from .solution import NodalAnalysisSolution
from .state_space_model import NodalStateSpaceModel, BranchValues
from scipy import signal
from typing import Any, Callable
from . import label_mapping as map
import numpy as np
from dataclasses import dataclass, field
from .supernodes import SuperNodes

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
        self.time, self.phi, self.x = signal.lsim(sys, np.column_stack([self.input[s](t) for s in sources]), t)
        self.i_c = (self.x*ss.A+ss.B*self.input[sources[0]](t))*self.c_values[0].value

    def get_potential(self, node_id: str) -> Any:
        V_active = np.zeros(shape=self.time.shape)
        if self._super_nodes.is_active(node_id):
            V_active = voltage_to_next_reference(self.network, SuperNodes(self.network), node_id, {k: self.input[k](self.time) for k in self.input})
            node_id = self._super_nodes.non_active_reference_node(node_id)
        if self.network.is_zero_node(node_id):
            return V_active
        return self.phi[:,self._node_mapping[node_id]] + V_active

    def get_current(self, branch_id: str) -> Any:
        branch = self.network[branch_id]
        if is_ideal_current_source(branch.element):
            return self.input[branch_id](self.time)
        if branch.id in [c.id for c in self.c_values]:
            return self.i_c
        return self.get_voltage(branch_id)/branch.element.Z
        if is_ideal_voltage_source(branch.element):
            Z = element_impedance(self.network, branch_id)
            I_branch_element = -branch.element.V/Z
            I_other_elements = short_circuit_current(
                trf.remove_element(self.network, branch_id),
                branch.node1,
                branch.node2)
            return  I_branch_element+I_other_elements
        if is_voltage_source(branch.element):
            return -(self.get_voltage(branch_id)+branch.element.V)/branch.element.Z
        return self.get_voltage(branch_id)/branch.element.Z

def voltage_to_next_reference(network: Network, super_nodes: SuperNodes, active_node: str, input: dict[str, np.ndarray]) -> Any:
    def voltage_between(node1: str, node2: str) -> str:
        branches = network.branches_between(node1, node2)
        voltage_sources = [b for b in branches if is_ideal_voltage_source(b.element)]
        if len(voltage_sources) != 1:
            raise Exception
        return voltage_sources[0].id
    voltage_source_node_pairs = zip(super_nodes.nodes_to_non_active_reference_node(active_node)[:-1], super_nodes.nodes_to_non_active_reference_node(active_node)[1:])
    return sum([input[voltage_between(n1, n2)] for n1, n2 in voltage_source_node_pairs])

# def transient_analysis_solver(network: Network) -> NetworkSolution:
#     return TransientAnalysisSolution(network)