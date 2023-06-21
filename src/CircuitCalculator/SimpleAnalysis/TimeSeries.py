from .layout import TimeSeriesPlot, new_time_series_plot, figure_wide, PlotFcn
from ..Circuit.solution import TimeDomainSolution

from dataclasses import dataclass
import numpy as np
import functools

@dataclass
class VoltageTimeSeriesPlot:
    time_series_plot: TimeSeriesPlot
    solution: TimeDomainSolution
    tmax: float
    tmin: float = 0
    N_samples: int = 200

    def add_voltage(self, id: str, **kwargs):
        t = np.linspace(self.tmin, self.tmax, self.N_samples)
        x = self.solution.get_voltage(id)
        self.time_series_plot.add_signal(t, x(t), f'V({id})', **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.time_series_plot.draw()

@dataclass
class CurrentTimeSeriesPlot:
    time_series_plot: TimeSeriesPlot
    solution: TimeDomainSolution
    tmax: float
    tmin: float = 0
    N_samples: int = 200

    def add_current(self, id: str, **kwargs):
        t = np.linspace(self.tmin, self.tmax, self.N_samples)
        x = self.solution.get_current(id)
        self.time_series_plot.add_signal(t, x(t), f'I({id})', **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.time_series_plot.draw()

def plot_ts_fcn(ax, x_fcn, tmin, tmax, N_samples, **kwargs) -> None:
    t = np.linspace(tmin, tmax, N_samples)
    ax.plot(t, x_fcn(t), **kwargs)

def plot_voltage_timeseries(id: str, tmax: float, tmin: float = 0, N_samples: int = 500, **kwargs):
    @new_time_series_plot(tmin=tmin, tmax=tmax, ylabel='u(t)→')
    def plot_timeseries(fig, ax, solution=None):
        kwargs.update({'label':f'V({id})'})
        plot_ts_fcn(ax, solution.get_voltage(id), tmin, tmax, N_samples, **kwargs)
        return fig, ax
    return plot_timeseries

def plot_current_timeseries(id: str, tmax: float, tmin: float = 0, N_samples: int = 500, **kwargs):
    @new_time_series_plot(tmin=tmin, tmax=tmax, ylabel='i(t)→')
    def plot_timeseries(fig, ax, solution=None):
        kwargs.update({'label':f'I({id})'})
        plot_ts_fcn(ax, solution.get_current(id), tmin, tmax, N_samples, **kwargs)
        return fig, ax
    return plot_timeseries

def steady_state_timedomain_analysis(circuit, w, fig_fcn, *args):
    solution = TimeDomainSolution(circuit=circuit, w=w)
    new_args = tuple(functools.partial(a, solution=solution) for a in args)
    return fig_fcn(*new_args)
