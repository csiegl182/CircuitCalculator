from .schematic import create_schematic
from . import errors
from ..Circuit.circuit import Circuit
from ..Circuit import terminal_analysis as ta
from ..SimpleCircuit.DiagramTranslator import circuit_translator
from ..dump_load import load, ParseError


SimulationSource = str | dict


def load_simulation_file(name: str) -> dict:
    try:
        return load(name)
    except FileNotFoundError as e:
        raise FileNotFoundError(f'Simulation file "{name}" does not exist.') from e
    except ParseError as e:
        raise ParseError(f'Cannot parse "{name}" as simulation file due to format issues.') from e


def circuit_from_simulation_data(data: dict) -> Circuit:
    schematic = create_schematic(data)
    return circuit_translator(schematic)


def circuit_from_simulation_source(source: SimulationSource) -> Circuit:
    if isinstance(source, str):
        source = load_simulation_file(source)
    return circuit_from_simulation_data(source)


def open_circuit_voltage(
    source: SimulationSource,
    node1: str,
    node2: str,
    w: float = 0,
    *,
    w_resolution: float = 1e-3,
    rms: bool = True
) -> complex:
    return ta.open_circuit_voltage(
        circuit_from_simulation_source(source),
        node1,
        node2,
        w,
        w_resolution=w_resolution,
        rms=rms
    )


def short_circuit_current(
    source: SimulationSource,
    node1: str,
    node2: str,
    w: float = 0,
    *,
    w_resolution: float = 1e-3,
    rms: bool = True
) -> complex:
    return ta.short_circuit_current(
        circuit_from_simulation_source(source),
        node1,
        node2,
        w,
        w_resolution=w_resolution,
        rms=rms
    )


def thevenin_parameters(
    source: SimulationSource,
    node1: str,
    node2: str,
    w: float = 0,
    *,
    w_resolution: float = 1e-3,
    rms: bool = True
) -> ta.EquivalentSourceParameters:
    return ta.thevenin_parameters(
        circuit_from_simulation_source(source),
        node1,
        node2,
        w,
        w_resolution=w_resolution,
        rms=rms
    )


def norten_parameters(
    source: SimulationSource,
    node1: str,
    node2: str,
    w: float = 0,
    *,
    w_resolution: float = 1e-3,
    rms: bool = True
) -> ta.EquivalentSourceParameters:
    return ta.norten_parameters(
        circuit_from_simulation_source(source),
        node1,
        node2,
        w,
        w_resolution=w_resolution,
        rms=rms
    )


norton_parameters = norten_parameters


equivalent_source_exceptions = errors.simulation_exceptions
