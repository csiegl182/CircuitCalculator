from .controlled_sources import (
    CurrentControlledCurrentSource,
    CurrentControlledVoltageSource,
    VoltageControlledCurrentSource,
    VoltageControlledVoltageSource,
)
from .network_components import NortenTheveninElement, TwoTerminalComponent
from .norten_thevenin_elements import NortenElement, TheveninElement

def impedance(name : str, Z : complex) -> NortenTheveninElement:
    return NortenElement(Z=Z, V=0, name=name, type='impedance')

def admittance(name : str, Y : complex) -> NortenTheveninElement:
    return TheveninElement(Y=Y, I=0, name=name, type='admittance')

def resistor(name : str, R : float) -> NortenTheveninElement:
    return NortenElement(Z=R, V=0, name=name, type='resistor')

def conductance(name : str, G : float) -> NortenTheveninElement:
    return TheveninElement(Y=G, I=0, name=name, type='conductance')

def load(name : str, P : float, V_ref: float = -1, I_ref: float = -1, Q : float = 0) -> NortenTheveninElement:
    if V_ref < 0 and I_ref < 0:
        raise AttributeError('A reference voltage or reference current has to be defined for a load.')
    if V_ref > 0 and I_ref > 0:
        raise AttributeError('You can only define a reference voltage or a reference current for a load.')
    if V_ref == 0 and I_ref < 0:
        raise ValueError('Reference voltage must be greater than zero.')
    if I_ref <= 0 and V_ref < 0:
        raise ValueError('Reference current must be greater than zero.')
    if V_ref > 0:
        return TheveninElement(Y=complex(P, Q)/V_ref**2, I=0, name=name, type='load')
    return NortenElement(Z=complex(P, Q)/I_ref**2, V=0, name=name, type='load')

def voltage_source(name : str, V : complex, Z : complex = 0) -> NortenTheveninElement:
    return NortenElement(V=V, Z=Z, name=name, type='voltage_source')

def current_source(name : str, I : complex, Y : complex = 0) -> NortenTheveninElement:
    return TheveninElement(I=I, Y=Y, name=name, type='current_source')

def voltage_controlled_current_source(name: str, G: complex, control_nodes: tuple[str, str]) -> TwoTerminalComponent:
    return VoltageControlledCurrentSource(
        name=name,
        transconductance=G,
        control_node1=control_nodes[0],
        control_node2=control_nodes[1]
    )


def current_controlled_current_source(name: str, current_gain: complex, control_branch: str) -> TwoTerminalComponent:
    return CurrentControlledCurrentSource(
        name=name,
        current_gain=current_gain,
        control_branch=control_branch,
    )


def voltage_controlled_voltage_source(name: str, voltage_gain: complex, control_nodes: tuple[str, str]) -> TwoTerminalComponent:
    return VoltageControlledVoltageSource(
        name=name,
        voltage_gain=voltage_gain,
        control_node1=control_nodes[0],
        control_node2=control_nodes[1],
    )


def current_controlled_voltage_source(name: str, transresistance: complex, control_branch: str) -> TwoTerminalComponent:
    return CurrentControlledVoltageSource(
        name=name,
        transresistance=transresistance,
        control_branch=control_branch,
    )


def open_circuit(name : str) -> NortenTheveninElement:
    return TheveninElement(I=0, Y=0, name=name, type='open_circuit')

def short_circuit(name : str) -> NortenTheveninElement:
    return NortenElement(V=0, Z=0, name=name, type='short_circuit')
