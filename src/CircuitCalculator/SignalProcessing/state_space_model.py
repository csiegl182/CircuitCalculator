import numpy as np
import sympy as sp
from dataclasses import dataclass
import scipy.signal
from typing import Protocol, Any

@dataclass(frozen=True)
class StateSpaceModel(Protocol):
    A: Any
    B: Any
    C: Any
    D: Any

    @property
    def n_states(self) -> int: ...

    @property
    def n_inputs(self) -> int: ...

    @property
    def n_outputs(self) -> int: ...

@dataclass(frozen=True)
class NumericStateSpaceModel:
    A: np.ndarray
    B: np.ndarray
    C: np.ndarray
    D: np.ndarray

    def __post_init__(self) -> None:
        if self.A.shape[0] != self.A.shape[1]:
            raise ValueError('Matrix A must be square')
        if self.B.shape[0] != self.A.shape[0]:
            raise ValueError('Number of columns of matrix B must be equal to number of rows of matrix A')
        if self.C.shape[1] != self.A.shape[0]:
            raise ValueError('Number of columns of matrix B must be equal to number of rows of matrix A')
        if self.D.shape[0] != self.C.shape[0]:
            raise ValueError('Number of rows of matrix D must be equal to number of rows of matrix C')
        if self.D.shape[1] != self.B.shape[1]:
            raise ValueError('Number of columns of matrix D must be equal to number of columns of matrix B')

    @property
    def n_states(self) -> int:
        return self.A.shape[0]

    @property
    def n_inputs(self) -> int:
        return self.B.shape[1]

    @property
    def n_outputs(self) -> int:
        return self.C.shape[0]

@dataclass(frozen=True)
class SymbolicStateSpaceModel:
    A: sp.Matrix
    B: sp.Matrix
    C: sp.Matrix
    D: sp.Matrix

    def __post_init__(self) -> None:
        if self.A.shape[0] != self.A.shape[1]:
            raise ValueError('Matrix A must be square')
        if self.B.shape[0] != self.A.shape[0]:
            raise ValueError('Number of columns of matrix B must be equal to number of rows of matrix A')
        if self.C.shape[1] != self.A.shape[0]:
            raise ValueError('Number of columns of matrix B must be equal to number of rows of matrix A')
        if self.D.shape[0] != self.C.shape[0]:
            raise ValueError('Number of rows of matrix D must be equal to number of rows of matrix C')
        if self.D.shape[1] != self.B.shape[1]:
            raise ValueError('Number of columns of matrix D must be equal to number of columns of matrix B')

    @property
    def n_states(self) -> int:
        return self.A.shape[0]

    @property
    def n_inputs(self) -> int:
        return self.B.shape[1]

    @property
    def n_outputs(self) -> int:
        return self.C.shape[0]

def continuous_state_space_solver(ssm: NumericStateSpaceModel, y: np.ndarray, t: np.ndarray, x0: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sys = scipy.signal.StateSpace(ssm.A, ssm.B, ssm.C, ssm.D)
    return scipy.signal.lsim(sys, y, t, x0)

def symbolic_state_space_solver(ssm: SymbolicStateSpaceModel, y: sp.Matrix, t: sp.Matrix, x0: sp.Matrix) -> sp.Symbol:
    ...