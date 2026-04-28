from __future__ import annotations

from ..Circuit.solution import ComplexSolution, NetworkSolver, complex_solution
from ..Network.NodalAnalysis.solution import numeric_nodal_analysis_bias_point_solution
from .circuit import ThreePhaseCircuit, transform_three_phase_circuit


def three_phase_complex_solution(
    circuit: ThreePhaseCircuit,
    w: float = 0,
    peak_values: bool = False,
    solver: NetworkSolver = numeric_nodal_analysis_bias_point_solution,
) -> ComplexSolution:
    return complex_solution(transform_three_phase_circuit(circuit), w=w, peak_values=peak_values, solver=solver)
