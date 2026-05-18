import numpy as np
import pytest
import sympy as sp

from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit.transfer_function import (
    numeric_transfer_function,
    TransferFunctionError,
    TransferFunctionOutput,
    symbolic_transfer_function,
)
import CircuitCalculator.Circuit.Components.symbolic_components as cmp
from CircuitCalculator.Circuit.Components import components as ncmp


def named_symbol(expr: sp.Expr, name: str) -> sp.Symbol:
    return next(symbol for symbol in expr.free_symbols if symbol.name == name)


def assert_transfer_functions_equal(actual: sp.Expr, expected: sp.Expr) -> None:
    assert sp.simplify(sp.nsimplify(actual) - expected).equals(0)


def test_rc_low_pass_voltage_transfer_function_matches_reference_formula() -> None:
    circuit = Circuit(
        components=[
            cmp.voltage_source(id="Vs", V="Vs", nodes=("1", "0")),
            cmp.resistor(id="R1", R="R1", nodes=("1", "2")),
            cmp.capacitor(id="C1", C="C1", nodes=("2", "0")),
        ],
        ground_node="0",
    )

    h = symbolic_transfer_function(circuit, input_id="Vs", output=TransferFunctionOutput.voltage("C1"))
    s = h.s
    r1 = named_symbol(h.expr, "R1")
    c1 = named_symbol(h.expr, "C1")

    assert_transfer_functions_equal(h.expr, 1 / (1 + s * r1 * c1))


def test_rc_low_pass_potential_transfer_function_matches_capacitor_voltage() -> None:
    circuit = Circuit(
        components=[
            cmp.voltage_source(id="Vs", V="Vs", nodes=("1", "0")),
            cmp.resistor(id="R1", R="R1", nodes=("1", "2")),
            cmp.capacitor(id="C1", C="C1", nodes=("2", "0")),
        ],
        ground_node="0",
    )

    h = symbolic_transfer_function(circuit, input_id="Vs", output=TransferFunctionOutput.potential("2"))
    s = h.s
    r1 = named_symbol(h.expr, "R1")
    c1 = named_symbol(h.expr, "C1")

    assert_transfer_functions_equal(h.expr, 1 / (1 + s * r1 * c1))


def test_rl_low_pass_voltage_transfer_function_matches_reference_formula() -> None:
    circuit = Circuit(
        components=[
            cmp.voltage_source(id="Vs", V="Vs", nodes=("1", "0")),
            cmp.inductor(id="L1", L="L1", nodes=("1", "2")),
            cmp.resistor(id="R1", R="R1", nodes=("2", "0")),
        ],
        ground_node="0",
    )

    h = symbolic_transfer_function(circuit, input_id="Vs", output=TransferFunctionOutput.voltage("R1"))
    s = h.s
    r1 = named_symbol(h.expr, "R1")
    l1 = named_symbol(h.expr, "L1")

    assert_transfer_functions_equal(h.expr, r1 / (s * l1 + r1))


def test_numeric_transfer_function_matches_rc_reference_coefficients() -> None:
    circuit = Circuit(
        components=[
            ncmp.dc_voltage_source(id="Vs", V=1.0, nodes=("1", "0")),
            ncmp.resistor(id="R1", R=10.0, nodes=("1", "2")),
            ncmp.capacitor(id="C1", C=2e-3, nodes=("2", "0")),
        ],
        ground_node="0",
    )

    h = numeric_transfer_function(circuit, input_id="Vs", output=TransferFunctionOutput.voltage("C1"))

    np.testing.assert_allclose(h.numerator_coeffs, np.array([50.0]))
    np.testing.assert_allclose(h.denominator_coeffs, np.array([1.0, 50.0]))
    np.testing.assert_allclose(h.poles(), np.array([-50.0]))
    assert h.zeros().size == 0


def test_numeric_transfer_function_matches_example_circuit_capacitor_voltage() -> None:
    circuit = Circuit(
        components=[
            ncmp.dc_voltage_source(id="Uq", V=5.0, nodes=("1", "0")),
            ncmp.resistor(id="R1", R=10.0, nodes=("1", "2")),
            ncmp.resistor(id="R2", R=20.0, nodes=("2", "0")),
            ncmp.resistor(id="R3", R=30.0, nodes=("2", "3")),
            ncmp.capacitor(id="C", C=1e-3, nodes=("3", "0")),
        ],
        ground_node="0",
    )

    h = numeric_transfer_function(circuit, input_id="Uq", output=TransferFunctionOutput.voltage("C"))

    np.testing.assert_allclose(h.numerator_coeffs, np.array([200.0 / 11.0]))
    np.testing.assert_allclose(h.denominator_coeffs, np.array([1.0, 300.0 / 11.0]))
    np.testing.assert_allclose(h.poles(), np.array([-300.0 / 11.0]))


def test_non_source_input_is_rejected() -> None:
    circuit = Circuit(
        components=[
            cmp.voltage_source(id="Vs", V="Vs", nodes=("1", "0")),
            cmp.resistor(id="R1", R="R1", nodes=("1", "2")),
            cmp.capacitor(id="C1", C="C1", nodes=("2", "0")),
        ],
        ground_node="0",
    )

    with pytest.raises(TransferFunctionError):
        symbolic_transfer_function(circuit, input_id="R1", output=TransferFunctionOutput.voltage("C1"))

    numeric_circuit = Circuit(
        components=[
            ncmp.dc_voltage_source(id="Vs", V=1.0, nodes=("1", "0")),
            ncmp.resistor(id="R1", R=10.0, nodes=("1", "2")),
            ncmp.capacitor(id="C1", C=1e-3, nodes=("2", "0")),
        ],
        ground_node="0",
    )

    with pytest.raises(TransferFunctionError):
        numeric_transfer_function(numeric_circuit, input_id="R1", output=TransferFunctionOutput.voltage("C1"))
