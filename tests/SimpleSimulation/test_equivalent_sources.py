import json

from numpy.testing import assert_almost_equal

from CircuitCalculator.SimpleSimulation import equivalent_sources as es


def voltage_divider_simulation_data() -> dict:
    return {
        'circuit': {
            'unit': 5,
            'elements': [
                {
                    'type': 'voltage_source',
                    'V': 12,
                    'name': 'V',
                    'reverse': True,
                    'direction': 'up'
                },
                {
                    'type': 'resistor',
                    'R': 100,
                    'name': 'R1',
                    'direction': 'right'
                },
                {
                    'type': 'node',
                    'name': 'out',
                    'id_loc': 'SE'
                },
                {
                    'type': 'resistor',
                    'R': 200,
                    'name': 'R2',
                    'direction': 'down'
                },
                {
                    'type': 'line',
                    'direction': 'left'
                },
                {
                    'type': 'ground',
                    'name': '0'
                }
            ]
        }
    }


def test_thevenin_parameters_can_be_calculated_from_simple_simulation_data() -> None:
    thevenin = es.thevenin_parameters(voltage_divider_simulation_data(), 'out', '0')

    assert_almost_equal(thevenin.open_circuit_voltage, 8)
    assert_almost_equal(thevenin.impedance, 100*200/(100+200))


def test_norten_parameters_can_be_calculated_from_simple_simulation_data() -> None:
    norten = es.norten_parameters(voltage_divider_simulation_data(), 'out', '0')

    assert_almost_equal(norten.short_circuit_current, 0.12)
    assert_almost_equal(norten.admittance, 1/(100*200/(100+200)))


def test_norton_alias_can_be_calculated_from_simple_simulation_data() -> None:
    norten = es.norton_parameters(voltage_divider_simulation_data(), 'out', '0')

    assert_almost_equal(norten.short_circuit_current, 0.12)


def test_thevenin_parameters_can_be_calculated_from_simple_simulation_json_file(tmp_path) -> None:
    simulation_file = tmp_path / 'voltage_divider.json'
    simulation_file.write_text(json.dumps(voltage_divider_simulation_data()))

    thevenin = es.thevenin_parameters(str(simulation_file), 'out', '0')

    assert_almost_equal(thevenin.open_circuit_voltage, 8)
    assert_almost_equal(thevenin.impedance, 100*200/(100+200))


def test_norten_parameters_can_be_calculated_from_simple_simulation_json_file(tmp_path) -> None:
    simulation_file = tmp_path / 'voltage_divider.json'
    simulation_file.write_text(json.dumps(voltage_divider_simulation_data()))

    norten = es.norten_parameters(str(simulation_file), 'out', '0')

    assert_almost_equal(norten.short_circuit_current, 0.12)
    assert_almost_equal(norten.admittance, 1/(100*200/(100+200)))
