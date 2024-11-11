from CircuitCalculator.dump_load import restore_complex_values

def test_restore_complex_nested_in_dict() -> None:
    z1 = complex(1, 2)
    z2 = complex(3, 4)
    data = {'z1': {'real': z1.real, 'imag': z1.imag}, 'nested': {'z2': {'real': z2.real, 'imag': z2.imag}}}
    restored_data = restore_complex_values(data)
    assert restored_data['z1'] == z1
    assert restored_data['nested']['z2'] == z2

def test_restore_complex_nested_in_list() -> None:
    z1 = complex(1, 2)
    z2 = complex(3, 4)
    data = {'nested': [{'z1': {'real': z1.real, 'imag': z1.imag}}, {'z2': {'real': z2.real, 'imag': z2.imag}}]}
    restored_data = restore_complex_values(data)
    assert restored_data['nested'][0]['z1'] == z1
    assert restored_data['nested'][1]['z2'] == z2