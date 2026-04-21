import numpy as np
from hypothesis import given, strategies as st
from CircuitCalculator.SignalProcessing.periodic_functions import AbstractHarmonicCoefficients


AMPLITUDES = st.floats(
    min_value=0,
    max_value=1e6,
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


class HarmonicImplementation(AbstractHarmonicCoefficients):
    def _amplitude_coefficient(self, _):
        return self.amplitude0

    def _phase_coefficient(self, _):
        return self.phase0


@given(AMPLITUDES, PHASES)
def test_a_coefficient_is_correct(A, phi) -> None:
    hi = HarmonicImplementation(A, phi)
    np.testing.assert_allclose(
        hi.a(0),
        A*np.cos(phi),
        atol=1e-12,
        rtol=1e-12,
    )


@given(AMPLITUDES, PHASES)
def test_b_coefficient_is_correct(A, phi) -> None:
    hi = HarmonicImplementation(A, phi)
    np.testing.assert_allclose(
        hi.b(0),
        -A*np.sin(phi),
        atol=1e-12,
        rtol=1e-12,
    )


@given(AMPLITUDES, PHASES)
def test_complex_part_is_correct(A, phi) -> None:
    hi = HarmonicImplementation(A, phi)
    np.testing.assert_allclose(
        hi.c(0),
        A/2*np.exp(1j*phi),
        atol=1e-12,
        rtol=1e-12,
    )
