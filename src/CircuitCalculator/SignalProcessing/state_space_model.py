import numpy as np
from typing import Protocol
from dataclasses import dataclass

@dataclass(frozen=True)
class StateSpaceModel:
    A: np.ndarray
    B: np.ndarray
    C: np.ndarray
    D: np.ndarray

    def __post_init__(self) -> None:
        if self.A.shape[0] != self.A.shape[1]:
            raise ValueError('Matrix A must be square')
        # n_states = self.A.shape[0]
        # n_inputs = self.B.shape[1]
        # if self.B.shape[0] != self.A.shape[0]:
        #     raise ValueError('Number of columns of matrix B must be equal to number of rows of matrix A')
        # if self.C.shape[1] != self.A.shape[0]:
        #     raise ValueError('Number of coluns of matrix B must be equal to number of rows of matrix A')

    @property
    def n_states(self) -> int:
        return self.A.shape[0]

    @property
    def n_input(self) -> int:
        return self.B.shape[1]

    @property
    def n_output(self) -> int:
        return self.C.shape[0]
