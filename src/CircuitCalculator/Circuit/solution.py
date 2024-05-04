from .circuit import Circuit, transform, frequency_components
from ..SignalProcessing.types import TimeDomainFunction, FrequencyDomainFunction
from ..Network.NodalAnalysis.node_analysis import nodal_analysis_solver
# from ..Network.NodalAnalysis.state_space_model import create_state_space_input_update_matrix
from ..Network.solution import NetworkSolver
from typing import Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import numpy as np

@dataclass
class CircuitSolution(ABC):
    circuit: Circuit = field(default_factory=lambda : Circuit([]))
    solver: NetworkSolver = field(default=nodal_analysis_solver)

    @abstractmethod
    def get_voltage(self, id: str) -> Any:
        ...

    @abstractmethod
    def get_current(self, id: str) -> Any:
        ...

    @abstractmethod
    def get_potential(self, id: str) -> Any:
        ...

    @abstractmethod
    def get_power(self, id: str) -> Any:
        ...

@dataclass
class DCSolution(CircuitSolution):
    def __post_init__(self):
        network = transform(self.circuit, w=[0])[0]
        self._solution = self.solver(network)

    def get_voltage(self, component_id: str) -> float:
        return self._solution.get_voltage(component_id).real

    def get_current(self, component_id: str) -> float:
        return self._solution.get_current(component_id).real

    def get_potential(self, node_id: str) -> float:
        return self._solution.get_potential(node_id).real

    def get_power(self, component_id: str) -> float:
        return self.get_voltage(component_id)*self.get_current(component_id)

@dataclass
class ComplexSolution(CircuitSolution):
    w: float = 0

    def __post_init__(self):
        network = transform(self.circuit, w=[self.w])[0]
        self._solution = self.solver(network)

    def get_voltage(self, component_id: str) -> complex:
        return self._solution.get_voltage(component_id)

    def get_current(self, component_id: str) -> complex:
        return self._solution.get_current(component_id)

    def get_potential(self, node_id: str) -> complex:
        return self._solution.get_potential(node_id)

    def get_power(self, component_id: str) -> complex:
        return self._solution.get_voltage(component_id)*np.conj(self._solution.get_current(component_id))

@dataclass
class TimeDomainSolution(CircuitSolution):
    w_max: float = field(default=0)
    w: list[float] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.w = frequency_components(self.circuit, self.w_max)
        networks = transform(self.circuit, w=self.w)
        self._solutions = [self.solver(network) for network in networks]

    def get_voltage(self, component_id: str) -> TimeDomainFunction:
        voltages = [solution.get_voltage(component_id) for solution in self._solutions]
        return np.vectorize(lambda t: np.array(np.sum([np.abs(V)*np.cos(w*t+np.angle(V)) for V, w in zip(voltages, self.w)])))

    def get_current(self, component_id: str) -> TimeDomainFunction:
        currents = [solution.get_current(component_id) for solution in self._solutions]
        return np.vectorize(lambda t: np.array(np.sum([np.abs(V)*np.cos(w*t+np.angle(V)) for V, w in zip(currents, self.w)])))

    def get_potential(self, node_id: str) -> TimeDomainFunction:
        potentials = [solution.get_potential(node_id) for solution in self._solutions]
        return np.vectorize(lambda t: np.array(np.sum([np.abs(phi)*np.cos(w*t+np.angle(phi)) for phi, w in zip(potentials, self.w)])))

    def get_power(self, component_id: str) -> TimeDomainFunction:
        voltage = self.get_voltage(component_id)
        current = self.get_current(component_id)
        return lambda t: np.array(voltage(t))*np.array(current(t))

@dataclass
class FrequencyDomainSolution(CircuitSolution):
    w_max: float = field(default=0)

    def __post_init__(self):
        self.w = frequency_components(self.circuit, self.w_max)
        networks = transform(self.circuit, w=self.w)
        self._solutions = [self.solver(network) for network in networks]

    def get_voltage(self, component_id: str) -> FrequencyDomainFunction:
        voltages = np.array([solution.get_voltage(component_id) for solution in self._solutions])
        return np.array(self.w), voltages

    def get_current(self, component_id: str) -> FrequencyDomainFunction:
        currents = np.array([solution.get_current(component_id) for solution in self._solutions])
        return np.array(self.w), currents

    def get_potential(self, node_id: str) -> FrequencyDomainFunction:
        potentials = np.array([solution.get_potential(node_id) for solution in self._solutions])
        return np.array(self.w), potentials

    def get_power(self, component_id: str) -> FrequencyDomainFunction:
        w, voltage = self.get_voltage(component_id)
        _, current = self.get_current(component_id)
        return w, voltage*np.conj(current)

from typing import Callable
from ..Network.NodalAnalysis.state_space_model import BranchValues

# @dataclass
# class TransientSolution(CircuitSolution):
#     t_end: float = 1
#     Ts: float = 0.2
#     t0: float = 0

#     def __post__init__(self):
#         network = transform(self.circuit, w=[0])[0]
#         all_Cs = [c for c in self.circuit.components if c.type == 'capacitor']
#         A, B = create_state_space_input_update_matrix(
#             network=network,
#             Cvalues=[BranchValues(value=float(C.value['C']), node1=C.nodes[0], node2=C.nodes[1]) for C in all_Cs]
#         )
#         from scipy import signal

#         Y = cre

#         sys = signal.StateSpace(A, B, np.eye(A.shape[0]), np.zeros((A.shape[0], B.shape[1])))
#         t = np.arange(self.t0, self.t_end, self.Ts)
#         u = np.column_stack([np.array(t>0.1, dtype=float)])

#         self._tout, self._yout, _ = signal.lsim(sys, u, t)

#     def get_voltage(self, component_id: str) -> TimeDomainFunction:
#         voltages = [solution.get_voltage(component_id) for solution in self._solutions]
#         return np.vectorize(lambda t: np.array(np.sum([np.abs(V)*np.cos(w*t+np.angle(V)) for V, w in zip(voltages, self.w)])))
        
        