import pytest
from hypothesis import given, strategies as st
from CircuitCalculator.SignalProcessing.periodic_functions import CosFunction, fourier_series, PeriodicFunction, RectFunction
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
    np.testing.assert_allclose(bn, [-cos_coef.amplitude(n)*np.sin(cos_coef.phase(n)) for n in range(100)], atol=1e-2, rtol=1e-3)

@given(st.floats(min_value=0.001, max_value=10, allow_subnormal=False, allow_infinity=False), st.floats(min_value=0.001, max_value=3, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
def test_first_100_coefficients_of_rect_function(T:float, A:float, phi:float) -> None:
    rect_fcn = RectFunction(T, A, phi)
    rect_coef = fourier_series(rect_fcn)

    an, bn = calc_fourier_coefficients_via_integration(rect_fcn, 100)
        
    np.testing.assert_allclose([rect_coef.amplitude(n)*np.cos(rect_coef.phase(n)) for n in range(100)], an, atol=1e-2, rtol=1e-3)
    np.testing.assert_allclose([-rect_coef.amplitude(n)*np.sin(rect_coef.phase(n)) for n in range(100)], bn, atol=1e-2, rtol=1e-3)
