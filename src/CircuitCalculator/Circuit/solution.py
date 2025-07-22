from .circuit import Circuit, transform, frequency_components, transform_symbolic_circuit
from ..SignalProcessing.types import TimeDomainFunction, FrequencyDomainSeries, TimeDomainSeries
from ..SignalProcessing.state_space_model import NumericStateSpaceModel, continuous_state_space_solver
from ..Network.NodalAnalysis.solution import numeric_nodal_analysis_bias_point_solution, symbolic_nodal_analysis_bias_point_solution
from .state_space_model import numeric_state_space_model_constructor, StateSpaceMatrixConstructor
from ..Network.solution import NetworkSolution, NetworkSolver
from typing import Any
from dataclasses import dataclass
from typing import Protocol
import numpy as np
import sympy as sp

class CircuitSolution(Protocol):
    def get_voltage(self, component_id: str) -> Any: ... 

    def get_current(self, component_id: str) -> Any: ...

    def get_potential(self, node_id: str) -> Any: ...

    def get_power(self, component_id: str) -> Any: ...

@dataclass(frozen=True)
class ScalarCircuitSolution:
    solution: NetworkSolution

@dataclass(frozen=True)
class VectorCircuitSolution:
    solutions: list[ScalarCircuitSolution]

@dataclass(frozen=True)
class EmptySolution:
    def get_voltage(self, component_id: str) -> Any:
        return None

    def get_current(self, component_id: str) -> Any:
        return None

    def get_potential(self, node_id: str) -> Any:
        return None

    def get_power(self, component_id: str) -> Any:
        return None

@dataclass(frozen=True)
class DCSolution(ScalarCircuitSolution):
    def get_voltage(self, component_id: str) -> float:
        return self.solution.get_voltage(component_id).real

    def get_current(self, component_id: str) -> float:
        return self.solution.get_current(component_id).real

    def get_potential(self, node_id: str) -> float:
        return self.solution.get_potential(node_id).real

    def get_power(self, component_id: str) -> float:
        return self.get_voltage(component_id)*self.get_current(component_id)

@dataclass(frozen=True)
class ComplexSolution(ScalarCircuitSolution):
    w: float = 0
    peak_values: bool = False

    def get_voltage(self, component_id: str) -> complex:
        return self.solution.get_voltage(component_id)

    def get_current(self, component_id: str) -> complex:
        return self.solution.get_current(component_id)

    def get_potential(self, node_id: str) -> complex:
        return self.solution.get_potential(node_id)

    def get_power(self, component_id: str) -> complex:
        if self.peak_values:
            return 1/2*self.get_voltage(component_id)*np.conj(self.get_current(component_id))
        return self.get_voltage(component_id)*np.conj(self.get_current(component_id))

class SymbolicSolution(ScalarCircuitSolution):
    def get_voltage(self, component_id: str) -> Any:
        return self.solution.get_voltage(component_id).simplify().nsimplify()

    def get_current(self, component_id: str) -> Any:
        return self.solution.get_current(component_id).simplify().nsimplify()

    def get_potential(self, node_id: str) -> Any:
        return self.solution.get_potential(node_id).simplify().nsimplify()

    def get_power(self, component_id: str) -> Any:
        return (self.get_voltage(component_id)*self.get_current(component_id)).simplify().nsimplify()

@dataclass(frozen=True)
class TimeDomainSolution(VectorCircuitSolution):
    solutions: list[ComplexSolution]
    w: list[float]

    def get_voltage(self, component_id: str) -> TimeDomainFunction:
        voltages = [solution.get_voltage(component_id) for solution in self.solutions]
        return np.vectorize(lambda t: np.array(np.sum([np.abs(V)*np.cos(w*t+np.angle(V)) for V, w in zip(voltages, self.w)])))

    def get_current(self, component_id: str) -> TimeDomainFunction:
        currents = [solution.get_current(component_id) for solution in self.solutions]
        return np.vectorize(lambda t: np.array(np.sum([np.abs(V)*np.cos(w*t+np.angle(V)) for V, w in zip(currents, self.w)])))

    def get_potential(self, node_id: str) -> TimeDomainFunction:
        potentials = [solution.get_potential(node_id) for solution in self.solutions]
        return np.vectorize(lambda t: np.array(np.sum([np.abs(phi)*np.cos(w*t+np.angle(phi)) for phi, w in zip(potentials, self.w)])))

    def get_power(self, component_id: str) -> TimeDomainFunction:
        voltage = self.get_voltage(component_id)
        current = self.get_current(component_id)
        return lambda t: np.array(voltage(t))*np.array(current(t))

@dataclass(frozen=True)
class FrequencyDomainSolution(VectorCircuitSolution):
    solutions: list[ComplexSolution]
    w: np.ndarray

    def get_voltage(self, component_id: str) -> FrequencyDomainSeries:
        voltages = 1/2*np.array([solution.get_voltage(component_id) for solution in self.solutions])
        return np.array(self.w), voltages

    def get_current(self, component_id: str) -> FrequencyDomainSeries:
        currents = 1/2*np.array([solution.get_current(component_id) for solution in self.solutions])
        return np.array(self.w), currents

    def get_potential(self, node_id: str) -> FrequencyDomainSeries:
        potentials = 1/2*np.array([solution.get_potential(node_id) for solution in self.solutions])
        return np.array(self.w), potentials

    def get_power(self, component_id: str) -> FrequencyDomainSeries:
        power = np.array([solution.get_power(component_id) for solution in self.solutions])
        return np.array(self.w), power

@dataclass(frozen=True)
class TransientSolution:
    t: np.ndarray
    ssm: StateSpaceMatrixConstructor
    u: np.ndarray
    x: np.ndarray

    def get_voltage(self, component_id: str) -> TimeDomainSeries:
        c, d = self.ssm.c_d_row_for_voltage(component_id)
        return self.t, np.reshape(c@self.x + d@self.u, (-1,))

    def get_current(self, component_id: str) -> TimeDomainSeries:
        c, d = self.ssm.c_d_row_for_current(component_id)
        return self.t, np.reshape(c@self.x + d@self.u, (-1,))

    def get_potential(self, node_id: str) -> TimeDomainSeries:
        c, d = self.ssm.c_d_row_for_potential(node_id)
        return self.t, np.reshape(c@self.x + d@self.u, (-1,))

    def get_power(self, component_id: str) -> TimeDomainSeries:
        return self.t, self.get_voltage(component_id)[1]*self.get_current(component_id)[1]

def dc_solution(circuit: Circuit, solver: NetworkSolver = numeric_nodal_analysis_bias_point_solution) -> DCSolution:
    network = transform(circuit, w=[0])[0]
    solution = solver(network)
    return DCSolution(solution=solution)

def complex_solution(circuit: Circuit, w: float = 0, peak_values: bool = False, solver: NetworkSolver = numeric_nodal_analysis_bias_point_solution) -> ComplexSolution:
    network = transform(circuit, w=[w], rms=not peak_values)[0]
    solution = solver(network)
    return ComplexSolution(solution=solution, w=w, peak_values=peak_values)

def symbolic_solution(circuit: Circuit, s: sp.core.symbol.Symbol = sp.Symbol('s', complex=True), solver: NetworkSolver = symbolic_nodal_analysis_bias_point_solution) -> SymbolicSolution:
    network = transform_symbolic_circuit(circuit, s=s)
    solution = solver(network)
    return SymbolicSolution(solution=solution)

def time_domain_solution(circuit: Circuit, w_max: float = 0, solver: NetworkSolver = numeric_nodal_analysis_bias_point_solution) -> TimeDomainSolution:
    w = frequency_components(circuit, w_max)
    solutions = [complex_solution(circuit, w=w_, peak_values=True, solver=solver) for w_ in w]
    return TimeDomainSolution(solutions=solutions, w=w)

def frequency_domain_solution(circuit: Circuit, w_max: float = 0, solver: NetworkSolver = numeric_nodal_analysis_bias_point_solution) -> FrequencyDomainSolution:
    w = np.array(frequency_components(circuit, w_max))
    solutions = [complex_solution(circuit, w=w_, peak_values=False, solver=solver) for w_ in w]
    return FrequencyDomainSolution(solutions=solutions, w=w)

def transient_solution(circuit: Circuit, tin: np.ndarray = np.zeros(0), input: dict[str, TimeDomainFunction] = {'': lambda t: np.zeros(0)}) -> TransientSolution:
    def _input_fcn(input_id: str) -> TimeDomainFunction:
        try:
            return input[input_id]
        except KeyError as e:
            raise KeyError(f'Input element with id "{input_id}" not defined.') from e
    ssm = numeric_state_space_model_constructor(circuit)
    u = np.array([_input_fcn(input_id)(tin) for input_id in ssm.sources])
    tout, x, _ = continuous_state_space_solver(
        NumericStateSpaceModel(A=ssm.A, B=ssm.B, C=np.eye(ssm.A.shape[0]), D=np.zeros((ssm.A.shape[0], ssm.B.shape[1]))),
        u.T,
        tin,
        np.zeros((ssm.A.shape[0], ))
    )
    x = np.reshape(x, (x.shape[0], ssm.A.shape[0])).T
    return TransientSolution(t=tout, ssm=ssm, u=u, x=x)
        
        