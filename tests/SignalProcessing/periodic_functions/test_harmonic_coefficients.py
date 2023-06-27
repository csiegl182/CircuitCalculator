import pytest
import numpy as np
from hypothesis import given, strategies as st
from CircuitCalculator.SignalProcessing.periodic_functions import fourier_series_mapping, TransformationError

@given(st.floats(min_value=0, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False), st.integers(max_value=-1))
def test_amplitude_method_raises_error_when_passing_negative_index(A, phi, index) -> None:
    for harmonic_implementator in fourier_series_mapping.values():
        harmonic_implementation = harmonic_implementator(A, phi)
        with pytest.raises(ValueError):
            harmonic_implementation.amplitude(index)

@given(st.floats(min_value=0, allow_subnormal=False), st.floats(min_value=0, max_value=2*np.pi, allow_subnormal=False), st.integers(max_value=-1))
def test_phase_method_raises_error_when_passing_negative_index(A, phi, index) -> None:
    for harmonic_implementator in fourier_series_mapping.values():
        harmonic_implementation = harmonic_implementator(A, phi)
        with pytest.raises(ValueError):
            harmonic_implementation.phase(index)