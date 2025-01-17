from typing import Optional
from .schematic import create_schematic
from .errors import simulation_exceptions
from matplotlib.axes import Axes
from CircuitCalculator.dump_load import load, FormatError
from CircuitCalculator.Circuit.solution import CircuitSolution
from CircuitCalculator.SimpleCircuit.DiagramTranslator import circuit_translator

def load_simulation_file(name: str) -> dict:
    try:
        return load(name)
    except FileNotFoundError:
        print(f'Simulation file "{name}" does not exist.')
        return {}
    except FormatError:
        print(f'Cannot parse "{name}" as simulation file due to format issues.')
        return {}

def parse_circuit_data(data: dict) -> dict:
    circuit_definiton = data.get('circuit', {'unit': 7, 'elements': [], 'solution': {'type': None}})
    if len(circuit_definiton['elements']) == 0:
        raise ValueError('No elements in circuit definition')
    return circuit_definiton
    
def show_schematic(data: dict, ax: Optional[Axes] = None) -> None:
    try:
        create_schematic(parse_circuit_data(data), ax)
    except simulation_exceptions as e:
        print(e)
        return

def show_schematic_from_file(name: str, ax: Optional[Axes] = None) -> None:
    data = load_simulation_file(name)
    show_schematic(data, ax)

def simulate_schematic(data: dict) -> CircuitSolution:
    ...

def simulate_schematic_from_file(name: str) -> CircuitSolution:
    data = load_simulation_file(name)
    return simulate_schematic(data)