import numpy as np
import pytest
from hypothesis import given, settings, strategies as st

from CircuitCalculator.SignalProcessing.periodic_functions import (
    CosFunction,
    PeriodicFunction,
    RectFunction,
    SawFunction,
    SinFunction,
    TriFunction,
    fourier_series,
)

PERIODS = st.floats(
    min_value=0.001,
    max_value=10,
    allow_nan=False,
    allow_infinity=False,
    allow_subnormal=False,
)
AMPLITUDES = st.floats(
    min_value=0.001,
    max_value=1e3,
    allow_nan=False,
    allow_infinity=False,
    allow_subnormal=False,
)
OFFSETS = st.floats(
    min_value=-10,
    max_value=10,
    allow_nan=False,
    allow_infinity=False,
    allow_subnormal=False,
)
PHASES = st.floats(
    min_value=0,
    max_value=2*np.pi,
    allow_nan=False,
    allow_infinity=False,
    allow_subnormal=False,
)

trapezoid = getattr(np, 'trapezoid', None)
if trapezoid is None:
    trapezoid = np.trapz


def calc_fourier_coefficients_via_integration(
    p_fcn: PeriodicFunction,
    num_f_samples: int,
    num_t_samples: int = 1000,
) -> tuple[np.ndarray, np.ndarray]:
    T = p_fcn.period
    w = 2*np.pi/T
    t = np.linspace(0, T, num_t_samples)
    dt = t[1]-t[0]
    y = p_fcn.time_function(t)

    an = np.array(
        [2/T*trapezoid(y*np.cos(n*w*t), dx=dt) for n in range(num_f_samples)]
    )
    bn = np.array(
        [2/T*trapezoid(y*np.sin(n*w*t), dx=dt) for n in range(num_f_samples)]
    )
    return (an, bn)


def assert_coefficients(
    coef,
    n: int,
    expected_amplitude: float,
    expected_phase: float = 0,
) -> None:
    np.testing.assert_allclose(
        coef.a(n),
        expected_amplitude*np.cos(expected_phase),
        atol=1e-12,
        rtol=1e-12,
        err_msg=f"a({n})",
    )
    np.testing.assert_allclose(
        coef.b(n),
        -expected_amplitude*np.sin(expected_phase),
        atol=1e-12,
        rtol=1e-12,
        err_msg=f"b({n})",
    )


@settings(deadline=None)
@given(PERIODS, AMPLITUDES, PHASES, OFFSETS)
def test_first_100_ab_coefficients_of_cos_function(
    T: float,
    A: float,
    phi: float,
    offset: float,
) -> None:
    cos_coef = fourier_series(CosFunction(T, A, phi, offset))

    for n in range(100):
        if n == 0:
            assert_coefficients(cos_coef, n, offset)
        elif n == 1:
            assert_coefficients(cos_coef, n, A, phi)
        else:
            assert_coefficients(cos_coef, n, 0)


@settings(deadline=None)
@given(PERIODS, AMPLITUDES, PHASES, OFFSETS)
def test_first_100_ab_coefficients_of_sin_function(
    T: float,
    A: float,
    phi: float,
    offset: float,
) -> None:
    sin_coef = fourier_series(SinFunction(T, A, phi, offset))

    for n in range(100):
        if n == 0:
            assert_coefficients(sin_coef, n, offset)
        elif n == 1:
            assert_coefficients(sin_coef, n, A, -np.pi/2+phi)
        else:
            assert_coefficients(sin_coef, n, 0)


@settings(deadline=None)
@given(PERIODS, AMPLITUDES, PHASES, OFFSETS)
def test_first_100_ab_coefficients_of_rect_function(
    T: float,
    A: float,
    phi: float,
    offset: float,
) -> None:
    rect_coef = fourier_series(RectFunction(T, A, phi, offset))

    for n in range(100):
        if n == 0:
            assert_coefficients(rect_coef, n, offset)
        elif n % 2 == 0:
            assert_coefficients(rect_coef, n, 0)
        else:
            assert_coefficients(rect_coef, n, 4/n/np.pi*A, -np.pi/2+n*phi)


@settings(deadline=None)
@given(PERIODS, AMPLITUDES, PHASES, OFFSETS)
def test_first_20_ab_coefficients_of_tri_function(
    T: float,
    A: float,
    phi: float,
    offset: float,
) -> None:
    tri_coef = fourier_series(TriFunction(T, A, phi, offset))

    for n in range(20):
        if n == 0:
            assert_coefficients(tri_coef, n, offset)
        elif n % 2 == 0:
            assert_coefficients(tri_coef, n, 0)
        else:
            assert_coefficients(tri_coef, n, 8/n/n/np.pi/np.pi*A, n*phi)


@settings(deadline=None)
@given(PERIODS, AMPLITUDES, PHASES, OFFSETS)
def test_first_20_ab_coefficients_of_saw_function(
    T: float,
    A: float,
    phi: float,
    offset: float,
) -> None:
    saw_coef = fourier_series(SawFunction(T, A, phi, offset))

    for n in range(20):
        if n == 0:
            assert_coefficients(saw_coef, n, offset)
        else:
            assert_coefficients(saw_coef, n, -2/n/np.pi*A, -np.pi/2+n*phi)


@pytest.mark.parametrize(
    ("periodic_function", "num_f_samples"),
    [
        (CosFunction(1.3, 1.25, 0.7, -0.2), 10),
        (SinFunction(1.3, 1.25, 0.7, -0.2), 10),
        (RectFunction(1.3, 1.25, 0.7, -0.2), 10),
        (TriFunction(1.3, 1.25, 0.7, -0.2), 10),
        (SawFunction(1.3, 1.25, 0.7, -0.2), 10),
    ],
)
def test_representative_coefficients_match_numerical_integration(
    periodic_function: PeriodicFunction,
    num_f_samples: int,
) -> None:
    coef = fourier_series(periodic_function)

    an, bn = calc_fourier_coefficients_via_integration(
        periodic_function,
        num_f_samples,
        num_t_samples=20000,
    )
    an[0] /= 2

    np.testing.assert_allclose(
        an,
        [coef.a(n) for n in range(num_f_samples)],
        atol=1e-3,
        rtol=1e-3,
    )
    np.testing.assert_allclose(
        bn,
        [coef.b(n) for n in range(num_f_samples)],
        atol=1e-3,
        rtol=1e-3,
    )
