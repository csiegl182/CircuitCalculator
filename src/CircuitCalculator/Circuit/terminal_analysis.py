from dataclasses import dataclass

from .circuit import Circuit, transform_circuit
from ..Network.NodalAnalysis import network_analysis as na
from ..Network.NodalAnalysis import node_analysis


@dataclass(frozen=True)
class EquivalentSourceParameters:
    open_circuit_voltage: complex
    short_circuit_current: complex
    impedance: complex
    admittance: complex

    @classmethod
    def from_thevenin_parameters(cls, open_circuit_voltage: complex, impedance: complex) -> "EquivalentSourceParameters":
        return cls(
            open_circuit_voltage=open_circuit_voltage,
            short_circuit_current=open_circuit_voltage/impedance,
            impedance=impedance,
            admittance=1/impedance
        )

    @classmethod
    def from_norton_parameters(cls, short_circuit_current: complex, admittance: complex) -> "EquivalentSourceParameters":
        return cls(
            open_circuit_voltage=short_circuit_current/admittance,
            short_circuit_current=short_circuit_current,
            impedance=1/admittance,
            admittance=admittance
        )

    from_norten_parameters = from_norton_parameters


def open_circuit_voltage(
    circuit: Circuit,
    node1: str,
    node2: str,
    w: float = 0,
    *,
    w_resolution: float = 1e-3,
    rms: bool = True
) -> complex:
    return na.open_circuit_voltage(transform_circuit(circuit, w, w_resolution=w_resolution, rms=rms), node1, node2)


def short_circuit_current(
    circuit: Circuit,
    node1: str,
    node2: str,
    w: float = 0,
    *,
    w_resolution: float = 1e-3,
    rms: bool = True
) -> complex:
    return na.short_circuit_current(transform_circuit(circuit, w, w_resolution=w_resolution, rms=rms), node1, node2)


def thevenin_parameters(
    circuit: Circuit,
    node1: str,
    node2: str,
    w: float = 0,
    *,
    w_resolution: float = 1e-3,
    rms: bool = True
) -> EquivalentSourceParameters:
    network = transform_circuit(circuit, w, w_resolution=w_resolution, rms=rms)
    U0 = na.open_circuit_voltage(network, node1, node2)
    Z = node_analysis.open_circuit_impedance(network, node1, node2)
    return EquivalentSourceParameters.from_thevenin_parameters(U0, Z)


def norten_parameters(
    circuit: Circuit,
    node1: str,
    node2: str,
    w: float = 0,
    *,
    w_resolution: float = 1e-3,
    rms: bool = True
) -> EquivalentSourceParameters:
    network = transform_circuit(circuit, w, w_resolution=w_resolution, rms=rms)
    IK = na.short_circuit_current(network, node1, node2)
    Z = node_analysis.open_circuit_impedance(network, node1, node2)
    return EquivalentSourceParameters.from_norton_parameters(IK, 1/Z)


norton_parameters = norten_parameters
