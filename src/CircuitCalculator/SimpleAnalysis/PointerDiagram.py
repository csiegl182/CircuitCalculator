from .Layout import PointerDiagram, color
from ..Circuit.solution import ComplexSolution
from dataclasses import dataclass

@dataclass
class VoltagePointerDiagram:
    pointer_diagram: PointerDiagram
    solution: ComplexSolution
    resistance: float = 1

    def _set_reference(self, ref_id: str, z: complex, z0: complex) -> None:
        self._pointer_heads.update({ref_id: z+z0})

    def _get_reference(self, ref_id: str) -> complex:
        if ref_id == '':
            return 0
        return self._pointer_heads.get(ref_id, self.solution.get_voltage(ref_id))

    def add_voltage_pointer(self, id: str, origin: str='', color=color['blue']) -> None:
        z = self.solution.get_voltage(id)
        z0 = self._get_reference(origin)
        self._set_reference(id, z, z0)
        self.pointer_diagram.add_pointer(z=z, z0=z0, color=color, label=f'V({id})')

    def add_current_pointer(self, id: str, color=color['red'], resistance: float = 0) -> None:
        if resistance == 0:
            resistance = self.resistance
        z = self.solution.get_current(id)*resistance
        self.pointer_diagram.add_pointer(z=z, color=color, label=f'I({id})·{resistance}Ω')

    def __enter__(self):
        self._pointer_heads = {}
        return self

    def __exit__(self, type, value, traceback):
        self.pointer_diagram.draw()

@dataclass
class CurrentPointerDiagram:
    pointer_diagram: PointerDiagram
    solution: ComplexSolution
    conductance: float = 1

    def _set_reference(self, ref_id: str, z: complex, z0: complex) -> None:
        self._pointer_heads.update({ref_id: z+z0})

    def _get_reference(self, ref_id: str) -> complex:
        if ref_id == '':
            return 0
        return self._pointer_heads.get(ref_id, self.solution.get_current(ref_id))

    def add_current_pointer(self, id: str, origin: str='', color=color['red']) -> None:
        z = self.solution.get_current(id)
        z0 = self._get_reference(origin)
        self._set_reference(id, z, z0)
        self.pointer_diagram.add_pointer(z=z, z0=z0, color=color, label=f'I({id})')

    def add_voltage_pointer(self, id: str, color=color['blue'], conductance: float = 0) -> None:
        if conductance == 0:
            conductance = self.conductance
        z = self.solution.get_voltage(id)*conductance
        self.pointer_diagram.add_pointer(z=z, color=color, label=f'V({id})·{conductance}S')

    def __enter__(self):
        self._pointer_heads = {}
        return self

    def __exit__(self, type, value, traceback):
        self.pointer_diagram.draw()

@dataclass
class PQDiagram:
    pointer_diagram: PointerDiagram
    solution: ComplexSolution
    
    def add_power(self, id: str, color=color['green']) -> None:
        z = self.solution.get_power(id)
        self.pointer_diagram.add_pointer(z=z, color=color, label=f'S({id})')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.pointer_diagram.draw()