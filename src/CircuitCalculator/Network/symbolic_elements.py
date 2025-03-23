from .norten_thevenin_elements import NortenTheveninElement, SymbolicNortenElement, SymbolicTheveninElement
import sympy as sp

def impedance(name : str, Z : str) -> NortenTheveninElement:
    return SymbolicNortenElement(Z=sp.sympify(Z), V=sp.sympify(0), name=name, type='impedance')

def admittance(name : str, Y : str) -> NortenTheveninElement:
    return SymbolicTheveninElement(Y=sp.sympify(Y), I=sp.sympify(0), name=name, type='admittance')

def resistor(name : str, R : str) -> NortenTheveninElement:
    return SymbolicNortenElement(Z=sp.sympify(R), V=sp.sympify(0), name=name, type='resistor')

def conductor(name : str, G : str) -> NortenTheveninElement:
    return SymbolicTheveninElement(Y=sp.sympify(G), I=sp.sympify(0), name=name, type='conductor')

def voltage_source(name : str, V : str, Z : str = '0') -> NortenTheveninElement:
    return SymbolicNortenElement(V=sp.sympify(V), Z=sp.sympify(Z), name=name, type='voltage_source')

def current_source(name : str, I : str, Y : str = '0') -> NortenTheveninElement:
    return SymbolicTheveninElement(I=sp.sympify(I), Y=sp.sympify(Y), name=name, type='current_source')

def open_circuit(name : str) -> NortenTheveninElement:
    return SymbolicTheveninElement(I=sp.sympify(0), Y=sp.sympify(0), name=name, type='open_circuit')

def short_circuit(name : str) -> NortenTheveninElement:
    return SymbolicNortenElement(V=sp.sympify(0), Z=sp.sympify(0), name=name, type='short_circuit')
