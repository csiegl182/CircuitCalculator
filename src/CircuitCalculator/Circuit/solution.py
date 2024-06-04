from .circuit import Circuit, transform, frequency_components
from ..SignalProcessing.types import TimeDomainFunction, FrequencyDomainSeries, TimeDomainSeries, StateSpaceSolver
from ..SignalProcessing.state_space_model import StateSpaceModel, continuous_state_space_solver
from ..Network.NodalAnalysis.bias_point_analysis import nodal_analysis_bias_point_solver
from ..Network.NodalAnalysis.state_space_model import nodal_state_space_model
from ..Network.solution import NetworkSolver
from typing import Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import numpy as np

@dataclass
class CircuitSolution(ABC):
    circuit: Circuit

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
    solver: NetworkSolver = field(default=nodal_analysis_bias_point_solver)

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
    solver: NetworkSolver = field(default=nodal_analysis_bias_point_solver)
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
    solver: NetworkSolver = field(default=nodal_analysis_bias_point_solver)

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
    solver: NetworkSolver = field(default=nodal_analysis_bias_point_solver)

    def __post_init__(self):
        self.w = frequency_components(self.circuit, self.w_max)
        networks = transform(self.circuit, w=self.w)
        self._solutions = [self.solver(network) for network in networks]

    def get_voltage(self, component_id: str) -> FrequencyDomainSeries:
        voltages = np.array([solution.get_voltage(component_id) for solution in self._solutions])
        return np.array(self.w), voltages

    def get_current(self, component_id: str) -> FrequencyDomainSeries:
        currents = np.array([solution.get_current(component_id) for solution in self._solutions])
        return np.array(self.w), currents

    def get_potential(self, node_id: str) -> FrequencyDomainSeries:
        potentials = np.array([solution.get_potential(node_id) for solution in self._solutions])
        return np.array(self.w), potentials

    def get_power(self, component_id: str) -> FrequencyDomainSeries:
        w, voltage = self.get_voltage(component_id)
        _, current = self.get_current(component_id)
        return w, voltage*np.conj(current)


@dataclass
class TransientSolution(CircuitSolution):
    tin: np.ndarray = field(default_factory=lambda : np.empty((0,1)))
    input: dict[str, TimeDomainFunction] = field(default_factory=dict)
    solver: StateSpaceSolver = field(default=continuous_state_space_solver)

    def __post_init__(self):
        network = transform(self.circuit, w=[0])[0]

        C_values = {c.id: float(c.value['C']) for c in self.circuit.components if c.type == 'capacitor'}
        L_values = {c.id: float(c.value['L']) for c in self.circuit.components if c.type == 'inductance'}

        self._ssm = nodal_state_space_model(network, c_values=C_values, l_values=L_values)
        self._u = np.array([self.input[input_id](self.tin) for input_id in self._ssm.sources])
        self._tout, self._x, _ = self.solver(
            StateSpaceModel(A=self._ssm.A, B=self._ssm.B, C=np.eye(self._ssm.A.shape[0]), D=np.zeros((self._ssm.A.shape[0], self._ssm.B.shape[1]))),
            self._u.T,
            self.tin,
            np.zeros((self._ssm.A.shape[0], 1))
        )
        self._x = np.reshape(self._x, (self._x.shape[0], self._ssm.A.shape[0])).T

    @property
    def t(self) -> np.ndarray:
        return self._tout

    def get_potential(self, node_id: str) -> TimeDomainSeries:
        return self._tout, np.reshape(self._ssm.c_row_for_potential(node_id)@self._x + self._ssm.d_row_for_potential(node_id)@self._u, (-1,))

    def get_voltage(self, component_id: str) -> TimeDomainSeries:
        return self._tout, np.reshape(self._ssm.c_row_voltage(component_id)@self._x + self._ssm.d_row_voltage(component_id)@self._u, (-1,))

    def get_current(self, component_id: str) -> TimeDomainSeries:
        return self._tout, np.reshape(self._ssm.c_row_current(component_id)@self._x + self._ssm.d_row_current(component_id)@self._u, (-1,))

    def get_power(self, component_id: str) -> TimeDomainSeries:
        return self._tout, self.get_voltage(component_id)[1]*self.get_current(component_id)[1]
        
        