from .norten_thevenin_elements import NortenTheveninElement, NortenElement, TheveninElement

def impedance(name : str, Z : complex) -> NortenTheveninElement:
    return NortenElement(Z=Z, V=0, name=name, type='impedance')

def admittance(name : str, Y : complex) -> NortenTheveninElement:
    return TheveninElement(Y=Y, I=0, name=name, type='admittance')

def resistor(name : str, R : float) -> NortenTheveninElement:
    return NortenElement(Z=R, V=0, name=name, type='resistor')

def conductor(name : str, G : float) -> NortenTheveninElement:
    return TheveninElement(Y=G, I=0, name=name, type='conductor')

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

def open_circuit(name : str) -> NortenTheveninElement:
    return TheveninElement(I=0, Y=0, name=name, type='open_circuit')

def short_circuit(name : str) -> NortenTheveninElement:
    return NortenElement(V=0, Z=0, name=name, type='short_circuit')
