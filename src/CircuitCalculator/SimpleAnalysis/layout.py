import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes as Axis

from typing import Callable

class LayoutError(Exception):
    ...

color = {
    'black' : (0, 0, 0),
    'grey' : (.7, .7, .7),
    'lightgrey' : (.9, .9, .9),
    'darkgrey' : (.5, .5, .5),
    'darkdarkgrey' : (.2, .2, .2),
    'darkblue' : (.13, .22, .39),
    'lightblue' : (.4, .7, 1),
    'red' : (0.721, 0, 0),
    'darkred' : (0.8, 0, 0),
    'green' : (0, 0.45, 0.333),
    'blue' : (.18, .33, .59),
    'purple' : (.44, .19, .63),
    'white' : (1, 1, 1)
}

Axes = tuple[Axis, ...]
FigureAxes = tuple[Figure, Axes]
Layout = Callable[[], FigureAxes]
PlotFcn = Callable[[Figure, Axes], FigureAxes]

def figure_default() -> FigureAxes:
    fig, ax = plt.subplots()
    return fig, (ax,)
    
def figure_two_rows() -> FigureAxes:
    fig, ax = plt.subplots(nrows=2, sharex=True)
    return fig, tuple(ax)

def apply_plt_fcn(fig, ax, *args: PlotFcn) -> FigureAxes:
    for plt_fcn in args:
        plt_fcn(fig, ax)
    return fig, ax

def legend(yoffset:float=1.1) -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            fig, ax = plot_fcn(fig, ax, *args, **kwargs)
            ax[0].legend(
                handles=[line for line in ax[0].lines if not line._label.startswith('_')],
                ncol=len(ax[0].lines),
                loc='upper center',
                bbox_to_anchor=(0.5, yoffset),
                frameon=False
            )
            return fig, ax
        return wrapper
    return decorator

def grid(visible:bool=True) -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            for a in ax:
                a.grid(visible=visible, zorder=-1)
            return plot_fcn(fig, ax, *args, **kwargs)
        return wrapper
    return decorator

def equal_scaling() -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            for a in ax:
                a.set_aspect('equal', 'box')
            return plot_fcn(fig, ax, *args, **kwargs)
        return wrapper
    return decorator

def xlim_bottom(xmin:float=0, xmax:float=-1) -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            if xmax >= xmin:
                ax[-1].set_xlim(left=xmin, right=xmax)
            return plot_fcn(fig, ax, *args, **kwargs)
        return wrapper
    return decorator

def xlabel_bottom(label:str='') -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            ax[-1].set_xlabel(label)
            return plot_fcn(fig, ax, *args, **kwargs)
        return wrapper
    return decorator

def nyquist_like_plot(ax_lim:tuple[float, float, float, float], xlabel:str='', ylabel:str='') -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        @equal_scaling()
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            ax[0].set_xlabel(xlabel)
            ax[0].set_ylabel(ylabel)
            ax[0].set_xlim(left=ax_lim[0], right=ax_lim[1])
            ax[0].set_ylim(bottom=ax_lim[2], top=ax_lim[3])
            return plot_fcn(fig, ax, *args, **kwargs)
        return wrapper
    return decorator

def frequencydomain_plot(ylabel:str='') -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            ax[0].set_ylabel(ylabel)
            ax[1].set_ylabel(ylabel)
            return plot_fcn(fig, ax, *args, **kwargs)
        return wrapper
    return decorator

def bode_like_plot(wmin:float=0, wmax:float=-1, logw:bool=False, logy:bool=False, xlabel:str='ω→', ylabel:str='') -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        @xlabel_bottom(xlabel)
        @xlim_bottom(xmin=wmin, xmax=wmax)
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            if len(ylabel) > 0:
                ax[-2].set_ylabel(f'|{ylabel}|→')
                ax[-1].set_ylabel(f'arg{{{ylabel}}}→')
            ax[-2].set_yscale('log' if logy else 'linear')
            ax[-1].set_xscale('log' if logw else 'linear')
            return plot_fcn(fig, ax, *args, **kwargs)
        return wrapper
    return decorator