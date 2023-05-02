from .TimeSeries import VoltageTimeSeriesPlot, CurrentTimeSeriesPlot
from .Layout import TimeSeriesPlot
from ..Circuit.circuit import Circuit
from ..Circuit.solution import TimeDomainSolution

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