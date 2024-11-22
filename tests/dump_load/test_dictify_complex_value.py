from hypothesis import given, strategies as st
from CircuitCalculator.dump_load import dictify_complex_values

@given(st.complex_numbers(allow_nan=False))
def test_dictify_complex(z: complex) -> None:
    data = {'z': z}
    real_data = dictify_complex_values(data)
    assert real_data['z']['real'] == z.real
    assert real_data['z']['imag'] == z.imag