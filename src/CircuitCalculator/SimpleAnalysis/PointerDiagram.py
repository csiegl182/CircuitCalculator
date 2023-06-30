from . import layout
from .plot_elements import complex_pointer
import functools
from typing import Callable
from ..Circuit.solution import ComplexSolution

def plot_pointer_by_id(id:str, origin:str='', scaling:float=1, **kwargs) -> layout.PlotFcn:
    def plot_pointer(fig:layout.Figure, ax:layout.Axes, *, pointer_fcn:Callable[[str], complex]=lambda _: 0+0j, label_fcn:Callable[[str], str]=lambda _: '') -> layout.FigureAxes:
        z0 = 0 if origin == '' else complex(pointer_fcn(origin))
        z1 = complex(pointer_fcn(id))
        z1 *= scaling
        if 'label' not in kwargs.keys():
            kwargs.update({'label':label_fcn(id)})
        complex_pointer(ax[0], z0, z0+z1, **kwargs)
        return fig, ax
    return plot_pointer

def plot_pointer_by_value(z:complex, origin:complex=0+0j, **kwargs) -> layout.PlotFcn:
    def plot_pointer(fig:layout.Figure, ax:layout.Axes, **_) -> layout.FigureAxes:
        complex_pointer(ax[0], origin, z+origin, **kwargs)
        return fig, ax
    return plot_pointer

def pointer_diagram(
        *args,
        pd_lim=(-1, 1, -1, 1),
        layout_fcn:layout.Layout=layout.figure_default,
        xlabel:str='',
        ylabel:str='') -> layout.FigureAxes:
    @layout.nyquist_plot(ax_lim=pd_lim, xlabel=xlabel, ylabel=ylabel)
    def plot_pointers(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        layout.apply_plt_fcn(fig, ax, *args)
        return fig, ax
    return plot_pointers(*layout_fcn())

def voltage_pointer_diagram_analysis(
        *args,
        solution:ComplexSolution,
        pd_lim:tuple[float, float, float, float]=(-1, 1, -1, 1),
        layout_fcn:layout.Layout=layout.figure_default) -> layout.FigureAxes:
    @layout.nyquist_plot(ax_lim=pd_lim, xlabel='Re{V}→', ylabel='Im{V}→')
    def plot_pointers(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        new_args = tuple(functools.partial(a, pointer_fcn=solution.get_voltage, label_fcn=lambda id: f'V({id})') for a in args)
        layout.apply_plt_fcn(fig, ax, *new_args)
        return fig, ax
    return plot_pointers(*layout_fcn())

def current_pointer_diagram_analysis(
        *args,
        solution:ComplexSolution,
        pd_lim:tuple[float, float, float, float]=(-1, 1, -1, 1),
        layout_fcn:layout.Layout=layout.figure_default) -> layout.FigureAxes:
    @layout.nyquist_plot(ax_lim=pd_lim, xlabel='Re{I}→', ylabel='Im{I}→')
    def plot_pointers(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        new_args = tuple(functools.partial(a, pointer_fcn=solution.get_current, label_fcn=lambda id: f'I({id})') for a in args)
        layout.apply_plt_fcn(fig, ax, *new_args)
        return fig, ax
    return plot_pointers(*layout_fcn())

def power_pointer_diagram_analysis(
        *args,
        solution:ComplexSolution,
        pd_lim:tuple[float, float, float, float]=(-1, 1, -1, 1),
        layout_fcn:layout.Layout=layout.figure_default) -> layout.FigureAxes:
    @layout.nyquist_plot(ax_lim=pd_lim, xlabel='P→', ylabel='Q→')
    def plot_pointers(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        new_args = tuple(functools.partial(a, pointer_fcn=solution.get_power, label_fcn=lambda id: f'S({id})') for a in args)
        layout.apply_plt_fcn(fig, ax, *new_args)
        return fig, ax
    return plot_pointers(*layout_fcn())

