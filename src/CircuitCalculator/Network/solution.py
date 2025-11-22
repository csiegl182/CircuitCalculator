from .network import Network
from typing import Callable, Protocol, Any

class NetworkSolution(Protocol):
    def get_voltage(self, branch_id: str) -> Any: ...

    def get_current(self, branch_id: str) -> Any: ...

    def get_potential(self, node_id: str) -> Any: ...

    def get_power(self, branch_id: str) -> Any: ...

NetworkSolver = Callable[[Network], NetworkSolution]

class NetworkSolutionException(Exception):
    def __init__(self, message: str = '', floating_nodes: tuple[str, ...] = (), contradictional_elements: tuple[str, ...] = ()) -> None:
        self.floating_nodes = floating_nodes
        self.contradictional_elements = contradictional_elements
        message += ' Floating nodes: ['
        message += ', '.join(floating_nodes) if floating_nodes else 'none'
        message += ']'
        message += ' Contradictional elements: ['
        message += ', '.join(contradictional_elements) if contradictional_elements else 'none'
        message += ']'
        super().__init__(message)