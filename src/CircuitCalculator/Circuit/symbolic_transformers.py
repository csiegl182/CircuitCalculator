import sympy as sp
from ..Network import symbolic_elements as elm
from ..Network import network as ntw
from typing import Callable, TypeVar
from . import components as ccp

CircuitComponent = TypeVar("CircuitComponent", bound=ccp.Component)
CircuitComponentTranslator = Callable[[ccp.Component], ntw.Branch]

def resistor(resistor: ccp.Component) -> ntw.Branch:
    R = sp.sympify(resistor.value['R'])
    if id == resistor.value['R']:
        R = sp.Symbol(id, real=True, positive=True)
    return ntw.Branch(resistor.nodes[0], resistor.nodes[1], elm.resistor(resistor.id, R))

def impedance(impedance: ccp.Component) -> ntw.Branch:
    Z = sp.sympify(impedance.value['Z'])
    if id == impedance.value['Z']:
        Z = sp.Symbol(id, complex=True)
    return ntw.Branch(impedance.nodes[0], impedance.nodes[1], elm.impedance(impedance.id, Z))

def capacitor(capacitor: ccp.Component) -> ntw.Branch:
    C = capacitor.value['C']
    if id == capacitor.value['C']:
        C = sp.Symbol(id, real=True, positive=True)
    return ntw.Branch(
        capacitor.nodes[0],
        capacitor.nodes[1],
        elm.admittance(capacitor.id, sp.sympify(f's*{C}'))
    )

def inductance(inductance: ccp.Component) -> ntw.Branch:
    L = inductance.value['L']
    if id == inductance.value['L']:
        L = sp.Symbol(id, real=True, positive=True)
    return ntw.Branch(
        inductance.nodes[0],
        inductance.nodes[1],
        elm.impedance(inductance.id, sp.sympify(f's*{L}'))
    )

def voltage_source(voltage_source: ccp.Component) -> ntw.Branch:
    V = sp.sympify(voltage_source.value['V'])
    Z = sp.sympify(voltage_source.value['R'])
    element = elm.voltage_source(voltage_source.id, V, Z)
    return ntw.Branch(
        voltage_source.nodes[0],
        voltage_source.nodes[1],
        element)

def current_source(current_source: ccp.Component) -> ntw.Branch:
    cs_I = sp.sympify(current_source.value['I'])
    cs_G = sp.sympify(current_source.value['G'])
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
}