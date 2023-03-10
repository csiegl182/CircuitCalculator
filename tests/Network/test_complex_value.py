from hypothesis import given, strategies as st
from CircuitCalculator.Network.elements import complex_value
import numpy as np

@given(st.floats(min_value=0, allow_subnormal=False), st.floats(allow_nan=False, allow_infinity=False))
def test_complex_value_calculates_absolute_value(X: float, phi: float) -> None:
    z = complex_value(X, phi)
    np.testing.assert_approx_equal(np.abs(z), X)

@given(st.floats(min_value=1e-7, exclude_min=True, allow_infinity=False, allow_subnormal=False), st.floats(min_value=-np.pi, max_value=np.pi, exclude_min=True, allow_subnormal=False))
def test_complex_value_calculates_correct_phase(X: float, phi: float) -> None:
    z = complex_value(X, phi)
    np.testing.assert_approx_equal(np.angle(z), phi)

@given(st.floats(max_value=-1e-7, allow_infinity=False), st.floats(min_value=-np.pi, max_value=np.pi))
def test_complex_value_adds_pi_on_phase_on_negative_amplitude(X: float, phi: float) -> None:
    z = complex_value(X, phi)
    np.testing.assert_approx_equal(np.abs(np.angle(z) - phi), np.pi)

@given(st.floats(min_value=-np.pi, max_value=np.pi))
def test_complex_value_with_infinite_amplitude_returns_infinite_real_value_and_zero_imag_value(phi) -> None:
    z = complex_value(np.inf, phi)
    assert z.real == np.inf
    assert z.imag == 0

@given(st.floats(min_value=-np.pi, max_value=np.pi))
def test_complex_value_with_infinite_amplitude_returns_zero_phase(phi) -> None:
    z = complex_value(np.inf, phi)
    assert np.angle(z) == 0

@given(st.floats(min_value=-np.pi+0.001, max_value=np.pi-0.001, exclude_min=True, exclude_max=True), st.integers(min_value=-5, max_value=5))
def test_complex_value_reduces_phase_to_minus_pi_to_pi(phi, n) -> None:
    z = complex_value(1, phi+n*2*np.pi)
    np.testing.assert_almost_equal(np.angle(z), phi, decimal=3)

@given(st.floats(min_value=0, allow_infinity=False), st.floats(allow_nan=False, allow_infinity=False))
def test_complex_value_can_handle_rms_values(X, phi) -> None:
    z = complex_value(X, phi, rms=True)
    np.testing.assert_approx_equal(np.abs(z), X*np.sqrt(2))

@given(st.floats(min_value=-180, max_value=180, allow_nan=False, allow_infinity=False))
def test_complex_value_can_handle_degree_phases(phi) -> None:
    z = complex_value(1, phi, deg=True)
    np.testing.assert_approx_equal(np.degrees(np.angle(z)), phi)
