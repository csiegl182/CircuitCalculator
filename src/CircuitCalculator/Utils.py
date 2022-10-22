import numpy as np

exp_prefixes = {
    -12 : 'p',
    -9 : 'n',
    -6 : 'u',
    -3 : 'm',
    -1 : 'c',
    3 : 'k',
    6 : 'M',
    9 : 'G',
    12 : 'T'
}

def scientific_float(value: float, precision: int = 3, use_exp_prefix: bool = False, exp_prefixes=exp_prefixes) -> str:
    def _floor3(value: float) -> int:
        return 3*np.floor(value/3)
    def _left_comma_valid_digits(value: float) -> int:
        return int(np.floor(np.log10(np.abs(value))))+1
    exp_extension = ''
    exp_prefix = ''
    scaling_exp = int(_floor3(np.log10(np.abs(value))))
    scaling = 10**scaling_exp
    value /= scaling
    decimal_places = max(0, precision - _left_comma_valid_digits(value))
    if use_exp_prefix:
        if scaling_exp in exp_prefixes.keys():
            exp_prefix = exp_prefixes[scaling_exp]
            scaling_exp -= scaling_exp
        else:
            if scaling_exp > max(exp_prefixes.keys()):
                exp_prefix = exp_prefixes[max(exp_prefixes.keys())]
                scaling_exp -= max(exp_prefixes.keys())
            if scaling_exp < min(exp_prefixes.keys()):
                exp_prefix = exp_prefixes[min(exp_prefixes.keys())]
                scaling_exp -= min(exp_prefixes.keys())
    if scaling_exp != 0:
        exp_extension = f'e{scaling_exp}'
    return f'{value:.{decimal_places}f}{exp_extension}{exp_prefix}'