from .norten_thevenin_elements import NortenTheveninElement, SymbolicNortenElement, SymbolicTheveninElement
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

def open_circuit(name : str) -> NortenTheveninElement:
    return SymbolicTheveninElement(I=sp.sympify(0), Y=sp.sympify(0), name=name, type='open_circuit')

def short_circuit(name : str) -> NortenTheveninElement:
    return SymbolicNortenElement(V=sp.sympify(0), Z=sp.sympify(0), name=name, type='short_circuit')
