from ..Utils import scientific_float

blue = '#02468F'
red = '#D20000'

def print_current(I: complex, precision: int = 3) -> str:
    real_part = scientific_float(I.real, precision=precision, use_exp_prefix=True, exp_prefixes={-6: 'u', -3: 'm', 3: 'k'})
    if I.imag/precision < 1:
        return real_part
    else:
        imag_part = scientific_float(I.imag, precision=precision, use_exp_prefix=True, exp_prefixes={-6: 'u', -3: 'm', 3: 'k'})
        return f'{real_part} + j{imag_part}'

def print_voltage(V: complex, precision: int = 3) -> str:
    real_part = scientific_float(V.real, precision=precision, use_exp_prefix=True, exp_prefixes={-6: 'u', -3: 'm', 3: 'k'})
    if V.imag/precision < 1:
        return real_part
    else:
        imag_part = scientific_float(V.imag, precision=precision, use_exp_prefix=True, exp_prefixes={-6: 'u', -3: 'm', 3: 'k'})
        return f'{real_part} + j{imag_part}'