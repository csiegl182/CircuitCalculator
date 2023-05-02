import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import Callable, List, Dict, Any
import numpy as np
from dataclasses import dataclass, field

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

FigureAxes = tuple[Figure, List[Axes]]
Layout = Callable[[], FigureAxes]

def default_layout(**kwargs) -> tuple[Figure, Axes]:
    return plt.subplots(ncols=1, nrows=1, **kwargs)

def grid_layout(grid: bool = True, **kwargs) -> tuple[Figure, Axes]:
    fig, ax = default_layout(**kwargs)
    ax.grid(visible=grid, zorder=-1)
    return fig, ax

@dataclass
class TimeSeriesPlot:
    tmax: float
    tmin: float = 0
    y_label: str = ''
    signal_args: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.fig, self.ax = plt.subplots(nrows=1, ncols=1, sharex=True)
        self.ax.set_xlabel('t→')
        self.ax.set_xlim(xmin=self.tmin, xmax=self.tmax)
        self._signal_plot_config: dict[str, dict[str, Any]] = {}
        self.ax.set_ylabel(f'{self.y_label}')
        self.ax.grid(visible=True, zorder=-1)

    def add_signal(self, x: np.ndarray, y: np.ndarray, label: str, **kwargs) -> None:
        self.signal_args.update({label : {'x': x, 'y': y, 'kwargs': kwargs}})

    def draw(self):
        for label, signal in self.signal_args.items():
            self.ax.plot(signal['x'], signal['y'], label=label, **signal['kwargs'])
        self.ax.legend(
            handles=[line for line in self.ax.lines],
            ncol=len(self.ax.lines),
            loc='upper center',
            bbox_to_anchor=(0.5, 1.1),
            frameon=False
        )