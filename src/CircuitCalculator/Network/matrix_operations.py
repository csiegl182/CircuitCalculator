import numpy as np
import sympy as sp
from sympy.matrices.common import NonInvertibleMatrixError
from typing import Protocol, Any

Matrix = np.ndarray | sp.Matrix
symbolic = sp.core.symbol.Symbol

class MatrixInversionException(Exception):
    """Exception raised when matrix inversion fails."""
    pass

class MatrixElement(Protocol):
    def __init__(self, value: complex | symbolic) -> None: ...
    @property
    def value(self) -> Any: ...

    @property
    def isfinite(self) -> bool: ...

class NumericMatrixElement:
    def __init__(self, value: complex | symbolic) -> None:
        try:
            self._value = complex(value)
        except ValueError:
            self._value = np.nan

    @property
    def value(self) -> complex:
        return self._value

    @property
    def isfinite(self) -> bool:
        if np.isnan(self.value):
            return True
        return np.isfinite(self.value)

class SymbolicMatrixElement:
    def __init__(self, value: complex | symbolic) -> None:
        self._value = sp.sympify(value)

    @property
    def value(self) -> Any:
        return self._value

    @property
    def isfinite(self) -> bool:
        if self.value == sp.nan:
            return True
        if self.value.is_finite is None:
            return True
        return self.value.is_finite

class MatrixOperations(Protocol):
    @staticmethod
    def zeros(shape: tuple[int, int]) -> Any: ...

    @staticmethod
    def nan(shape: tuple[int, int]) -> Any: ...

    @staticmethod
    def column_vector(values: list[complex | symbolic]) -> Any: ...

    @staticmethod
    def vstack(matrices: tuple[Any, ...]) -> Any: ...

    @staticmethod
    def hstack(matrices: tuple[Any, ...]) -> Any: ...
    
    @staticmethod
    def diag(values: list[complex | float | symbolic]) -> Any: ...

    @staticmethod
    def diag_vec(values: Any) -> list[complex | symbolic]: ...

    @staticmethod
    def inv(matrix: Any) -> Any: ...

    @staticmethod
    def solve(A: Any, b: Any) -> tuple[complex | symbolic, ...]: ...

    @staticmethod
    def elm(value: complex | symbolic) -> MatrixElement: ...

    @staticmethod
    def shape(matrix: Any) -> tuple[int, int]: ...

    @staticmethod
    def contains_nan(matrix: Any) -> bool: ...

    @staticmethod
    def any_element(matrix: Any, axis: int) -> np.ndarray: ...

    @staticmethod
    def delete(matrix: Any, idx: list[int], axis: int) -> Any: ...

class NumPyMatrixOperations:
    @staticmethod
    def zeros(shape: tuple[int, int]) -> np.ndarray:
        return np.zeros(shape, dtype=complex)

    @staticmethod
    def nan(shape: tuple[int, int]) -> np.ndarray:
        return np.full(shape, np.nan, dtype=complex)

    @staticmethod
    def column_vector(values: list[complex | symbolic]) -> Any:
        return np.array([NumericMatrixElement(v).value for v in values]).reshape(len(values), 1)

    @staticmethod
    def vstack(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
        return np.vstack(matrices)

    @staticmethod
    def hstack(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
        return np.hstack(matrices)

    @staticmethod
    def diag(values: list[complex | symbolic]) -> np.ndarray:
        return np.diag([NumericMatrixElement(v).value for v in values])

    @staticmethod
    def diag_vec(values: np.ndarray) -> list[complex | symbolic]:
        return [NumericMatrixElement(v).value for v in np.diag(values)]

    @staticmethod
    def inv(matrix: np.ndarray) -> np.ndarray:
        try:
            return np.linalg.inv(matrix)
        except np.linalg.LinAlgError:
            raise MatrixInversionException("Matrix inversion failed, possibly due to singular matrix.")

    @staticmethod
    def solve(A: np.ndarray, b: np.ndarray) -> tuple[complex, ...]:
        try:
            return tuple(np.linalg.solve(A, b).flatten())
        except np.linalg.LinAlgError:
            raise MatrixInversionException("Matrix inversion failed, possibly due to singular matrix.")

    @staticmethod
    def elm(value: complex | symbolic) -> NumericMatrixElement:
        return NumericMatrixElement(value)

    @staticmethod
    def shape(matrix: np.ndarray) -> tuple[int, int]:
        return (matrix.shape[0], matrix.shape[1])

    @staticmethod
    def contains_nan(matrix: np.ndarray) -> bool:
        return np.any(np.isnan(matrix)) == True

    @staticmethod
    def any_element(matrix: np.ndarray, axis: int) -> np.ndarray:
        return np.any(matrix, axis=axis)

    @staticmethod
    def delete(matrix: np.ndarray, idx: list[int], axis: int) -> np.ndarray:
        return np.delete(matrix, idx, axis)

class SymPyMatrixOperations:
    @staticmethod
    def zeros(shape: tuple[int, int]) -> sp.Matrix:
        return sp.zeros(*shape)

    @staticmethod
    def nan(shape: tuple[int, int]) -> sp.Matrix:
        return sp.Matrix([[sp.nan] * shape[1]] * shape[0])

    @staticmethod
    def column_vector(values: list[complex | symbolic]) -> sp.Matrix:
        return sp.Matrix([[v] for v in values]).reshape(len(values), 1)

    @staticmethod
    def vstack(matrices: tuple[sp.Matrix, ...]) -> sp.Matrix:
        return sp.Matrix.vstack(*matrices)

    @staticmethod
    def hstack(matrices: tuple[sp.Matrix, ...]) -> sp.Matrix:
        return sp.Matrix.hstack(*[sp.Matrix(m) for m in matrices])

    @staticmethod
    def diag(values: list[complex | symbolic]) -> sp.Matrix:
        return sp.diag(*values)

    @staticmethod
    def diag_vec(values: sp.Matrix) -> list[complex | symbolic]:
        return list(values.diagonal())

    @staticmethod
    def inv(matrix: sp.Matrix) -> sp.Matrix:
        try:
            return sp.Matrix(matrix.inv())
        except ValueError:
            raise MatrixInversionException("Matrix inversion failed, possibly due to singular matrix.")

    @staticmethod
    def solve(A: sp.Matrix, b: sp.Matrix) -> tuple[symbolic, ...]:
        try:
            return tuple(A.LUsolve(b))
        except NonInvertibleMatrixError:
            raise MatrixInversionException("Matrix inversion failed, possibly due to singular matrix.")

    @staticmethod
    def elm(value: complex | symbolic) -> SymbolicMatrixElement:
        return SymbolicMatrixElement(value)

    @staticmethod
    def shape(matrix: sp.Matrix) -> tuple[int, int]:
        return (matrix.shape[0], matrix.shape[1])

    @staticmethod
    def contains_nan(matrix: sp.Matrix) -> bool:
        return False

    @staticmethod
    def any_element(matrix: sp.Matrix, axis: int) -> np.ndarray:
        is_zero = np.array(matrix.applyfunc(lambda x: int(x != 0)), dtype=int)
        return np.any(is_zero, axis)

    @staticmethod
    def delete(matrix: sp.Matrix, idx: list[int], axis: int) -> sp.Matrix:
        if len(idx) == 0:
            return matrix
        if axis == 0:
            return matrix.row_del(*idx)
        if axis == 1:
            return matrix.col_del(*idx)
        return matrix