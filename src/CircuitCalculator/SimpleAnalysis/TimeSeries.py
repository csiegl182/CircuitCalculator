from . import layout
from ..Circuit.solution import TimeDomainSolution, TimeDomainFunction
import numpy as np
import functools
from typing import Callable

def plot_timeseries_fcn(ax, x_fcn, tmin, tmax, N_samples, **kwargs) -> None:
    t = np.linspace(tmin, tmax, N_samples)
    ax.plot(t, x_fcn(t), **kwargs)

def plot_timeseries_by_id(
          id:str,
          t_min:float=0,
          t_max:float=0,
          N_samples:int=500,
          **kwargs) -> layout.PlotFcn:
    def plot_timeseries(
              fig:layout.Figure,
              ax:layout.Axes,
              ts_fcn:Callable[[str], TimeDomainFunction]=lambda _: lambda t: np.zeros(np.size(t)),
              label_fcn:Callable[[str], str]=lambda _: '',
              **_) -> layout.FigureAxes:
        x_min, x_max = t_min, t_max
        if t_min >= t_max:
            x_min, x_max = ax[0].get_xlim()
        if 'label' not in kwargs.keys():
            kwargs.update({'label':label_fcn(id)})
        plot_timeseries_fcn(ax[0], ts_fcn(id), x_min, x_max, N_samples, **kwargs)
        return fig, ax
    return plot_timeseries

def plot_timeseries_by_fcn(
          ts_fcn:TimeDomainFunction,
          t_min:float=0,
          t_max:float=0,
          N_samples:int=500,
          **kwargs) -> layout.PlotFcn:
    def plot_timeseries(fig:layout.Figure, ax:layout.Axes, **_) -> layout.FigureAxes:
        x_min, x_max = t_min, t_max
        if t_min >= t_max:
            x_min, x_max = ax[0].get_xlim()
        plot_timeseries_fcn(ax[0], ts_fcn, x_min, x_max, N_samples, **kwargs)
        return fig, ax
    return plot_timeseries

def time_domain_plot(
        *args,
        tmax:float,
        tmin:float=0,
        layout_fcn:layout.Layout=layout.figure_default,
        xlabel:str='t→',
        ylabel:str='') -> layout.FigureAxes:
        @layout.timeseries_plot(tmin=tmin, tmax=tmax, xlabel=xlabel, ylabel=ylabel)
        def plot_timeseries(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
             layout.apply_plt_fcn(fig, ax, *args)
             return fig, ax
        return plot_timeseries(*layout_fcn())

def steady_state_voltage_timedomain_analysis(
        *args,
        solution:TimeDomainSolution,
        tmax:float,
        tmin:float=0,
        layout_fcn:layout.Layout=layout.figure_default) -> layout.FigureAxes:
        @layout.timeseries_plot(tmin=tmin, tmax=tmax, ylabel='v(t)→')
        def plot_timeseries(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
             new_args = [functools.partial(a, ts_fcn=solution.get_voltage, label_fcn=lambda id: f'V({id})') for a in args]
             layout.apply_plt_fcn(fig, ax, *new_args)
             return fig, ax
        return plot_timeseries(*layout_fcn())

def steady_state_current_timedomain_analysis(
        *args,
        solution:TimeDomainSolution,
        tmax:float,
        tmin:float=0,
        layout_fcn:layout.Layout=layout.figure_default) -> layout.FigureAxes:
        @layout.timeseries_plot(tmin=tmin, tmax=tmax, ylabel='i(t)→')
        def plot_timeseries(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
             new_args = [functools.partial(a, ts_fcn=solution.get_current, label_fcn=lambda id: f'I({id})') for a in args]
             layout.apply_plt_fcn(fig, ax, *new_args)
             return fig, ax
        return plot_timeseries(*layout_fcn())

def steady_state_instantaneous_power_analysis(
        *args,
        solution:TimeDomainSolution,
        tmax:float,
        tmin:float=0,
        layout_fcn:layout.Layout=layout.figure_default) -> layout.FigureAxes:
        @layout.timeseries_plot(tmin=tmin, tmax=tmax, ylabel='p(t)→')
        def plot_timeseries(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
             new_args = [functools.partial(a, ts_fcn=solution.get_power, label_fcn=lambda id: f'P({id})') for a in args]
             layout.apply_plt_fcn(fig, ax, *new_args)
             return fig, ax
        return plot_timeseries(*layout_fcn())
