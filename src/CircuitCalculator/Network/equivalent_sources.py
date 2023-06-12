from .network import Network
from .NodalAnalysis import NodalAnalysisSolution
from .impedance import open_circuit_impedance


def calculate_open_circuit_voltage(network: Network, node1: str, node2: str) -> complex:
    if node1 == node2:
        return 0
    solution = NodalAnalysisSolution(network)
    open_circuit_branch = network.branches_between(node1, node2)[0]
    if open_circuit_branch.node1 == node1:
        return solution.get_voltage(open_circuit_branch.id)
    else:
        return -solution.get_voltage(open_circuit_branch.id)

class TheveninEquivalentSource:
    def __init__(self, network: Network, node1: str, node2: str) -> None:
        self.U = calculate_open_circuit_voltage(network, node1, node2)
        self.Z = open_circuit_impedance(network, node1, node2)

class NortenEquivalentSource:
    def __init__(self, network: Network, node1: str, node2: str) -> None:
        thevenin = TheveninEquivalentSource(network, node1, node2)
        self.I = thevenin.U/thevenin.Z
        self.Y = 1/thevenin.Z
        