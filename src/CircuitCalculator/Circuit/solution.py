from .circuit import Circuit, transform, frequency_components, transform_symbolic_circuit, transform_circuit
from ..SignalProcessing.types import TimeDomainFunction, FrequencyDomainSeries, TimeDomainSeries, StateSpaceSolver
from ..SignalProcessing.state_space_model import NumericStateSpaceModel, continuous_state_space_solver
from ..Network.NodalAnalysis.bias_point_analysis import nodal_analysis_bias_point_solver, symbolic_nodal_analysis_bias_point_solver
from ..Network.NodalAnalysis.state_space_model import numeric_state_space_model
from .state_space_model import numeric_state_space_model_constructor
from ..Network.solution import NetworkSolver
from typing import Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import numpy as np
import sympy as sp

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
class EmptySolution(CircuitSolution):
    circuit: Circuit = field(default_factory=lambda: Circuit([]))

    def get_voltage(self, _: str) -> Any:
        return None

    def get_current(self, _: str) -> Any:
        return None

    def get_potential(self, _: str) -> Any:
        return None

    def get_power(self, _: str) -> Any:
        return None

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
    peak_values: bool = False

    def __post_init__(self):
        network = transform(self.circuit, w=[self.w], rms=not self.peak_values)[0]
        if self.w == 0:
            self.peak_values = True
        self._solution = self.solver(network)

    def get_voltage(self, component_id: str) -> complex:
        return self._solution.get_voltage(component_id)

    def get_current(self, component_id: str) -> complex:
        return self._solution.get_current(component_id)

    def get_potential(self, node_id: str) -> complex:
        return self._solution.get_potential(node_id)

    def get_power(self, component_id: str) -> complex:
        if self.peak_values:
            return 1/2*self.get_voltage(component_id)*np.conj(self.get_current(component_id))
        return self.get_voltage(component_id)*np.conj(self.get_current(component_id))

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
    one_sided: bool = field(default=True)

    def __post_init__(self):
        self.w = np.array(frequency_components(self.circuit, self.w_max))
        self._solutions = np.array([ComplexSolution(circuit=self.circuit, solver=self.solver, w=w, peak_values=True) for w in self.w])
        if not self.one_sided:
            self.w = np.concatenate((-self.w[-1:0:-1], self.w))
            self._solutions = 1/2*np.concatenate((np.conj(self._solutions[-1:0:-1]), self._solutions))

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
        power = np.array([solution.get_power(component_id) for solution in self._solutions])
        return np.array(self.w), power

@dataclass
class TransientSolution(CircuitSolution):
    tin: np.ndarray = field(default_factory=lambda : np.empty((0,1)))
    input: dict[str, TimeDomainFunction] = field(default_factory=dict)
    solver: StateSpaceSolver = field(default=continuous_state_space_solver)

    def _input_fcn(self, input_id: str) -> TimeDomainFunction:
        try:
            return self.input[input_id]
        except KeyError as e:
            raise KeyError(f'Input element with id "{input_id}" not defined.') from e

    def __post_init__(self):
        self._ssm = numeric_state_space_model_constructor(self.circuit)
        self._u = np.array([self._input_fcn(input_id)(self.tin) for input_id in self._ssm.sources])
        self._tout, self._x, _ = self.solver(
            NumericStateSpaceModel(A=self._ssm.A, B=self._ssm.B, C=np.eye(self._ssm.A.shape[0]), D=np.zeros((self._ssm.A.shape[0], self._ssm.B.shape[1]))),
            self._u.T,
            self.tin,
            np.zeros((self._ssm.A.shape[0], ))
        )
        self._x = np.reshape(self._x, (self._x.shape[0], self._ssm.A.shape[0])).T

    @property
    def t(self) -> np.ndarray:
        return self._tout

    def get_potential(self, node_id: str) -> TimeDomainSeries:
        c, d = self._ssm.c_d_row_for_potential(node_id)
        return self._tout, np.reshape(c@self._x + d@self._u, (-1,))

    def get_voltage(self, component_id: str) -> TimeDomainSeries:
        c, d = self._ssm.c_d_row_for_voltage(component_id)
        return self._tout, np.reshape(c@self._x + d@self._u, (-1,))

    def get_current(self, component_id: str) -> TimeDomainSeries:
        c, d = self._ssm.c_d_row_for_current(component_id)
        return self._tout, np.reshape(c@self._x + d@self._u, (-1,))

    def get_power(self, component_id: str) -> TimeDomainSeries:
        return self._tout, self.get_voltage(component_id)[1]*self.get_current(component_id)[1]

@dataclass
class SymbolicSolution(CircuitSolution):
    solver: NetworkSolver = field(default=symbolic_nodal_analysis_bias_point_solver)
    s: sp.Symbol = sp.Symbol('s', complex=True)

    def __post_init__(self):
        network = transform_symbolic_circuit(self.circuit, s=self.s)
        self._solution = self.solver(network)

    def get_voltage(self, component_id: str) -> Any:
        return self._solution.get_voltage(component_id).simplify().nsimplify()

    def get_current(self, component_id: str) -> Any:
        return self._solution.get_current(component_id).simplify().nsimplify()

    def get_potential(self, node_id: str) -> Any:
        return self._solution.get_potential(node_id).simplify().nsimplify()

    def get_power(self, component_id: str) -> Any:
        return (self.get_voltage(component_id)*self.get_current(component_id)).simplify().nsimplify()
        
        