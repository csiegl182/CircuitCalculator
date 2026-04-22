from numpy.testing import assert_almost_equal

from CircuitCalculator.Circuit import terminal_analysis as ta
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit.Components import components as cp


def voltage_divider_circuit() -> Circuit:
    return Circuit(
        components=[
            cp.dc_voltage_source(V=12, id='V', nodes=('1', '0')),
            cp.resistor(R=100, id='R1', nodes=('1', '2')),
            cp.resistor(R=200, id='R2', nodes=('2', '0'))
        ],
        ground_node='0'
    )


def test_open_circuit_voltage_can_be_calculated_for_circuit() -> None:
    voltage = ta.open_circuit_voltage(voltage_divider_circuit(), '2', '0')

    assert_almost_equal(voltage, 8)


def test_short_circuit_current_can_be_calculated_for_circuit() -> None:
    current = ta.short_circuit_current(voltage_divider_circuit(), '2', '0')

    assert_almost_equal(current, 0.12)


def test_thevenin_parameters_can_be_calculated_for_circuit() -> None:
    thevenin = ta.thevenin_parameters(voltage_divider_circuit(), '2', '0')

    assert_almost_equal(thevenin.open_circuit_voltage, 8)
    assert_almost_equal(thevenin.impedance, 100*200/(100+200))
    assert_almost_equal(thevenin.short_circuit_current, 0.12)
    assert_almost_equal(thevenin.admittance, 1/(100*200/(100+200)))


def test_equivalent_source_parameters_can_be_created_from_thevenin_parameters() -> None:
    parameters = ta.EquivalentSourceParameters.from_thevenin_parameters(
        open_circuit_voltage=8,
        impedance=100*200/(100+200)
    )

    assert_almost_equal(parameters.open_circuit_voltage, 8)
    assert_almost_equal(parameters.short_circuit_current, 0.12)
    assert_almost_equal(parameters.impedance, 100*200/(100+200))
    assert_almost_equal(parameters.admittance, 1/(100*200/(100+200)))


def test_norten_parameters_can_be_calculated_for_circuit() -> None:
    norten = ta.norten_parameters(voltage_divider_circuit(), '2', '0')

    assert_almost_equal(norten.open_circuit_voltage, 8)
    assert_almost_equal(norten.short_circuit_current, 0.12)
    assert_almost_equal(norten.impedance, 100*200/(100+200))
    assert_almost_equal(norten.admittance, 1/(100*200/(100+200)))


def test_equivalent_source_parameters_can_be_created_from_norton_parameters() -> None:
    parameters = ta.EquivalentSourceParameters.from_norton_parameters(
        short_circuit_current=0.12,
        admittance=1/(100*200/(100+200))
    )

    assert_almost_equal(parameters.open_circuit_voltage, 8)
    assert_almost_equal(parameters.short_circuit_current, 0.12)
    assert_almost_equal(parameters.impedance, 100*200/(100+200))
    assert_almost_equal(parameters.admittance, 1/(100*200/(100+200)))


def test_norton_alias_can_be_used_for_circuit() -> None:
    norten = ta.norton_parameters(voltage_divider_circuit(), '2', '0')

    assert_almost_equal(norten.short_circuit_current, 0.12)


def test_frequency_parameter_selects_operating_point() -> None:
    voltage = ta.open_circuit_voltage(voltage_divider_circuit(), '2', '0', w=1)

    assert_almost_equal(voltage, 0)
