from hypothesis import given, strategies as st
from CircuitCalculator.SignalProcessing.periodic_functions import CosFunction, SinFunction, fourier_series, PeriodicFunction, RectFunction, TriFunction, SawFunction
import numpy as np

def calc_fourier_coefficients_via_integration(p_fcn: PeriodicFunction, num_f_samples: int, num_t_samples: int = 1000) -> tuple[np.ndarray, np.ndarray]:
    T = p_fcn.period
    w = 2*np.pi/T
    t = np.linspace(0, T, num_t_samples)
    dt = t[1]-t[0]

    an = np.array([2/T*np.trapz(p_fcn.time_function(t)*np.cos(n*w*t), dx=dt) for n in range(num_f_samples)])
    bn = np.array([2/T*np.trapz(p_fcn.time_function(t)*np.sin(n*w*t), dx=dt) for n in range(num_f_samples)])
    return (an, bn)

@given(st.floats(min_value=0.001, max_value=10, allow_subnormal=False, allow_infinity=False), st.floats(min_value=0.001, max_value=1e6, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
def test_first_100_coefficients_of_cos_function(T:float, A:float, phi:float) -> None:
    cos_fcn = CosFunction(T, A, phi)
    cos_coef = fourier_series(cos_fcn)

    an, bn = calc_fourier_coefficients_via_integration(cos_fcn, 100)
        
    np.testing.assert_allclose(an, [cos_coef.amplitude(n)*np.cos(cos_coef.phase(n)) for n in range(100)], atol=1e-2, rtol=1e-3)
    np.testing.assert_allclose(bn, [cos_coef.amplitude(n)*np.sin(cos_coef.phase(n)) for n in range(100)], atol=1e-2, rtol=1e-3)

@given(st.floats(min_value=0.001, max_value=10, allow_subnormal=False, allow_infinity=False), st.floats(min_value=0.001, max_value=1e6, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
def test_first_100_coefficients_of_sin_function(T:float, A:float, phi:float) -> None:
    sin_fcn = SinFunction(T, A, phi)
    sin_coef = fourier_series(sin_fcn)

    an, bn = calc_fourier_coefficients_via_integration(sin_fcn, 100)
        
    np.testing.assert_allclose(an, [sin_coef.amplitude(n)*np.cos(sin_coef.phase(n)) for n in range(100)], atol=1e-2, rtol=1e-3)
    np.testing.assert_allclose(bn, [sin_coef.amplitude(n)*np.sin(sin_coef.phase(n)) for n in range(100)], atol=1e-2, rtol=1e-3)

@given(st.floats(min_value=0.001, max_value=10, allow_subnormal=False, allow_infinity=False), st.floats(min_value=0.001, max_value=3, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
def test_first_100_coefficients_of_rect_function(T:float, A:float, phi:float) -> None:
    rect_fcn = RectFunction(T, A, phi)
    rect_coef = fourier_series(rect_fcn)

    an, bn = calc_fourier_coefficients_via_integration(rect_fcn, 100)
        
    np.testing.assert_allclose([rect_coef.amplitude(n)*np.cos(rect_coef.phase(n)) for n in range(100)], an, atol=1e-2, rtol=1e-3)
    np.testing.assert_allclose([rect_coef.amplitude(n)*np.sin(rect_coef.phase(n)) for n in range(100)], bn, atol=1e-2, rtol=1e-3)

@given(st.floats(min_value=0.001, max_value=10, allow_subnormal=False, allow_infinity=False), st.floats(min_value=0.001, max_value=4e3, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
def test_first_20_coefficients_of_tri_function(T:float, A:float, phi:float) -> None:
    tri_fcn = TriFunction(T, A, phi)
    tri_coef = fourier_series(tri_fcn)

    an, bn = calc_fourier_coefficients_via_integration(tri_fcn, 20)
        
    np.testing.assert_allclose(an, [tri_coef.amplitude(n)*np.cos(tri_coef.phase(n)) for n in range(20)], atol=1e-2, rtol=1e-3)
    np.testing.assert_allclose(bn, [tri_coef.amplitude(n)*np.sin(tri_coef.phase(n)) for n in range(20)], atol=1e-2, rtol=1e-3)

# @given(st.floats(min_value=0.001, max_value=10, allow_subnormal=False, allow_infinity=False), st.floats(min_value=0.001, max_value=3, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
# def test_first_100_coefficients_of_saw_function(T:float, A:float, phi:float) -> None:
def test_first_100_coefficients_of_saw_function() -> None:
    T =.1
    A = 1
    phi = 0
    saw_fcn = SawFunction(T, A, phi)
    saw_coef = fourier_series(saw_fcn)

    an, bn = calc_fourier_coefficients_via_integration(saw_fcn, 100)
        
    np.testing.assert_allclose([saw_coef.amplitude(n)*np.cos(saw_coef.phase(n)) for n in range(100)], an, atol=1e-2, rtol=1e-3)
    np.testing.assert_allclose([saw_coef.amplitude(n)*np.sin(saw_coef.phase(n)) for n in range(100)], bn, atol=1e-2, rtol=1e-3)