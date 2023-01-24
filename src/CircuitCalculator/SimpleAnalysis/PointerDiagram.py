import numpy as np
from .Elements import complex_pointer
from .Layout import Layout, color, grid_layout
from functools import partial
from CircuitCalculator.Network.solution import NetworkSolution

class PointerDiagram:
    def __init__(self, layout: Layout = grid_layout):
        self.pointer_drawers = []
        self._max_length = 0
        self.fig, self.ax = layout()
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlabel(r'$\mathrm{Re}\,\{U\}$')
        self.ax.set_ylabel(r'$\mathrm{Im}\,\{U\}$')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        for draw_pointer in self.pointer_drawers:
            draw_pointer(height=0.05*self._max_length, width=0.05*self._max_length)
        self.ax.legend(
            handles=[line for line in self.ax.lines],
            ncols=len(self.ax.lines),
            loc='upper center',
            bbox_to_anchor=(0.5, 1.1),
            frameon=False
        )
        self.fig.show()

    def add_pointer(self, z: complex, z0: complex = 0, **kwargs):
        self._max_length = max(self._max_length, np.abs(z))
        self.pointer_drawers.append(partial(complex_pointer, self.ax, z0, z0+z, **kwargs))

class VoltagePointerDiagram(PointerDiagram):
    def __init__(self, solution: NetworkSolution, conductor: float = 1.0, layout: Layout = grid_layout):
        self._solution = solution
        self._conductor = conductor
        self._pointer_heads = {}
        super().__init__(layout=layout)

    def _set_reference(self, ref_id: str, z: complex, z0: complex) -> None:
        self._pointer_heads.update({ref_id: z+z0})

    def _get_reference(self, ref_id: str) -> complex:
        if ref_id == '':
            return 0
        return self._pointer_heads.get(ref_id, self._solution.get_voltage(ref_id))

    def add_voltage_pointer(self, id: str, origin: str='', color=color['blue']) -> None:
        z = self._solution.get_voltage(id)
        z0 = self._get_reference(origin)
        self._set_reference(id, z, z0)
        self.add_pointer(z=z, z0=z0, color=color, label=f'$V({id})$')

    def add_current_pointer(self, id: str, color=color['red'], conductor: float = 0) -> None:
        if conductor == 0:
            conductor = self._conductor
        z = self._solution.get_current(id)*conductor
        self.add_pointer(z=z, color=color, label=f'$I({id})/{conductor}\Omega$')
