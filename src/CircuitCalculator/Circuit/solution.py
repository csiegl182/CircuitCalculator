from .circuit import Circuit, transform
from ..Network.NodalAnalysis import nodal_analysis_solver
from typing import Protocol, Any, Callable, List
from dataclasses import dataclass

class NetworkSolution(Protocol):
    def get_voltage(self, id: str) -> Any: ...

    def get_current(self, id: str) -> Any: ...

    def get_power(self, id: str) -> Any: ...

@dataclass
class TimneDomainCircuitSolution:
    circuit: Circuit

    def get_voltage(self, component_id: str) -> Callable[[float], List[float]]:
        network = transform(self.circuit)
        solution = nodal_analysis_solver(network)

        return lambda t: [1, 2, 3]