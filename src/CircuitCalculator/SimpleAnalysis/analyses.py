from .PointerDiagram import VoltagePointerDiagram, CurrentPointerDiagram, PQDiagram
from .layout import PointerDiagram
from ..Circuit.circuit import Circuit
from ..Circuit.solution import TimeDomainSolution, ComplexSolution

def voltage_pointer_diagram(circuit: Circuit, w: float, resistance: float = 1, arrow_base: float = 0.05, arrow_length: float = 0.05) -> VoltagePointerDiagram:
    return VoltagePointerDiagram(
        pointer_diagram=PointerDiagram(xlabel='Re{U}→', ylabel='Im{U}→', arrow_base=arrow_base, arrow_length=arrow_length),
        solution=ComplexSolution(circuit, w=w),
        resistance=resistance
    )

def current_pointer_diagram(circuit: Circuit, w: float, conductance: float = 1, arrow_base: float = 0.05, arrow_length: float = 0.05) -> CurrentPointerDiagram:
    return CurrentPointerDiagram(
        pointer_diagram=PointerDiagram(xlabel='Re{I}→', ylabel='Im{I}→', arrow_base=arrow_base, arrow_length=arrow_length),
        solution=ComplexSolution(circuit, w=w),
        conductance=conductance
    )

def pq_diagram(circuit: Circuit, w: float, arrow_base: float = 0.05, arrow_length: float = 0.05) -> PQDiagram:
    return PQDiagram(
        pointer_diagram=PointerDiagram(xlabel='P→', ylabel='Q→', arrow_base=arrow_base, arrow_length=arrow_length),
        solution=ComplexSolution(circuit, w=w)
    )