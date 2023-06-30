from . import layout
from ..Circuit.solution import FrequencyDomainSolution, FrequencyDomainFunction
import functools
from typing import Callable
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

def nyquist_plot(
        *args,
        ax_lim:tuple[float, float, float, float],
        layout_fcn:layout.Layout=layout.figure_default,
        xlabel:str='',
        ylabel:str='') -> layout.FigureAxes:
    @layout.nyquist_plot(ax_lim=ax_lim, xlabel=xlabel, ylabel=ylabel)
    def plot_frequencydomain(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        layout.apply_plt_fcn(fig, ax, *args)
        return fig, ax
    return plot_frequencydomain(*layout_fcn())

def nyquist_voltage_analysis(
        *args,
        solution:FrequencyDomainSolution,
        ax_lim:tuple[float, float, float, float],
        layout_fcn:layout.Layout=layout.figure_default) -> layout.FigureAxes:
    @layout.nyquist_plot(ax_lim=ax_lim, xlabel='Re{V}→', ylabel='Im{V}→')
    def plot_nyquist(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        new_args = [functools.partial(a, fd_fcn=solution.get_voltage, label_fcn=lambda id: f'V({id})') for a in args]
        layout.apply_plt_fcn(fig, ax, *new_args)
        return fig, ax
    return plot_nyquist(*layout_fcn())

def nyquist_current_analysis(
        *args,
        solution:FrequencyDomainSolution,
        ax_lim:tuple[float, float, float, float],
        layout_fcn:layout.Layout=layout.figure_default) -> layout.FigureAxes:
    @layout.nyquist_plot(ax_lim=ax_lim, xlabel='Re{I}→', ylabel='Im{I}→')
    def plot_nyquist(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        new_args = [functools.partial(a, fd_fcn=solution.get_voltage, label_fcn=lambda id: f'I({id})') for a in args]
        layout.apply_plt_fcn(fig, ax, *new_args)
        return fig, ax
    return plot_nyquist(*layout_fcn())

def nyquist_power_analysis(
        *args,
        solution:FrequencyDomainSolution,
        ax_lim:tuple[float, float, float, float],
        layout_fcn:layout.Layout=layout.figure_default) -> layout.FigureAxes:
    @layout.nyquist_plot(ax_lim=ax_lim, xlabel='P→', ylabel='Q→')
    def plot_nyquist(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        new_args = [functools.partial(a, fd_fcn=solution.get_voltage, label_fcn=lambda id: f'S({id})') for a in args]
        layout.apply_plt_fcn(fig, ax, *new_args)
        return fig, ax
    return plot_nyquist(*layout_fcn())