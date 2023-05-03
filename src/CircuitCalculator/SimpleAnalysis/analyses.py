from .TimeSeries import VoltageTimeSeriesPlot, CurrentTimeSeriesPlot
from .PointerDiagram import VoltagePointerDiagram, CurrentPointerDiagram
from .Layout import TimeSeriesPlot, PointerDiagram
from ..Circuit.circuit import Circuit
from ..Circuit.solution import TimeDomainSolution, ComplexSolution

def voltage_timeseries_plot(circuit: Circuit, tmax: float, tmin: float = 0, N_samples: int = 200) -> VoltageTimeSeriesPlot:
    return VoltageTimeSeriesPlot(
        time_series_plot=TimeSeriesPlot(tmin=tmin, tmax=tmax, y_label='u(t)→'),
        solution=TimeDomainSolution(circuit),
        tmin=tmin,
        tmax=tmax,
        N_samples=N_samples
    )

def current_timeseries_plot(circuit: Circuit, tmax: float, tmin: float = 0, N_samples: int = 200) -> CurrentTimeSeriesPlot:
    return CurrentTimeSeriesPlot(
        time_series_plot=TimeSeriesPlot(tmin=tmin, tmax=tmax, y_label='i(t)→'),
        solution=TimeDomainSolution(circuit),
        tmin=tmin,
        tmax=tmax,
        N_samples=N_samples
    )

def voltage_pointer_diagram(circuit: Circuit, w: float, resistance: float = 1, arrow_base: float = 0.05, arrow_length: float = 0.05) -> VoltagePointerDiagram:
    return VoltagePointerDiagram(
        pointer_diagram=PointerDiagram(arrow_base=arrow_base, arrow_length=arrow_length),
        solution=ComplexSolution(circuit, w=w),
        resistance=resistance
    )

def current_pointer_diagram(circuit: Circuit, w: float, conductance: float = 1, arrow_base: float = 0.05, arrow_length: float = 0.05) -> CurrentPointerDiagram:
    return CurrentPointerDiagram(
        pointer_diagram=PointerDiagram(arrow_base=arrow_base, arrow_length=arrow_length),
        solution=ComplexSolution(circuit, w=w),
        conductance=conductance
    )