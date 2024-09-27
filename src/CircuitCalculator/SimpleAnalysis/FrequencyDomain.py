from . import layout
from ..Circuit.solution import FrequencyDomainSolution, FrequencyDomainSeries
from typing import Callable, TypedDict
import numpy as np
import functools

def plot_discrete_frequencies_fcn(ax:layout.Axis, w:np.ndarray, X:np.ndarray, **kwargs) -> None:
    line = ax.plot([w[0], w[0]], [0, X[0]], **kwargs)
    color = line[0].get_color()
    kwargs.update({'label': '', 'color': color})
    for w0, X0 in zip(w[1:], X[1:]):
        ax.plot([w0, w0], [0, X0], **kwargs)

def plot_frequencies_by_id(
        id:str,
        **kwargs) -> layout.PlotFcn:
    def plot_frequencies(
            fig:layout.Figure,
            ax:layout.Axes,
            fd_fcn:Callable[[str], FrequencyDomainSeries]=lambda _: (np.array(0), np.array(0)),
            label_fcn:Callable[[str], str]=lambda _: '',
            **_) -> layout.FigureAxes:
        if 'label' not in kwargs.keys():
            kwargs.update({'label':label_fcn(id)})
        w, X = fd_fcn(id)
        plot_discrete_frequencies_fcn(ax[-2], w, np.abs(X), **kwargs)
        plot_discrete_frequencies_fcn(ax[-1], w, np.angle(X), **kwargs)
        return fig, ax
    return plot_frequencies

def plot_frequencies_by_fcn(
        fd_fcn:FrequencyDomainSeries,
        **kwargs) -> layout.PlotFcn:
    def plot_frequencies(fig:layout.Figure, ax:layout.Axes, **_) -> layout.FigureAxes:
        plot_discrete_frequencies_fcn(ax[-2], fd_fcn[0], np.abs(fd_fcn[1]), **kwargs)
        plot_discrete_frequencies_fcn(ax[-1], fd_fcn[0], np.angle(fd_fcn[1]), **kwargs)
        return fig, ax
    return plot_frequencies

class FrequencyDomainPlotProperties(TypedDict):
    fd_fcn: Callable[[str], FrequencyDomainSeries]
    label_fcn: Callable[[str], str]
    ylabel:str

def plot_frequencydomain_factory(
        *args,
        type:str='default',
        solution:FrequencyDomainSolution,
        wmin:float=0,
        wmax:float=-1,
        abs_min:float=0,
        abs_max:float=-1,
        phi_min:float=-np.pi,
        phi_max:float=+np.pi,
        logw:bool=False,
        logy:bool=False,
        xlabel:str='ω→',
        ylabel:str='') -> layout.PlotFcn:

    fd_plot_config: dict[str, FrequencyDomainPlotProperties] = {
        'default' : {'fd_fcn' : lambda _: (np.zeros(1), np.zeros(1)), 'label_fcn' : lambda _: '', 'ylabel' : ''},
        'voltage' : {'fd_fcn' : solution.get_voltage, 'label_fcn' : lambda id: f'V({id})', 'ylabel' : 'V'},
        'current' : {'fd_fcn' : solution.get_current, 'label_fcn' : lambda id: f'I({id})', 'ylabel' : 'I'},
        'power' : {'fd_fcn' : solution.get_power, 'label_fcn' : lambda id: f'S({id})', 'ylabel' : 'S'}
    }
    fd_properties = fd_plot_config.get(type, fd_plot_config['default'])
    ylabel = ylabel if len(ylabel) > 0 else fd_properties['ylabel']

    @layout.legend(yoffset=1.2)
    @layout.grid()
    @layout.bode_like_plot(wmin=wmin, wmax=wmax, logw=logw, logy=logy, xlabel=xlabel, ylabel=ylabel)
    def plot_frequencydomain(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        ax[-2].set_ylim(bottom=abs_min)
        if abs_max > 0:
            ax[-2].set_ylim(top=abs_max)
        ax[-1].set_ylim(bottom=phi_min, top=phi_max)
        new_args = [functools.partial(a, fd_fcn=fd_properties['fd_fcn'], label_fcn=fd_properties['label_fcn']) for a in args]
        layout.apply_plt_fcn(fig, ax, *new_args)
        return fig, ax
    return plot_frequencydomain

def frequency_domain_plot(*args, layout_fcn:layout.Layout=layout.figure_two_rows, **kwargs) -> layout.FigureAxes:
    plot_frequencydomain = plot_frequencydomain_factory(*args, type='default', **kwargs)
    return plot_frequencydomain(*layout_fcn())

def discrete_frequencies_voltage_analysis(*args, layout_fcn:layout.Layout=layout.figure_two_rows, **kwargs) -> layout.FigureAxes:
    plot_frequencydomain = plot_frequencydomain_factory(*args, type='voltage', **kwargs)
    return plot_frequencydomain(*layout_fcn())

def discrete_frequencies_current_analysis(*args, layout_fcn:layout.Layout=layout.figure_two_rows, **kwargs) -> layout.FigureAxes:
    plot_frequencydomain = plot_frequencydomain_factory(*args, type='current', **kwargs)
    return plot_frequencydomain(*layout_fcn())

def discrete_frequencies_power_analysis(*args, layout_fcn:layout.Layout=layout.figure_two_rows, **kwargs) -> layout.FigureAxes:
    plot_frequencydomain = plot_frequencydomain_factory(*args, type='power', **kwargs)
    return plot_frequencydomain(*layout_fcn())