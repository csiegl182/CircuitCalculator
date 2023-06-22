import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

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

FigureAxes = tuple[Figure, Axes]
Layout = Callable[[], FigureAxes]
PlotFcn = Callable[[Figure, Axes], FigureAxes]

def default_layout(**kwargs) -> FigureAxes:
    return plt.subplots(ncols=1, nrows=1, **kwargs)

def grid_layout(grid: bool = True, **kwargs) -> FigureAxes:
    fig, ax = default_layout(**kwargs)
    ax.grid(visible=grid, zorder=-1)
    return fig, ax

def figure_default() -> FigureAxes:
    return plt.subplots()

def apply_plt_fcn(fig, ax, *args: PlotFcn) -> FigureAxes:
    for plt_fcn in args:
        plt_fcn(fig, ax)
    return fig, ax

def timeseries_plot(tmin:float=0, tmax:float=1, grid:bool=True, xlabel:str='t→', ylabel:str='') -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_xlim(xmin=tmin, xmax=tmax)
            ax.grid(visible=grid, zorder=-1)
            fig, ax = plot_fcn(fig, ax, *args, **kwargs)
            ax.legend(
                handles=[line for line in ax.lines if not line._label.startswith('_')],
                ncol=len(ax.lines),
                loc='upper center',
                bbox_to_anchor=(0.5, 1.1),
                frameon=False
            )
            return fig, ax
        return wrapper
    return decorator

def pointer_diagram_plot(ax_lim:tuple[float, float, float, float], xlabel:str='', ylabel:str='', grid:bool=True) -> Callable[[PlotFcn], PlotFcn]:
    def decorator(plot_fcn: PlotFcn) -> PlotFcn:
        def wrapper(fig: Figure, ax: Axes, *args, **kwargs) -> FigureAxes:
            ax.grid(visible=grid, zorder=-1)
            ax.set_aspect('equal', 'box')
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_xlim(left=ax_lim[0], right=ax_lim[1])
            ax.set_ylim(bottom=ax_lim[2], top=ax_lim[3])
            fig, ax = plot_fcn(fig, ax, *args, **kwargs)
            ax.legend(
                handles=[line for line in ax.lines if not line._label.startswith('_')],
                ncol=len(ax.lines),
                loc='upper center',
                bbox_to_anchor=(0.5, 1.1),
                frameon=False
            )
            return fig, ax
        return wrapper
    return decorator
