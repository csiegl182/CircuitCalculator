from . import layout
from ..Circuit.solution import FrequencyDomainSolution, FrequencyDomainFunction
from typing import Callable
import numpy as np
import functools

def plot_discrete_frequencies_fcn(ax:layout.Axes, w:np.ndarray, X:np.ndarray, **kwargs) -> None:
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
            fd_fcn:Callable[[str], FrequencyDomainFunction]=lambda _: (np.array(0), np.array(0)),
            label_fcn:Callable[[str], str]=lambda _: '',
            **_) -> layout.FigureAxes:
        if 'label' not in kwargs.keys():
            kwargs.update({'label':label_fcn(id)})
        w, X = fd_fcn(id)
        plot_discrete_frequencies_fcn(ax, w, np.abs(X), **kwargs)
        return fig, ax
    return plot_frequencies

def frequency_domain_plot(
        *args,
        wmax:float,
        wmin:float=0,
        layout_fcn:layout.Layout=layout.figure_default,
        xlabel:str='ω→',
        ylabel:str='') -> layout.FigureAxes:
    @layout.frequencydomain_plot(wmin=wmin, wmax=wmax, xlabel=xlabel, ylabel=ylabel)
    def plot_frequencydomain(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        layout.apply_plt_fcn(fig, ax, *args)
        return fig, ax
    return plot_frequencydomain(*layout_fcn())

def discrete_frequencies_voltage_analysis(
        *args,
        solution:FrequencyDomainSolution,
        wmax:float,
        wmin:float=0,
        layout_fcn:layout.Layout=layout.figure_default) -> layout.FigureAxes:
    @layout.frequencydomain_plot(wmin=wmin, wmax=wmax, ylabel='V(ω)→')
    def plot_frequencydomain(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        new_args = [functools.partial(a, fd_fcn=solution.get_voltage, label_fcn=lambda id: f'V({id})') for a in args]
        layout.apply_plt_fcn(fig, ax, *new_args)
        return fig, ax
    return plot_frequencydomain(*layout_fcn())
