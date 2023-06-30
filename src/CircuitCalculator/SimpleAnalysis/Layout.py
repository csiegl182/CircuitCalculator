import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes as Axis

from typing import Callable

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

def default_layout(**kwargs) -> FigureAxes:
    return plt.subplots(ncols=1, nrows=1, **kwargs)

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

def timeseries_plot(tmin:float=0, tmax:float=1, grid:bool=True, xlabel:str='t→', ylabel:str='') -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            ax[0].set_xlabel(xlabel)
            ax[0].set_ylabel(ylabel)
            ax[0].set_xlim(xmin=tmin, xmax=tmax)
            ax[0].grid(visible=grid, zorder=-1)
            fig, ax = plot_fcn(fig, ax, *args, **kwargs)
            ax[0].legend(
                handles=[line for line in ax[0].lines if not line._label.startswith('_')],
                ncol=len(ax[0].lines),
                loc='upper center',
                bbox_to_anchor=(0.5, 1.1),
                frameon=False
            )
            return fig, ax
        return wrapper
    return decorator

def frequencydomain_plot(wmin:float=0, wmax:float=1, grid:bool=True, xlabel:str='ω→', ylabel:str='') -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            ax[0].set_xlabel(xlabel)
            ax[0].set_ylabel(ylabel)
            ax[0].set_xlim(xmin=wmin, xmax=wmax)
            ax[0].grid(visible=grid, zorder=-1)
            fig, ax = plot_fcn(fig, ax, *args, **kwargs)
            ax[0].legend(
                handles=[line for line in ax[0].lines if not line._label.startswith('_')],
                ncol=len(ax[0].lines),
                loc='upper center',
                bbox_to_anchor=(0.5, 1.1),
                frameon=False
            )
            return fig, ax
        return wrapper
    return decorator

def nyquist_plot(ax_lim:tuple[float, float, float, float], xlabel:str='', ylabel:str='', grid:bool=True) -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            ax[0].grid(visible=grid, zorder=-1)
            ax[0].set_aspect('equal', 'box')
            ax[0].set_xlabel(xlabel)
            ax[0].set_ylabel(ylabel)
            ax[0].set_xlim(left=ax_lim[0], right=ax_lim[1])
            ax[0].set_ylim(bottom=ax_lim[2], top=ax_lim[3])
            fig, ax = plot_fcn(fig, ax, *args, **kwargs)
            ax[0].legend(
                handles=[line for line in ax[0].lines if not line._label.startswith('_')],
                ncol=len(ax[0].lines),
                loc='upper center',
                bbox_to_anchor=(0.5, 1.1),
                frameon=False
            )
            return fig, ax
        return wrapper
    return decorator

def bode_plot(wmin:float=0, wmax:float=1, grid:bool=True, xlabel:str='ω→', ylabel_abs:str='', ylabel_phase:str='') -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            ax[0].set_xlabel(xlabel)
            ax[0].set_ylabel(ylabel_abs)
            ax[0].set_xlim(xmin=wmin, xmax=wmax)
            ax[0].grid(visible=grid, zorder=-1)
            ax[1].set_xlabel(xlabel)
            ax[1].set_ylabel(ylabel_phase)
            ax[1].grid(visible=grid, zorder=-1)
            fig, ax = plot_fcn(fig, ax, *args, **kwargs)
            ax[0].legend(
                handles=[line for line in ax[0].lines if not line._label.startswith('_')],
                ncol=len(ax[0].lines),
                loc='upper center',
                bbox_to_anchor=(0.5, 1.1),
                frameon=False
            )
            return fig, ax
        return wrapper
    return decorator