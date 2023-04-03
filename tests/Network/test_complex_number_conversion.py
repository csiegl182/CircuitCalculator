import pytest
from CircuitCalculator.Network.loaders import to_complex, FileFormatError
import numpy as np

def test_real_imag_dict_converts_to_complex_number() -> None:
    z = 12 + 33j
    d = {'real' : z.real, 'imag' : z.imag} 
    np.testing.assert_almost_equal(to_complex(d), z)

def test_abs_phase_dict_converts_to_complex_number() -> None:
    z = 12 + 33j
    d = {'abs' : abs(z), 'phase' : np.angle(z)}
    np.testing.assert_almost_equal(to_complex(d), z)

def test_abs_phase_dict_with_degree_converts_to_complex_number() -> None:
    z = 12 + 33j
    d = {'abs' : abs(z), 'phase' : np.angle(z)/np.pi*180}
    np.testing.assert_almost_equal(to_complex(d, degree=True), z)

def test_incorrect_values_lead_to_error() -> None:
    with pytest.raises(FileFormatError):
        to_complex({'foo' : 12, 'bar' : 18})

