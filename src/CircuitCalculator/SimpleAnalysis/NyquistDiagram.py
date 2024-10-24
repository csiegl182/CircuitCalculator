from . import layout
from ..Circuit.solution import FrequencyDomainSolution, FrequencyDomainSeries
import functools
from typing import Callable, Dict, TypedDict
import numpy as np

def plot_nyquist_by_id(id:str, **kwargs) -> layout.PlotFcn:
    def plot_pointer(fig:layout.Figure, ax:layout.Axes, *, fd_fcn:Callable[[str], tuple[list[float], list[complex]]]=lambda _: ([0], [0+0j]), label_fcn:Callable[[str], str]=lambda _: '') -> layout.FigureAxes:
        w, z = fd_fcn(id)
        if 'label' not in kwargs.keys():
            kwargs.update({'label':label_fcn(id)})
        if 'marker' not in kwargs.keys():
            kwargs.update({'marker':'o'})
        kwargs.update({'linestyle': ''})

        ax[0].plot(np.real(z), np.imag(z), **kwargs)
        return fig, ax
    return plot_pointer

def plot_nyquist_by_value(z:list[complex], **kwargs) -> layout.PlotFcn:
    def plot_pointer(fig:layout.Figure, ax:layout.Axes, **_) -> layout.FigureAxes:
        ax[0].plot(np.real(z), np.imag(z), **kwargs)
        return fig, ax
    return plot_pointer

class NyquistDiagramProperties(TypedDict):
    fd_fcn: Callable[[str], FrequencyDomainSeries]
    label_fcn: Callable[[str], str]
    xlabel:str
    ylabel:str

def plot_nyquist_diagram_factory(
        *args,
        type:str='default',
        solution:FrequencyDomainSolution,
        ax_lim:tuple[float, float, float, float]=(-1, 1, -1, 1),
        xlabel:str='',
        ylabel:str='') -> layout.PlotFcn:

    nyquist_diagram_configuration: Dict[str, NyquistDiagramProperties] = {
        'default' : {'fd_fcn' : lambda _: (np.zeros(1), np.zeros(1)), 'label_fcn' : lambda _: '', 'xlabel' : 'Re→', 'ylabel' : 'Im→'},
        'voltage' : {'fd_fcn' : solution.get_voltage, 'label_fcn' : lambda id: f'V({id})', 'xlabel' : 'Re{V}→', 'ylabel' : 'Im{V}→'},
        'current' : {'fd_fcn' : solution.get_current, 'label_fcn' : lambda id: f'I({id})', 'xlabel' : 'Re{I}→', 'ylabel' : 'Im{I}→'},
        'power' : {'fd_fcn' : solution.get_power, 'label_fcn' : lambda id: f'S({id})', 'xlabel' : 'P→', 'ylabel' : 'Q→'}
    }
    nd_properties = nyquist_diagram_configuration.get(type, nyquist_diagram_configuration['default'])
    xlabel = xlabel if len(xlabel) > 0 else nd_properties['xlabel']
    ylabel = ylabel if len(ylabel) > 0 else nd_properties['ylabel']

    @layout.legend()
    @layout.grid()
    @layout.nyquist_like_plot(ax_lim=ax_lim, xlabel=xlabel, ylabel=ylabel)
    def plot_nyquist_diagram(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        new_args = [functools.partial(a, fd_fcn=nd_properties['fd_fcn'], label_fcn=nd_properties['label_fcn']) for a in args]
        layout.apply_plt_fcn(fig, ax, *new_args)
        return fig, ax
    return plot_nyquist_diagram

def nyquist_plot(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
    plot_nyquist_diagram = plot_nyquist_diagram_factory(*args, type='default', **kwargs)
    return plot_nyquist_diagram(*layout_fcn())

def nyquist_voltage_analysis(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
    plot_nyquist_diagram = plot_nyquist_diagram_factory(*args, type='voltage', **kwargs)
    return plot_nyquist_diagram(*layout_fcn())

def nyquist_current_analysis(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
    plot_nyquist_diagram = plot_nyquist_diagram_factory(*args, type='current', **kwargs)
    return plot_nyquist_diagram(*layout_fcn())

def nyquist_power_analysis(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
    plot_nyquist_diagram = plot_nyquist_diagram_factory(*args, type='power', **kwargs)
    return plot_nyquist_diagram(*layout_fcn())
