from .circuit import Circuit, transform, frequency_components
from ..SignalProcessing.types import TimeDomainFunction, FrequencyDomainFunction
from ..Network.NodalAnalysis import nodal_analysis_solver
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

    def get_power(self, component_id: str) -> FrequencyDomainFunction:
        w, voltage = self.get_voltage(component_id)
        _, current = self.get_current(component_id)
        return w, voltage*np.conj(current)