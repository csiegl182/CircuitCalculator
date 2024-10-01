import pytest
import numpy as np
from hypothesis import given, strategies as st
from CircuitCalculator.SignalProcessing.periodic_functions import fourier_series_mapping, AbstractHarmonicCoefficients

@given(st.floats(min_value=0, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False), st.integers(max_value=-1))
def test_amplitude_method_raises_error_when_passing_negative_index(A, phi, index) -> None:
    for harmonic_implementator in fourier_series_mapping.values():
        harmonic_implementation = harmonic_implementator(A, phi, 0)
        with pytest.raises(ValueError):
            harmonic_implementation.amplitude(index)

@given(st.floats(min_value=0, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False), st.integers(max_value=-1))
def test_phase_method_raises_error_when_passing_negative_index(A, phi, index) -> None:
    for harmonic_implementator in fourier_series_mapping.values():
        harmonic_implementation = harmonic_implementator(A, phi, 0)
        with pytest.raises(ValueError):
            harmonic_implementation.phase(index)

@given(st.floats(min_value=0, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
def test_real_part_is_correct(A, phi) -> None:
    class HarmonicImplementation(AbstractHarmonicCoefficients):
        def _amplitude_coefficient(self, _):
            return self.amplitude0
        def _phase_coefficient(self, _):
            return self.phase0
    hi = HarmonicImplementation(A, phi)
    assert hi.real(0) == A*np.cos(phi)

@given(st.floats(min_value=0, allow_subnormal=False, allow_infinity=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
def test_imag_part_is_correct(A, phi) -> None:
    class HarmonicImplementation(AbstractHarmonicCoefficients):
        def _amplitude_coefficient(self, _):
            return self.amplitude0
        def _phase_coefficient(self, _):
            return self.phase0
    hi = HarmonicImplementation(A, phi)
    assert hi.imag(0) == A*np.sin(phi)

@given(st.floats(min_value=0, allow_subnormal=False, allow_infinity=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False))
def test_complex_part_is_correct(A, phi) -> None:
    class HarmonicImplementation(AbstractHarmonicCoefficients):
        def _amplitude_coefficient(self, _):
            return self.amplitude0
        def _phase_coefficient(self, _):
            return self.phase0
    hi = HarmonicImplementation(A, phi)
    assert hi.c(0) == A/2*np.exp(-1j*phi)