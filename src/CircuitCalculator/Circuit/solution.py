from .circuit import Circuit, transform
from ..Network.NodalAnalysis import nodal_analysis_solver
from ..Network.solution import NetworkSolver
from typing import Callable, List, Union, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import numpy as np

TimeDomainFunction = Callable[[float], List[float]]
FrequencyDomainFunction = Tuple[List[float], List[complex]]
CircuitSolutionValue = Union[
    float,
    complex,
    TimeDomainFunction,
    FrequencyDomainFunction
]

@dataclass
class CircuitSolution(ABC):
    circuit: Circuit
    solver: NetworkSolver = field(default=nodal_analysis_solver)

    @abstractmethod
    def get_voltage(self, id: str) -> CircuitSolutionValue:
        ...

    @abstractmethod
    def get_current(self, id: str) -> CircuitSolutionValue:
        ...

    @abstractmethod
    def get_power(self, id: str) -> CircuitSolutionValue:
        ...

@dataclass
class DCSolution(CircuitSolution):
    def __post_init__(self):
        network = transform(self.circuit, w=[0])[0]
        self._solution = self.solver(network)

    def get_voltage(self, component_id: str) -> complex:
        return self._solution.get_voltage(component_id)

    def get_current(self, component_id: str) -> complex:
        return self._solution.get_current(component_id)

    def get_power(self, component_id: str) -> complex:
        return self._solution.get_power(component_id)

@dataclass
class TimeDomainSolution(CircuitSolution):
    w: List[float] = field(default_factory=list)
    def __post_init__(self):
        if len(self.w) == 0:
            self.w = self.circuit.w
        networks = transform(self.circuit, w=self.w)
        self._solutions = [self.solver(network) for network in networks]

    def get_voltage(self, component_id: str) -> TimeDomainFunction:
        voltages = [solution.get_voltage(component_id) for solution in self._solutions]
        return lambda t: list(np.sum([np.abs(V)*np.cos(w*t+np.angle(V)) for V, w in zip(voltages, self.w)]))

    def get_current(self, component_id: str) -> TimeDomainFunction:
        currents = [solution.get_current(component_id) for solution in self._solutions]
        return lambda t: list(np.sum([np.abs(V)*np.cos(w*t+np.angle(V)) for V, w in zip(currents, self.w)]))

    def get_power(self, component_id: str) -> TimeDomainFunction:
        voltage = self.get_voltage(component_id)
        current = self.get_current(component_id)
        return lambda t: list(np.array(voltage(t))*np.array(current(t)))

@dataclass
class FrequencyDomainSolution(CircuitSolution):
    def __post_init__(self):
        networks = transform(self.circuit, w=self.circuit.w)
        self._solutions = [self.solver(network) for network in networks]

    def get_voltage(self, component_id: str) -> FrequencyDomainFunction:
        voltages = [solution.get_voltage(component_id) for solution in self._solutions]
        return self.circuit.w, voltages

    def get_current(self, component_id: str) -> FrequencyDomainFunction:
        currents = [solution.get_current(component_id) for solution in self._solutions]
        return self.circuit.w, currents

    def get_power(self, component_id: str) -> FrequencyDomainFunction:
        voltage = self.get_voltage(component_id)
        current = self.get_current(component_id)
        return self.circuit.w, list(np.array(voltage)*np.conj(np.array(current)))