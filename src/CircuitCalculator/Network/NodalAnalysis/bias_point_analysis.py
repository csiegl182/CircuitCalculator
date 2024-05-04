from . import labelmapper as map
from .node_analysis import calculate_node_voltages, create_current_vector_from_network, create_node_matrix_from_network, element_impedance, open_circuit_impedance
from .supernodes import SuperNodes
from .. import transformers as trf
from ..elements import is_ideal_current_source, is_ideal_voltage_source, is_voltage_source
from ..network import Network
from ..solution import NetworkSolution
from .solution import NodalAnalysisSolution
import numpy as np
from dataclasses import dataclass

@dataclass
class NodalAnalysisBiasPointSolution(NodalAnalysisSolution):
    node_mapper: map.NodeIndexMapper = map.default_node_mapper

    def __post_init__(self) -> None:
        Y = create_node_matrix_from_network(self.network, node_index_mapper=self.node_mapper)
        I = create_current_vector_from_network(self.network, node_index_mapper=self.node_mapper)
        try:
            self._solution_vector = calculate_node_voltages(Y, I)
        except np.linalg.LinAlgError:
            self._solution_vector = np.zeros(np.size(I))
        if np.any(np.isnan(self._solution_vector)):
            self._solution_vector = np.zeros(np.size(I))

    @property
    def _super_nodes(self) -> SuperNodes:
        return SuperNodes(self.network)

    @property
    def _node_mapping(self) -> dict[str, int]:
        return self.node_mapper(self.network)

    def _select_active_node(self, branch_id: str) -> str:
        branch = self.network[branch_id]
        if self._super_nodes.is_active(branch.node1):
            return branch.node1
        return branch.node2

    def get_potential(self, node_id: str) -> complex:
        V_active = 0+0j
        if self._super_nodes.is_active(node_id):
            V_active = self._super_nodes.voltage_to_next_reference(node_id)
            node_id = self._super_nodes.next_reference(node_id)
        if self.network.is_zero_node(node_id):
            return V_active
        return self._solution_vector[self._node_mapping[node_id]] + V_active

    def get_current(self, branch_id: str) -> complex:
        branch = self.network[branch_id]
        if is_ideal_current_source(branch.element):
            return branch.element.I
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

def open_circuit_voltage(network: Network, node1: str, node2: str) -> complex:
    solution = NodalAnalysisBiasPointSolution(network)
    if node1 == node2:
        return 0
    phi1 = solution.get_potential(node_id=node1)
    phi2 = solution.get_potential(node_id=node2)
    return phi1-phi2

def short_circuit_current(network: Network, node1: str, node2: str) -> complex:
    Z = open_circuit_impedance(network, node1, node2)
    V = open_circuit_voltage(network, node1, node2)
    return V/Z

def nodal_analysis_bias_point_solver(network: Network) -> NetworkSolution:
    return NodalAnalysisBiasPointSolution(network)