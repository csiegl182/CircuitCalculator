import matplotlib.pyplot as plt # type: ignore
import numpy as np
from CircuitCalculator.Network.network import Network


class PointerDiagram:
    def __init__(self, network: Network):
        self.fig, self.ax = plt.subplots()
        self._network = network
        self._label_branch_mapping = {branch.element.id: branch for branch in network.branches}

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.fig.show()

    def add_pointer(self, label: str):
        network = self.solution.ge
        U = self.solution.get_voltage()

        self.ax.plot([0, np.real(z)], [0, np.imag(z)])
