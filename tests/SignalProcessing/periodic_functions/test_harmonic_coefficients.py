import pytest
import numpy as np
from hypothesis import given, strategies as st
from CircuitCalculator.SignalProcessing.periodic_functions import fourier_series_mapping, AbstractHarmonicCoefficients

@given(st.floats(min_value=0, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
def test_a_coefficient_is_correct(A, phi) -> None:
    class HarmonicImplementation(AbstractHarmonicCoefficients):
        def _amplitude_coefficient(self, _):
            return self.amplitude0
        def _phase_coefficient(self, _):
            return self.phase0
    hi = HarmonicImplementation(A, phi)
    assert hi.a(0) == A*np.cos(phi)

@given(st.floats(min_value=0, allow_subnormal=False, allow_infinity=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
def test_b_coefficient_is_correct(A, phi) -> None:
    class HarmonicImplementation(AbstractHarmonicCoefficients):
        def _amplitude_coefficient(self, _):
            return self.amplitude0
        def _phase_coefficient(self, _):
            return self.phase0
    hi = HarmonicImplementation(A, phi)
    assert hi.b(0) == -A*np.sin(phi)

@given(st.floats(min_value=0, allow_subnormal=False, allow_infinity=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
def test_complex_part_is_correct(A, phi) -> None:
    class HarmonicImplementation(AbstractHarmonicCoefficients):
        def _amplitude_coefficient(self, _):
            return self.amplitude0
        def _phase_coefficient(self, _):
            return self.phase0
    hi = HarmonicImplementation(A, phi)
    assert hi.c(0) == A/2*np.exp(1j*phi)