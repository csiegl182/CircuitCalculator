import numpy as np
from dataclasses import dataclass, field

@dataclass(frozen=True)
class FloatPrecision:
    value: float
    precision: int = 3

    @property
    def mantissa(self) -> int:
        return int(np.round(self.value/(10**self.exponent)))

    @property
    def exponent(self) -> int:
        abs_value = abs(self.value)
        str_abs_value = self._float_to_string(abs_value)
        pre_decimal = str_abs_value.split('.')[0]
        if pre_decimal == '0':
            post_decimal = str_abs_value.split('.')[-1]
            exp0 = len(post_decimal)-len(post_decimal.lstrip('0'))
            rounded_value = np.round(abs_value * 10**exp0, decimals=self.precision) / 10**exp0
            rounded_post_decimal = self._float_to_string(rounded_value).split('.')[-1]
            if rounded_post_decimal == '0':
                return 0
            return -(len(rounded_post_decimal)-len(rounded_post_decimal.lstrip('0'))+self.precision)
        return len(pre_decimal)-self.precision

    def _float_to_string(self, value: float) -> str:
        str_abs_value = str(value)
        if str_abs_value.count('e') == 1:
            post_decimal_digits = abs(int(str_abs_value.split('e')[-1]))+1+self.precision
            return f'{value:.{post_decimal_digits}f}'
        return str(value)

@dataclass(frozen=True)
class Float3:
    value: FloatPrecision

    @property
    def precision(self) -> int:
        return self.value.precision

    @property
    def mantissa(self) -> float:
        return self.value.mantissa * 10**(self.value.exponent-self.exponent)

    @property
    def exponent(self) -> int:
        return int(3*np.floor((self.precision + self.value.exponent - 1)/3))

@dataclass
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
        3 : 'k',
        6 : 'M',
        9 : 'G',
        12 : 'T'
    })

    @property
    def value3(self) -> Float3:
        return Float3(FloatPrecision(self.value, self.precision))

    def exp_prefix(self, exp) -> str:
        if not self.use_exp_prefix:
            return ''
        if exp > max(self.exp_prefixes.keys()):
            return self.exp_prefixes[max(self.exp_prefixes.keys())]
        if exp < min(self.exp_prefixes.keys()):
            return self.exp_prefixes[min(self.exp_prefixes.keys())]
        if exp in self.exp_prefixes.keys():
            return self.exp_prefixes.get(exp, '')
        return ''

    def exp_extension(self, exp) -> str:
        def rebase_exp(exp: int) -> int:
            if not self.use_exp_prefix:
                return exp
            if not exp in self.exp_prefixes.keys():
                if exp > max(self.exp_prefixes.keys()):
                    return exp - max(self.exp_prefixes.keys())
                if exp < min(self.exp_prefixes.keys()):
                    return exp - min(self.exp_prefixes.keys())
            return 0
        if rebase_exp(exp) == 0:
            return ''
        return f'e{rebase_exp(exp)}'

    def __str__(self) -> str:
        pre_decimal_positions = 0 if np.abs(self.value3.mantissa) < 1 else len(str(abs(self.value3.mantissa)).split('.')[0])
        post_decimal_positions = max(self.precision - pre_decimal_positions, 0)
        pre_decimal = int(self.value3.mantissa)
        pre_decimal_str = f'{pre_decimal:d}'
        post_decimal = int(np.round(self.value3.mantissa % 1 * 10**(post_decimal_positions)))
        post_decimal_str = '' if post_decimal_positions == 0 else f'.{post_decimal:0{post_decimal_positions}d}'
        return f'{pre_decimal_str}{post_decimal_str}{self.exp_extension(self.value3.exponent)}{self.exp_prefix(self.value3.exponent)}{self.unit}'

@dataclass(frozen=True)
class ScientificComplex:
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
                if self.imag.value3.exponent > self.real.value3.exponent:
                    target_exp_prefix = {self.imag.value3.exponent : self.exp_prefixes.get(self.imag.value3.exponent, '')}
                target_exp_prefix = {self.real.value3.exponent : self.exp_prefixes.get(self.real.value3.exponent, '')}
                real = ScientificFloat(self.real.value, self.unit, self.precision, self.use_exp_prefix, target_exp_prefix)
                imag = ScientificFloat(self.imag.value, self.unit, self.precision, self.use_exp_prefix, target_exp_prefix)
                if real.value3.exponent > imag.value3.exponent or imag.value3.mantissa == 0:
                    return f'{self.real_sign}{real.__str__()}'
                if imag.value3.exponent > real.value3.exponent or real.value3.mantissa == 0:
                    sign = '' if self.imag_sign.strip() == '+' else self.imag_sign
                    return f'{sign}j{imag.__str__()}'
                return f'{self.real_sign}{real.__str__()}{self.imag_sign}j{imag.__str__()}'
            return f'{self.real_sign}{self.real.__str__()}{self.imag_sign}j{self.imag.__str__()}'
