import sympy as sp
from ..Network import symbolic_elements as elm
from ..Network import network as ntw
from typing import Callable, TypeVar
from . import components as ccp

CircuitComponent = TypeVar("CircuitComponent", bound=ccp.Component)
CircuitComponentTranslator = Callable[[ccp.Component], ntw.Branch]

def resistor(resistor: ccp.Component) -> ntw.Branch:
    R = sp.sympify(resistor.value['R'])
    if R == sp.nan or resistor.id == resistor.value['R']:
        R = sp.Symbol(resistor.id, real=True, positive=True)
    return ntw.Branch(resistor.nodes[0], resistor.nodes[1], elm.resistor(resistor.id, R))

def impedance(impedance: ccp.Component) -> ntw.Branch:
    Z = sp.sympify(impedance.value['Z'])
    if Z == sp.nan or impedance.id == impedance.value['Z']:
        Z = sp.Symbol(impedance.id, complex=True)
    return ntw.Branch(impedance.nodes[0], impedance.nodes[1], elm.impedance(impedance.id, Z))

def capacitor(capacitor: ccp.Component) -> ntw.Branch:
    C = sp.sympify(capacitor.value['C'])
    if C == sp.nan or capacitor.id == capacitor.value['C']:
        C = sp.Symbol(capacitor.id, real=True, positive=True)
    s = sp.Symbol('s')
    return ntw.Branch(
        capacitor.nodes[0],
        capacitor.nodes[1],
        elm.admittance(capacitor.id, s*C)  # type: ignore
    )

def inductance(inductance: ccp.Component) -> ntw.Branch:
    L = sp.sympify(inductance.value['L'])
    if L == sp.nan or inductance.id == inductance.value['L']:
        L = sp.Symbol(inductance.id, real=True, positive=True)
    s = sp.Symbol('s')
    return ntw.Branch(
        inductance.nodes[0],
        inductance.nodes[1],
        elm.impedance(inductance.id, s*L) # type: ignore
    )

def voltage_source(voltage_source: ccp.Component) -> ntw.Branch:
    V = sp.sympify(voltage_source.value['V'])
    Z = sp.sympify(voltage_source.value['R'])
    if V == sp.nan:
        V = sp.Symbol(voltage_source.id)
    element = elm.voltage_source(voltage_source.id, V, Z)
    return ntw.Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element)

def current_source(current_source: ccp.Component) -> ntw.Branch:
    cs_I = sp.sympify(current_source.value['I'])
    cs_G = sp.sympify(current_source.value['G'])
    if cs_I == sp.nan:
        cs_I = sp.Symbol(current_source.id)
    element = elm.current_source(current_source.id, cs_I, cs_G)
    return ntw.Branch(
        current_source.nodes[0],
        current_source.nodes[1],
        element
    )

def short_circuit(short_circuit: ccp.Component) -> ntw.Branch:
    return ntw.Branch(
        short_circuit.nodes[0],
        short_circuit.nodes[1],
        elm.short_circuit(short_circuit.id)
    )

transformers : dict[str, CircuitComponentTranslator] = {
    'resistor' : resistor,
    'impedance' : impedance,
    'capacitor' : capacitor,
    'inductance' : inductance,
    'voltage_source' : voltage_source,
    'current_source' : current_source,
    'short_circuit' : short_circuit,
    'dc_voltage_source' : voltage_source,
    'dc_current_source' : current_source
}