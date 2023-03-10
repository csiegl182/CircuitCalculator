import numpy as np
from dataclasses import dataclass, field

@dataclass(frozen=True)
class ScientificFloat:
    value: float
    unit: str = ''
    precision: int = 3
    use_exp_prefix: bool = False
    exp_prefixes: dict[int, str] = field(default_factory=lambda: {
        -12 : 'p',
        -9 : 'n',
        -6 : 'u',
        -3 : 'm',
        -1 : 'c',
        0 : '',
        3 : 'k',
        6 : 'M',
        9 : 'G',
        12 : 'T'
    })

    @property
    def scaling_exp(self) -> int:
        scaling_exp1 = int(3*np.floor(np.log10(np.abs(self.value))/3))
        value = np.round(self.value / 10**scaling_exp1)*10**scaling_exp1
        scaling_exp2 = int(3*np.floor(np.log10(np.abs(value))/3))
        return scaling_exp2

    @property
    def scaled_value_exp(self) -> int:
        if not self.use_exp_prefix:
            return self.scaling_exp
        if not self.scaling_exp in self.exp_prefixes.keys():
            if self.scaling_exp > max(self.exp_prefixes.keys()):
                return self.scaling_exp - max(self.exp_prefixes.keys())
            if self.scaling_exp < min(self.exp_prefixes.keys()):
                return self.scaling_exp - min(self.exp_prefixes.keys())
        return 0

    @property
    def scaling(self) -> float:
        return 10**self.scaling_exp

    @property
    def scaled_value(self) -> float:
        return self.value/self.scaling

    @property
    def left_comma_valid_digits(self) -> int:
        return int(np.floor(np.log10(np.round(np.abs(self.scaled_value)))))+1

    @property
    def decimal_places(self) -> float:
        return max(0, self.precision - self.left_comma_valid_digits)
    
    @property
    def exp_prefix(self) -> str:
        if not self.use_exp_prefix:
            return ''
        if self.scaling_exp > max(self.exp_prefixes.keys()):
            return self.exp_prefixes[max(self.exp_prefixes.keys())]
        if self.scaling_exp < min(self.exp_prefixes.keys()):
            return self.exp_prefixes[min(self.exp_prefixes.keys())]
        if self.scaling_exp in self.exp_prefixes.keys():
            return self.exp_prefixes[self.scaling_exp]
        return ''

    @property
    def exp_extension(self) -> str:
        if self.scaled_value_exp != 0:
            return f'e{self.scaled_value_exp}'
        return ''

    def __str__(self) -> str:
        return f'{self.scaled_value:.{self.decimal_places}f}{self.exp_extension}{self.exp_prefix}{self.unit}'

@dataclass(frozen=True)
class ScientificComplex(ScientificFloat):
    value: complex
    unit: str = ''
    precision: int = 3
    use_exp_prefix: bool = False
    hide_minor_part: bool = True
    compact: bool = False
    polar: bool = False
    deg: bool = False
    exp_prefixes: dict[int, str] = field(default_factory=lambda: {
        -12 : 'p',
        -9 : 'n',
        -6 : 'u',
        -3 : 'm',
        -1 : 'c',
        0 : '',
        3 : 'k',
        6 : 'M',
        9 : 'G',
        12 : 'T'
    })

    @property
    def real(self) -> ScientificFloat:
        return ScientificFloat(abs(self.value.real), self.unit, self.precision, self.use_exp_prefix, self.exp_prefixes)

    @property
    def imag(self) -> ScientificFloat:
        return ScientificFloat(abs(self.value.imag), self.unit, self.precision, self.use_exp_prefix, self.exp_prefixes)

    @property
    def abs(self) -> ScientificFloat:
        return ScientificFloat(abs(self.value), self.unit, self.precision, self.use_exp_prefix, self.exp_prefixes)

    @property
    def angle(self) -> float:
        return float(np.angle(self.value, deg=self.deg))
    
    @property
    def real_sign(self) -> str:
        sign = '' if self.value.real >= 0 else '- '
        if self.compact:
            return sign.strip()
        return sign
    
    @property
    def imag_sign(self) -> str:
        sign = ' + ' if self.value.imag >= 0 else ' - '
        if self.compact:
            return sign.strip()
        return sign

    def __str__(self) -> str:
        with np.errstate(divide='ignore'):
            if self.polar:
                if self.deg:
                    if np.log10(np.abs(self.angle)) <= -2:
                        return f'{str(self.abs)}'
                    return f'{str(self.abs)}∠{self.angle:.2f}'
                if np.log10(np.abs(self.angle)) <= -5:
                    return f'{str(self.abs)}'
                return f'{str(self.abs)}∠{self.angle:.4f}'
            if self.hide_minor_part:
                if self.imag.scaling_exp > self.real.scaling_exp:
                    target_exp_prefix = {self.imag.scaling_exp : self.exp_prefixes[self.imag.scaling_exp]}
                target_exp_prefix = {self.real.scaling_exp : self.exp_prefixes[self.real.scaling_exp]}
                real = ScientificFloat(self.real.value, self.unit, self.precision, self.use_exp_prefix, target_exp_prefix)
                imag = ScientificFloat(self.imag.value, self.unit, self.precision, self.use_exp_prefix, target_exp_prefix)
                if real.scaled_value_exp > imag.scaled_value_exp:
                    return f'{self.real_sign}{real.__str__()}'
                if imag.scaled_value_exp > real.scaled_value_exp:
                    sign = '' if self.imag_sign.strip() == '+' else self.imag_sign
                    return f'{sign}j{imag.__str__()}'
                return f'{self.real_sign}{real.__str__()}{self.imag_sign}j{imag.__str__()}'
            return f'{self.real_sign}{self.real.__str__()}{self.imag_sign}j{self.imag.__str__()}'
