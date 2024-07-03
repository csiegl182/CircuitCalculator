from . import layout
from ..Circuit.solution import TimeDomainSolution, TimeDomainFunction
import numpy as np
import functools
from typing import Callable, TypedDict, Dict

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

class PlotTimeSeriesProperties(TypedDict):
     ts_fcn: Callable[[str], TimeDomainFunction]
     label_fcn: Callable[[str], str]
     ylabel: str

def plot_timeseries_factory(
        *args,
        type:str='default',
        solution:TimeDomainSolution,
        tmax:float=-1,
        tmin:float=0,
        xlabel:str='t→',
        ylabel:str='') -> layout.PlotFcn:

    time_series_configurations: Dict[str, PlotTimeSeriesProperties] = {
        'voltage' : {'ts_fcn': solution.get_voltage, 'label_fcn': lambda id: f'V({id})', 'ylabel': 'v(t)→'},
        'current' : {'ts_fcn': solution.get_current, 'label_fcn': lambda id: f'I({id})', 'ylabel': 'i(t)→'},
        'power' : {'ts_fcn': solution.get_power, 'label_fcn': lambda id: f'P({id})', 'ylabel': 'p(t)→'},
        'default' : {'ts_fcn': lambda _: lambda t: np.zeros(np.size(t)), 'label_fcn': lambda _: '', 'ylabel': ''}
    }

    ts_properties = time_series_configurations.get(type, time_series_configurations['default'])
    ylabel = ylabel if len(ylabel) > 0 else ts_properties['ylabel']

    @layout.legend()
    @layout.grid()
    @layout.xlim_bottom(xmin=tmin, xmax=tmax)
    @layout.xlabel_bottom(xlabel)
    def plot_timeseries(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        ax[-1].set_ylabel(ylabel)
        updated_args = [functools.partial(a, ts_fcn=ts_properties['ts_fcn'], label_fcn=ts_properties['label_fcn']) for a in args]
        layout.apply_plt_fcn(fig, ax, *updated_args)
        return fig, ax
    return plot_timeseries

def time_domain_plot(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
        plot_timeseries = plot_timeseries_factory(*args, type='default', **kwargs)
        return plot_timeseries(*layout_fcn())

def steady_state_voltage_timedomain_analysis(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
        plot_timeseries = plot_timeseries_factory(*args, type='voltage', **kwargs)
        return plot_timeseries(*layout_fcn())

def steady_state_current_timedomain_analysis(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
        plot_timeseries = plot_timeseries_factory(*args, type='current', **kwargs)
        return plot_timeseries(*layout_fcn())

def steady_state_instantaneous_power_analysis(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
        plot_timeseries = plot_timeseries_factory(*args, type='power', **kwargs)
        return plot_timeseries(*layout_fcn())