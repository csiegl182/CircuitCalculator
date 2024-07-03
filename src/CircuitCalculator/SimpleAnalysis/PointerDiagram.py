from . import layout
from .plot_elements import complex_pointer
import functools
from typing import Callable, Dict, TypedDict
from ..Circuit.solution import ComplexSolution

def plot_pointer_by_id(id:str, origin:str='', scaling:float=1, reverse:bool=False, **kwargs) -> layout.PlotFcn:
    def plot_pointer(fig:layout.Figure, ax:layout.Axes, *, pointer_fcn:Callable[[str], complex]=lambda _: 0+0j, label_fcn:Callable[[str], str]=lambda _: '') -> layout.FigureAxes:
        z0 = 0 if origin == '' else complex(pointer_fcn(origin))
        z1 = complex(pointer_fcn(id))
        z1 *= scaling
        if reverse:
            z1 = -z1
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

class PlotPointerDiagramProperties(TypedDict):
    pointer_fcn: Callable[[str], complex]
    label_fcn: Callable[[str], str]
    xlabel:str
    ylabel:str

def plot_pointers_factory(
        *args,
        type:str='default',
        solution:ComplexSolution,
        pd_lim:tuple[float, float, float, float]=(-1, 1, -1, 1),
        xlabel:str='',
        ylabel:str='') -> layout.PlotFcn:
    
    pointer_diagram_configurations: Dict[str, PlotPointerDiagramProperties] = {
        'default' : {'pointer_fcn' : lambda _: 0j, 'label_fcn' : lambda _: '', 'xlabel' : 'Re→', 'ylabel' : 'Im→'},
        'voltage' : {'pointer_fcn' : solution.get_voltage, 'label_fcn' : lambda id: f'V({id})', 'xlabel' : 'Re{V}→', 'ylabel' : 'Im{V}→'},
        'current' : {'pointer_fcn' : solution.get_current, 'label_fcn' : lambda id: f'I({id})', 'xlabel' : 'Re{I}→', 'ylabel' : 'Im{I}→'},
        'power' : {'pointer_fcn' : solution.get_power, 'label_fcn' : lambda id: f'S({id})', 'xlabel' : 'P→', 'ylabel' : 'Q→'}
    }
    pd_properties = pointer_diagram_configurations.get(type, pointer_diagram_configurations['default'])
    xlabel = xlabel if len(xlabel) > 0 else pd_properties['xlabel']
    ylabel = ylabel if len(ylabel) > 0 else pd_properties['ylabel']

    @layout.legend()
    @layout.grid()
    @layout.nyquist_like_plot(ax_lim=pd_lim, xlabel=xlabel, ylabel=ylabel)
    def plot_pointers(fig:layout.Figure, ax:layout.Axes) -> layout.FigureAxes:
        new_args = tuple(functools.partial(a, pointer_fcn=pd_properties['pointer_fcn'], label_fcn=pd_properties['label_fcn']) for a in args)
        layout.apply_plt_fcn(fig, ax, *new_args)
        return fig, ax
    return plot_pointers

def pointer_diagram(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
    plot_pointers = plot_pointers_factory(*args, type='default', **kwargs)
    return plot_pointers(*layout_fcn())

def voltage_pointer_diagram_analysis(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
    plot_pointers = plot_pointers_factory(*args, type='voltage', **kwargs)
    return plot_pointers(*layout_fcn())

def current_pointer_diagram_analysis(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
    plot_pointers = plot_pointers_factory(*args, type='current', **kwargs)
    return plot_pointers(*layout_fcn())

def power_pointer_diagram_analysis(*args, layout_fcn:layout.Layout=layout.figure_default, **kwargs) -> layout.FigureAxes:
    plot_pointers = plot_pointers_factory(*args, type='power', **kwargs)
    return plot_pointers(*layout_fcn())