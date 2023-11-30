from .network import Network
from .NodalAnalysis.node_analysis import open_circuit_impedance, open_circuit_voltage

class TheveninEquivalentSource:
    def __init__(self, network: Network, node1: str, node2: str) -> None:
        self.U = open_circuit_voltage(network, node1, node2)
        self.Z = open_circuit_impedance(network, node1, node2)

class NortenEquivalentSource:
    def __init__(self, network: Network, node1: str, node2: str) -> None:
        thevenin = TheveninEquivalentSource(network, node1, node2)
        self.I = thevenin.U/thevenin.Z
        self.Y = 1/thevenin.Z
        