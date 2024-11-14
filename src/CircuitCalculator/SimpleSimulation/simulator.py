from typing import Optional
from .schematic import create_schematic
from .errors import handle_simulation_exceptions
from matplotlib.axes import Axes
from CircuitCalculator.dump_load import load

@handle_simulation_exceptions
def simulate(data: dict, circuit_ax: Optional[Axes] = None) -> None:
    circuit_definiton = data.get('circuit', {'unit': 7, 'elements': [], 'solution': {'type': None}})
    if len(circuit_definiton['elements']) == 0:
        raise ValueError('No elements in circuit definition')
    create_schematic(circuit_definiton, circuit_ax)

def simulate_file(name: str) -> None:
    data = load(name)
    simulate(data)