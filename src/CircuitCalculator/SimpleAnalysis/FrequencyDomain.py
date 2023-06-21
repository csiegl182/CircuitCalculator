from .layout import NyquistPlot, color
from ..Circuit.circuit import Circuit
from ..Circuit.impedance import open_circuit_impedance
from dataclasses import dataclass

@dataclass
class ImpedanceNyquistPlot:
    nyquist_plot: NyquistPlot
    circuit: Circuit

    def _set_reference(self, ref_id: str, z: complex, z0: complex) -> None:
        self._pointer_heads.update({ref_id: z+z0})

    def _get_reference(self, ref_id: str) -> complex:
        if ref_id == '':
            return 0
        return self._pointer_heads.get(ref_id, self.solution.get_voltage(ref_id))

    def add_impedance(self, label: str, nodes: tuple[str, str], color=color['blue']) -> None:
        z = self.solution.get_voltage(id)
        self.nyquist_plot.add_plot(z=z, color=color, label=f'Z({id})')

    def __enter__(self):
        self._pointer_heads = {}
        return self

    def __exit__(self, type, value, traceback):
        self.pointer_diagram.draw()
