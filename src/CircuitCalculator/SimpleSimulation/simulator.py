from typing import Optional
from .schematic import draw_schematic, create_schematic
from . import errors
from matplotlib.axes import Axes
from CircuitCalculator.dump_load import load, FormatError
import CircuitCalculator.Circuit.solution as solution
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.SimpleCircuit.DiagramTranslator import circuit_translator

def load_simulation_file(name: str) -> dict:
    try:
        return load(name)
    except FileNotFoundError as e:
        raise FileNotFoundError(f'Simulation file "{name}" does not exist.') from e
    except FormatError as e:
        raise FormatError(f'Cannot parse "{name}" as simulation file due to format issues.') from e
    
def show_schematic(data: dict, ax: Optional[Axes] = None) -> None:
    try:
        draw_schematic(data, ax)
    except errors.simulation_exceptions as e:
        print(e)
        return

def show_schematic_from_file(name: str, ax: Optional[Axes] = None) -> None:
    try:
        data = load_simulation_file(name)
        show_schematic(data, ax)
    except errors.simulation_exceptions as e:
        print(e)
        return

solutions : dict[str, type[solution.CircuitSolution]]= {
    'dc': solution.DCSolution,
    'complex': solution.ComplexSolution,
    'time_domain': solution.TimeDomainSolution,
    'frequency_domain': solution.FrequencyDomainSolution,
    'transient': solution.TransientSolution,
    'symbolic': solution.SymbolicSolution
}

def get_solution(solution_type: str, circuit: Circuit, **kwargs) -> solution.CircuitSolution:
    try:
        solution = solutions[solution_type]
    except KeyError as e:
        raise errors.UnknownSolutionType(solution_type, list(solutions.keys())) from e
    try:
        return solution(circuit, **kwargs)
    except TypeError as e:
        raise errors.SolutionUsageError(solution_type, list(kwargs.keys())) from e

def simulate_schematic(data: dict, solution_type: str, **kwargs) -> solution.CircuitSolution:
    try:
        schematic = create_schematic(data)
        circuit = circuit_translator(schematic)
        return get_solution(solution_type, circuit, **kwargs)
    except errors.simulation_exceptions as e:
        print(e)
        return solution.EmptySolution()

def simulate_schematic_from_file(name: str, solution_type: str, **kwargs) -> solution.CircuitSolution:
    try:
        data = load_simulation_file(name)
        return simulate_schematic(data, solution_type, **kwargs)
    except errors.simulation_exceptions as e:
        print(e)
        return solution.EmptySolution()