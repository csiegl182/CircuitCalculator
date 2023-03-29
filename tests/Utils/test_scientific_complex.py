from CircuitCalculator.Utils import ScientificComplex

def test_simple_complex_value() -> None:
    z = 3+7j
    str_repr = str(ScientificComplex(z))
    assert str_repr == '3.00 + j7.00'

def test_complex_value_with_negative_imaginary_part() -> None:
    z = 3-7j
    str_repr = str(ScientificComplex(z))
    assert str_repr == '3.00 - j7.00'

def test_complex_value_with_negative_real_part() -> None:
    z = -3+7j
    str_repr = str(ScientificComplex(z))
    assert str_repr == '- 3.00 + j7.00'

def test_complex_value_with_negative_real_part_and_compact_layout() -> None:
    z = -3+7j
    str_repr = str(ScientificComplex(z, compact=True))
    assert str_repr == '-3.00+j7.00'

def test_complex_value_with_dominating_real_part() -> None:
    z = 3+7e-3j
    str_repr = str(ScientificComplex(z))
    assert str_repr == '3.00'

def test_complex_value_with_dominating_imag_part() -> None:
    z = 3e-3+7j
    str_repr = str(ScientificComplex(z))
    assert str_repr == 'j7.00'

def test_complex_value_with_different_scaling() -> None:
    z = 3+7e-3j
    str_repr = str(ScientificComplex(z, hide_minor_part=False))
    assert str_repr == '3.00 + j7.00e-3'

def test_complex_value_with_given_exponential_prefix() -> None:
    z = 3e-3+7e-3j
    str_repr = str(ScientificComplex(z, use_exp_prefix=True))
    assert str_repr == '3.00m + j7.00m'

def test_complex_value_with_different_scaling_and_given_exponential_prefix() -> None:
    z = 3e-3+7e-6j
    str_repr = str(ScientificComplex(z, use_exp_prefix=True))
    assert str_repr == '3.00m'

def test_complex_value_as_polar_in_rad() -> None:
    z = (1+1j)/1.414
    str_repr = str(ScientificComplex(z, polar=True))
    assert str_repr == '1.00∠0.7854'

def test_complex_value_as_polar_in_rad_with_exp_prefix_and_unit() -> None:
    z = (1+1j)/1.414e3
    str_repr = str(ScientificComplex(z, use_exp_prefix=True, unit='W', polar=True))
    assert str_repr == '1.00mW∠0.7854'

def test_complex_value_as_polar_in_deg() -> None:
    z = (1+1j)/1.414
    str_repr = str(ScientificComplex(z, polar=True, deg=True))
    assert str_repr == '1.00∠45.00'

def test_complex_value_hides_small_angles_in_rad() -> None:
    z = 1+0.00001j
    str_repr = str(ScientificComplex(z, polar=True, deg=True))
    assert str_repr == '1.00'

def test_complex_value_hides_small_angles_in_deg() -> None:
    z = 1+0.00001j
    str_repr = str(ScientificComplex(z, polar=True, deg=True))
    assert str_repr == '1.00'

def test_complex_value_hides_zero_imaginary_part() -> None:
    z = 1
    str_repr = str(ScientificComplex(z))
    assert str_repr == '1.00'