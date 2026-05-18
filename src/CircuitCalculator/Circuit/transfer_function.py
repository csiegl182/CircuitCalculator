from dataclasses import dataclass
from typing import Literal

import numpy as np
from scipy import signal
import sympy as sp

from .circuit import Circuit
from .state_space_model import numeric_state_space_model_constructor, symbolic_state_space_model_constructor


class TransferFunctionError(ValueError):
    ...


@dataclass(frozen=True)
class TransferFunctionOutput:
    kind: Literal["voltage", "current", "potential"]
    id: str

    @classmethod
    def voltage(cls, component_id: str) -> "TransferFunctionOutput":
        return cls(kind="voltage", id=component_id)

    @classmethod
    def current(cls, component_id: str) -> "TransferFunctionOutput":
        return cls(kind="current", id=component_id)

    @classmethod
    def potential(cls, node_id: str) -> "TransferFunctionOutput":
        return cls(kind="potential", id=node_id)


@dataclass(frozen=True)
class SymbolicTransferFunction:
    expr: sp.Expr
    input_id: str
    output: TransferFunctionOutput
    s: sp.Symbol

    def numerator(self) -> sp.Expr:
        return sp.expand(sp.fraction(sp.together(self.expr))[0])

    def denominator(self) -> sp.Expr:
        return sp.expand(sp.fraction(sp.together(self.expr))[1])

    def zeros(self) -> list[sp.Expr]:
        numerator = self.numerator()
        if numerator == 0:
            return []
        return list(sp.roots(sp.Poly(numerator, self.s), self.s).keys())

    def poles(self) -> list[sp.Expr]:
        denominator = self.denominator()
        if denominator == 0:
            return []
        return list(sp.roots(sp.Poly(denominator, self.s), self.s).keys())


@dataclass(frozen=True)
class NumericTransferFunction:
    numerator_coeffs: np.ndarray
    denominator_coeffs: np.ndarray
    input_id: str
    output: TransferFunctionOutput

    def transfer_function(self) -> signal.TransferFunction:
        return signal.TransferFunction(self.numerator_coeffs, self.denominator_coeffs)

    def zeros(self) -> np.ndarray:
        return np.roots(self.numerator_coeffs) if self.numerator_coeffs.size > 1 else np.array([], dtype=complex)

    def poles(self) -> np.ndarray:
        return np.roots(self.denominator_coeffs)


def _trim_leading_small_coefficients(coeffs: np.ndarray, atol: float = 1e-12) -> np.ndarray:
    idx = 0
    while idx < coeffs.size - 1 and abs(coeffs[idx]) <= atol:
        idx += 1
    return coeffs[idx:]


def _validate_and_select_output(constructor, input_id: str, output: TransferFunctionOutput):
    sources = constructor.sources

    if input_id not in sources:
        raise TransferFunctionError(
            f'Input "{input_id}" is not an independent source of the state-space model. '
            f'Available inputs are: {sources}.'
        )

    if output.kind == "voltage":
        c_row, d_row = constructor.c_d_row_for_voltage(output.id)
    elif output.kind == "current":
        c_row, d_row = constructor.c_d_row_for_current(output.id)
    elif output.kind == "potential":
        c_row, d_row = constructor.c_d_row_for_potential(output.id)
    else:
        raise TransferFunctionError(f'Unsupported output kind "{output.kind}".')

    return sources.index(input_id), c_row, d_row


def numeric_transfer_function(
        circuit: Circuit,
        input_id: str,
        output: TransferFunctionOutput) -> NumericTransferFunction:
    constructor = numeric_state_space_model_constructor(circuit)
    input_idx, c_row, d_row = _validate_and_select_output(constructor, input_id, output)

    if constructor.A.shape[0] == 0:
        numerator_coeffs = np.array([float(d_row[0, input_idx])], dtype=float)
        denominator_coeffs = np.array([1.0], dtype=float)
    else:
        A = np.asarray(np.real_if_close(constructor.A), dtype=float)
        B = np.asarray(np.real_if_close(constructor.B), dtype=float)
        C = np.asarray(np.real_if_close(c_row), dtype=float)
        D = np.asarray(np.real_if_close(d_row), dtype=float)
        numerator_coeffs, denominator_coeffs = signal.ss2tf(
            A,
            B,
            C,
            D,
            input=input_idx
        )
        numerator_coeffs = np.asarray(numerator_coeffs[0], dtype=float)
        denominator_coeffs = np.asarray(denominator_coeffs, dtype=float)

    return NumericTransferFunction(
        numerator_coeffs=_trim_leading_small_coefficients(numerator_coeffs) if np.any(numerator_coeffs) else np.array([0.0]),
        denominator_coeffs=_trim_leading_small_coefficients(denominator_coeffs) if np.any(denominator_coeffs) else np.array([1.0]),
        input_id=input_id,
        output=output
    )


def symbolic_transfer_function(
        circuit: Circuit,
        input_id: str,
        output: TransferFunctionOutput,
        s: sp.Symbol = sp.Symbol("s", complex=True)) -> SymbolicTransferFunction:
    constructor = symbolic_state_space_model_constructor(circuit)
    input_idx, c_row, d_row = _validate_and_select_output(constructor, input_id, output)
    if constructor.A.shape[0] == 0:
        expr = d_row[0, input_idx]
    else:
        identity = sp.eye(constructor.A.shape[0])
        b_col = constructor.B[:, input_idx:input_idx+1]
        expr = (c_row * (s * identity - constructor.A).inv() * b_col + d_row[:, input_idx:input_idx+1])[0, 0]

    return SymbolicTransferFunction(
        expr=sp.nsimplify(sp.factor(expr)),
        input_id=input_id,
        output=output,
        s=s
    )
