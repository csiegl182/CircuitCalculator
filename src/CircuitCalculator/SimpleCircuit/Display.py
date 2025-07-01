from ..Display.ScientificFloat import ScientificFloat, ScientificComplex
from math import degrees, pi
from cmath import phase

blue = '#02468F'
red = '#D20000'
green = '#007355'

def print_complex(value: complex, unit: str = '', precision: int = 3, polar: bool = False, deg: bool = False) -> str:
    return str(ScientificComplex(
        value=value,
        unit=unit,
        precision=precision,
        polar=polar,
        use_exp_prefix=True,
        deg=deg,
        exp_prefixes={-6: 'u', -3: 'm', 3: 'k'},
        compact=True
    ))

def print_abs(value: complex, unit: str = '', precision: int = 3) -> str:
    return str(ScientificFloat(
        value=abs(value),
        unit=unit,
        precision=precision,
        use_exp_prefix=True,
        exp_prefixes={-6: 'u', -3: 'm', 3: 'k'},
    ))

def print_real(value: complex, unit: str = '', precision: int = 3) -> str:
    return str(ScientificFloat(
        value=value.real,
        unit=unit,
        precision=precision,
        use_exp_prefix=True,
        exp_prefixes={-6: 'u', -3: 'm', 3: 'k'},
    ))

def print_sinosoidal(value: complex, unit: str = '', precision: int = 3, w: float = 0, sin: bool = False, deg: bool = False, hertz: bool = False) -> str:
    abs_value = ScientificFloat(value=abs(value), unit=unit, precision=precision, use_exp_prefix=True, exp_prefixes={-6: 'u', -3: 'm', 3: 'k'})
    phase_value = phase(value)
    phase_value+= -pi/2 if sin else 0
    abs_phase_value = ScientificFloat(value=abs(degrees(phase_value)), unit='°', precision=precision) if deg else ScientificFloat(value=abs(phase_value), precision=precision)
    label = str(abs_value)
    if w == 0:
        return label
    label+= '·'
    label+= 'sin' if sin else 'cos'
    label+= '('
    label+= '2π·' if hertz else ''
    label+= str(ScientificFloat(w/2/pi, 'Hz', precision=precision, use_exp_prefix=True, exp_prefixes={-3: 'm', 3: 'k', 6: 'M', 9: 'G', 12: 'T'})) if hertz else str(ScientificFloat(w, '/s', precision=precision))
    label+= '·t'
    if abs(phase_value) > 1e-4:
        label+= '+' if phase_value > 0 else '-'
        label+= str(abs_phase_value)
    label+= ')'
    return label

def print_active_power(value: float, precision: int = 3) -> str:
    P = ScientificFloat(value=abs(value), unit='W', precision=precision, use_exp_prefix=True)
    P_sign = '↓' if value > 0 else '↑'
    label = f'{P}{P_sign}'
    return label

def print_active_reactive_power(value: complex, precision: int = 3) -> str:
    P = ScientificFloat(value=abs(value.real), unit='W', precision=precision, use_exp_prefix=True)
    Q = ScientificFloat(value=abs(value.imag), unit='var', precision=precision, use_exp_prefix=True)
    P_sign = '↓' if value.real > 0 else '↑'
    Q_sign = '↓' if value.imag > 0 else '↑'
    label = f'P: {P_sign}{P}'
    label+= f'\nQ: {Q_sign}{Q}' if Q.value > 1e-4 else ''
    return label

def print_resistance(R: float, precision: int = 3):
    return str(ScientificFloat(value=R, unit='Ω', use_exp_prefix=True, exp_prefixes={-3: 'm', 3: 'k', 6: 'M', 9: 'G'}, precision=precision))

def print_conductance(G: float, precision: int = 3):
    return str(ScientificFloat(value=G, unit='S', use_exp_prefix=True, exp_prefixes={-3: 'm', 3: 'k', 6: 'M', 9: 'G'}, precision=precision))

def print_impedance(Z: complex, precision: int = 3):
    return str(ScientificComplex(value=Z, unit='Ω', use_exp_prefix=True, exp_prefixes={-3: 'm', 3: 'k', 6: 'M', 9: 'G'}, precision=precision))

def print_capacitance(C: float, precision: int = 3):
    return str(ScientificFloat(value=C, unit='F', use_exp_prefix=True, exp_prefixes={-12: 'p', -9: 'n', -6: 'μ', -3: 'm'}, precision=precision))

def print_inductance(L: float, precision: int = 3):
    return str(ScientificFloat(value=L, unit='H', use_exp_prefix=True, exp_prefixes={-9: 'n', -6: 'μ', -3: 'm'}, precision=precision))