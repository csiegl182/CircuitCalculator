from .network import Network
from typing import Callable, Protocol

class NetworkSolution(Protocol):
    def get_voltage(self, branch_id: str) -> complex: ...

    def get_current(self, branch_id: str) -> complex: ...

NetworkSolver = Callable[[Network], NetworkSolution]