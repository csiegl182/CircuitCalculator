import numpy as np

from CircuitCalculator.Circuit.Components import components as cp
from CircuitCalculator.Circuit.circuit import Circuit
from CircuitCalculator.Circuit.solution import complex_solution


def test_complex_current_source_is_active_for_complex_solution_frequency() -> None:
    circuit = Circuit(
        [
            cp.complex_current_source(id="I1", nodes=("1", "0"), I=5 + 2j, Y=0),
            cp.impedance(id="Z1", nodes=("1", "0"), Z=10 + 5j),
        ],
        ground_node="0",
    )

    solution = complex_solution(circuit, w=2 * np.pi * 50)

    assert np.isclose(solution.get_current("I1"), 5 + 2j)
    assert np.isclose(solution.get_current("Z1"), -(5 + 2j))
