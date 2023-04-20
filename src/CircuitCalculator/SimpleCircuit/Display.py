from ..Utils import ScientificFloat, ScientificComplex
from math import degrees, pi
from cmath import phase

blue = '#02468F'
red = '#D20000'

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