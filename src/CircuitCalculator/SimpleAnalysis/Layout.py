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

Layout = Callable[[], tuple[Figure, Axes]]

def default_layout(**kwargs) -> tuple[Figure, Axes]:
    return plt.subplots(ncols=1, nrows=1, **kwargs)

def grid_layout(grid: bool = True, **kwargs) -> tuple[Figure, Axes]:
    fig, ax = default_layout(**kwargs)
    ax.grid(visible=grid, zorder=-1)
    return fig, ax