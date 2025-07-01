from .components import Component
import sympy as sp

def value_less_than_zero(value: str) -> bool:
    if len(value) == 0:
        return False
    x = sp.sympify(value)
    try:
        return (x < 0) == True
    except TypeError:
        return False

def resistor(id: str, nodes: tuple[str, str], R: str = '', **_) -> Component:
    if value_less_than_zero(R):
        raise ValueError('R must be greater than zero.')
    return Component(
        type='resistor',
        id=id,
        value={'R': R if len(R) > 0 else id},
        nodes=nodes
        )

def conductance(id: str, nodes: tuple[str, str], G: str = '', **_) -> Component:
    if value_less_than_zero(G):
        raise ValueError('G must be greater than zero.')
    return Component(
        type='conductance',
        id=id,
        value={'G': G if len(G) > 0 else id},
        nodes=nodes
        )

def capacitor(id: str, nodes: tuple[str, str], C: str = '', **_) -> Component:
    if value_less_than_zero(C):
        raise ValueError('C must be greater than zero.')
    return Component(
        type='capacitor',
        id=id,
        value={'C': C if len(C) > 0 else id},
        nodes=nodes
    )

def inductance(id: str, nodes: tuple[str, str], L: str = '', **_) -> Component:
    if value_less_than_zero(L):
        raise ValueError('L must be greater than zero.')
    return Component(
        type='inductance',
        id=id,
        value={'L': L if len(L) > 0 else id},
        nodes=nodes
    )

def impedance(id: str, nodes: tuple[str, str], Z: str = '', **_) -> Component:
    return Component(
        type='impedance',
        id=id,
        value={'Z': Z if len(Z) > 0 else id},
        nodes=nodes
        )

def admittance(id: str, nodes: tuple[str, str], Y: str = '', **_) -> Component:
    return Component(
        type='admittance',
        id=id,
        value={'Y': Y if len(Y) > 0 else id},
        nodes=nodes
        )

def voltage_source(id: str, nodes: tuple[str, str], V: str = '', R: str = '0', **_) -> Component:
    return Component(
        type='dc_voltage_source',
        id=id,
        value={'V': V if len(V) > 0 else id, 'R': R, 'w': 0, 'phi': 0},
        nodes=nodes
        )

def current_source(id: str, nodes: tuple[str, str], I: str = '', G: str = '0', **_) -> Component:
    return Component(
        type='dc_current_source',
        id=id,
        value={'I': I if len(I) > 0 else id, 'G': G, 'w': 0, 'phi': 0},
        nodes=nodes
        )

def open_circuit(id: str, nodes: tuple[str, str], **_) -> Component:
    return Component(
        type='open_circuit',
        id=id,
        nodes=nodes
    )        

def short_circuit(id: str, nodes: tuple[str, str], **_) -> Component:
    return Component(
        type='short_circuit',
        id=id,
        nodes=nodes
    )        

def ground(id: str='gnd', nodes: tuple[str]=('0',), **_) -> Component:
    return Component(
        type='ground',
        id=id,
        nodes=nodes
    )