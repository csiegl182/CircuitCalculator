from .network import Network, Branch
from typing import Callable, Protocol

class NetworkSolution(Protocol):
    def get_voltage(self, branch: Branch) -> complex: pass

    def get_current(self, branch: Branch) -> complex: pass

NetworkSolver = Callable[[Network], NetworkSolution]