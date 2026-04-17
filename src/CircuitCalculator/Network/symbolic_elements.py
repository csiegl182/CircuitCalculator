from .controlled_sources import (
    CurrentControlledCurrentSource,
    CurrentControlledVoltageSource,
    VoltageControlledCurrentSource,
    VoltageControlledVoltageSource,
)
from .network_components import NortenTheveninElement, TwoTerminalComponent
from .norten_thevenin_elements import SymbolicNortenElement, SymbolicTheveninElement
import sympy as sp

def impedance(name : str, Z : sp.Symbol) -> NortenTheveninElement:
    return SymbolicNortenElement(Z=Z, V=sp.sympify(0), name=name, type='impedance')

def admittance(name : str, Y : sp.Symbol) -> NortenTheveninElement:
    return SymbolicTheveninElement(Y=Y, I=sp.sympify(0), name=name, type='admittance')

def resistor(name : str, R : sp.Symbol) -> NortenTheveninElement:
    return SymbolicNortenElement(Z=R, V=sp.sympify(0), name=name, type='resistor')

def conductor(name : str, G : sp.Symbol) -> NortenTheveninElement:
    return SymbolicTheveninElement(Y=G, I=sp.sympify(0), name=name, type='conductor')

def voltage_source(name : str, V : sp.Symbol, Z : sp.Symbol = sp.sympify(0)) -> NortenTheveninElement:
    return SymbolicNortenElement(V=V, Z=sp.sympify(Z), name=name, type='voltage_source')

def current_source(name : str, I : sp.Symbol, Y : sp.Symbol = sp.sympify(0)) -> NortenTheveninElement:
    return SymbolicTheveninElement(I=I, Y=sp.sympify(Y), name=name, type='current_source')

def voltage_controlled_current_source(name: str, G: sp.Symbol, control_nodes: tuple[str, str]) -> TwoTerminalComponent:
    return VoltageControlledCurrentSource(
        name=name,
        transconductance=sp.sympify(G),
        control_node1=control_nodes[0],
        control_node2=control_nodes[1]
    )


def current_controlled_current_source(name: str, current_gain: sp.Symbol, control_branch: str) -> TwoTerminalComponent:
    return CurrentControlledCurrentSource(
        name=name,
        current_gain=sp.sympify(current_gain),
        control_branch=control_branch,
    )


def voltage_controlled_voltage_source(name: str, voltage_gain: sp.Symbol, control_nodes: tuple[str, str]) -> TwoTerminalComponent:
    return VoltageControlledVoltageSource(
        name=name,
        voltage_gain=sp.sympify(voltage_gain),
        control_node1=control_nodes[0],
        control_node2=control_nodes[1],
    )


def current_controlled_voltage_source(name: str, transresistance: sp.Symbol, control_branch: str) -> TwoTerminalComponent:
    return CurrentControlledVoltageSource(
        name=name,
        transresistance=sp.sympify(transresistance),
        control_branch=control_branch,
    )


def open_circuit(name : str) -> NortenTheveninElement:
    return SymbolicTheveninElement(I=sp.sympify(0), Y=sp.sympify(0), name=name, type='open_circuit')

def short_circuit(name : str) -> NortenTheveninElement:
    return SymbolicNortenElement(V=sp.sympify(0), Z=sp.sympify(0), name=name, type='short_circuit')
