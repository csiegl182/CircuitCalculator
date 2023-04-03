from ..Utils import ScientificComplex

blue = '#02468F'
red = '#D20000'

def print_current(I: complex, precision: int = 3, polar=False) -> str:
    return str(ScientificComplex(I, 'A', precision=precision, polar=polar, use_exp_prefix=True, exp_prefixes={-6: 'u', -3: 'm', 3: 'k'}, compact=True))

def print_voltage(V: complex, precision: int = 3, polar=False) -> str:
    return str(ScientificComplex(V, 'V', precision=precision, polar=polar, use_exp_prefix=True, exp_prefixes={-6: 'u', -3: 'm', 3: 'k'}, compact=True))