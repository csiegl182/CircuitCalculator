from .layout import timeseries_plot
from ..Circuit.solution import TimeDomainSolution

import numpy as np
import functools

def plot_ts_fcn(ax, x_fcn, tmin, tmax, N_samples, **kwargs) -> None:
    t = np.linspace(tmin, tmax, N_samples)
    ax.plot(t, x_fcn(t), **kwargs)

def plot_voltage_timeseries(id: str, tmax: float, tmin: float = 0, N_samples: int = 500, **kwargs):
    @timeseries_plot(tmin=tmin, tmax=tmax, ylabel='u(t)→')
    def plot_timeseries(fig, ax, solution=None):
        kwargs.update({'label':f'V({id})'})
        plot_ts_fcn(ax, solution.get_voltage(id), tmin, tmax, N_samples, **kwargs)
        return fig, ax
    return plot_timeseries

def plot_current_timeseries(id: str, tmax: float, tmin: float = 0, N_samples: int = 500, **kwargs):
    @timeseries_plot(tmin=tmin, tmax=tmax, ylabel='i(t)→')
    def plot_timeseries(fig, ax, solution=None):
        kwargs.update({'label':f'I({id})'})
        plot_ts_fcn(ax, solution.get_current(id), tmin, tmax, N_samples, **kwargs)
        return fig, ax
    return plot_timeseries

def steady_state_timedomain_analysis(circuit, w, fig_fcn, *args):
    solution = TimeDomainSolution(circuit=circuit, w=w)
    new_args = tuple(functools.partial(a, solution=solution) for a in args)
    return fig_fcn(*new_args)
