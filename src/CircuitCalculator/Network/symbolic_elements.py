from .norten_thevenin_elements import NortenTheveninElement, SymbolicNortenElement, SymbolicTheveninElement

def impedance(name : str, Z : str) -> NortenTheveninElement:
    return SymbolicNortenElement(Z=Z, V='0', name=name, type='impedance')

def admittance(name : str, Y : str) -> NortenTheveninElement:
    return SymbolicTheveninElement(Y=Y, I='0', name=name, type='admittance')

def resistor(name : str, R : str) -> NortenTheveninElement:
    return SymbolicNortenElement(Z=R, V='0', name=name, type='resistor')

def conductor(name : str, G : str) -> NortenTheveninElement:
    return SymbolicTheveninElement(Y=G, I='0', name=name, type='conductor')

def load(name : str, P : str, V_ref: str = '', I_ref: str = '', Q : str = '0') -> NortenTheveninElement:
    if V_ref == '' and I_ref == '':
        raise AttributeError('A reference voltage or reference current has to be defined for a load.')
    if V_ref != '' and I_ref != '':
        raise AttributeError('You can only define a reference voltage or a reference current for a load.')
    if V_ref != '':
        return SymbolicTheveninElement(Y=f'({P}+1j*{Q})/({V_ref}*{V_ref})', I='0', name=name, type='load')
    return SymbolicNortenElement(Z=f'({P}+1j*{Q})/({I_ref}*{I_ref})', V='0', name=name, type='load')

def voltage_source(name : str, V : str, Z : str = '0') -> NortenTheveninElement:
    return SymbolicNortenElement(V=V, Z=Z, name=name, type='voltage_source')

def current_source(name : str, I : str, Y : str = '0') -> NortenTheveninElement:
    return SymbolicTheveninElement(I=I, Y=Y, name=name, type='current_source')

def open_circuit(name : str) -> NortenTheveninElement:
    return SymbolicTheveninElement(I='0', Y='0', name=name, type='open_circuit')

def short_circuit(name : str) -> NortenTheveninElement:
    return SymbolicNortenElement(V='0', Z='0', name=name, type='short_circuit')
