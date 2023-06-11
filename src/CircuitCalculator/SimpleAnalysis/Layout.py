import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from .Elements import complex_pointer

import numpy as np
from  functools import partial
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any

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

    def __post_init__(self) -> None:
        self.fig, self.ax = plt.subplots(nrows=1, ncols=1, sharex=True)
        self.ax.set_xlabel('t→')
        self.ax.set_xlim(xmin=self.tmin, xmax=self.tmax)
        self._signal_plot_config: dict[str, dict[str, Any]] = {}
        self.ax.set_ylabel(f'{self.y_label}')
        self.ax.grid(visible=True, zorder=-1)

    def add_signal(self, x: np.ndarray, y: np.ndarray, label: str, **kwargs) -> None:
        self.signal_args.update({label : {'x': x, 'y': y, 'kwargs': kwargs}})

    def draw(self) -> None:
        for label, signal in self.signal_args.items():
            self.ax.plot(signal['x'], signal['y'], label=label, **signal['kwargs'])
        self.ax.legend(
            handles=[line for line in self.ax.lines],
            ncol=len(self.ax.lines),
            loc='upper center',
            bbox_to_anchor=(0.5, 1.1),
            frameon=False
        )

@dataclass
class PointerDiagram:
    arrow_base: float = 0.05
    arrow_length: float = 0.05
    xlabel: str = ''
    ylabel: str = ''

    def __post_init__(self) -> None:
        self.fig, self.ax = plt.subplots(ncols=1, nrows=1)
        self.ax.grid(visible=True, zorder=-1)
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.pointer_drawers = []
        self._max_length = 0

    def add_pointer(self, z: complex, z0: complex = 0, **kwargs) -> None:
        self._max_length = max(self._max_length, np.abs(z))
        self.pointer_drawers.append(partial(complex_pointer, self.ax, z0, z0+z, **kwargs))

    def draw(self) -> None:
        for draw_pointer in self.pointer_drawers:
            draw_pointer(height=self.arrow_base*self._max_length, width=self.arrow_length*self._max_length)
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()
        self.ax.set_xlim(xmin=min(x_min, y_min), xmax=max(x_max, y_max))
        self.ax.set_ylim(ymin=min(x_min, y_min), ymax=max(x_max, y_max))
        self.ax.legend(
            handles=[line for line in self.ax.lines],
            ncol=len(self.ax.lines),
            loc='upper center',
            bbox_to_anchor=(0.5, 1.1),
            frameon=False
        )

@dataclass
class NyquistPlot:
    xlabel: str = ''
    ylabel: str = ''
    signal_args: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.fig, self.ax = plt.subplots(ncols=1, nrows=1)
        self.ax.grid(visible=True, zorder=-1)
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)

    def add_plot(self, z: complex, w: float, label: str, **kwargs) -> None:
        self.signal_args.update({label : {'z': z, 'w': w, 'kwargs': kwargs}})

    def draw(self) -> None:
        for label, signal in self.signal_args.items():
            self.ax.plot(np.real(signal['z']), np.imag(signal['z']), label=label, **signal['kwargs'])
        self.ax.legend(
            handles=[line for line in self.ax.lines],
            ncol=len(self.ax.lines),
            loc='upper center',
            bbox_to_anchor=(0.5, 1.1),
            frameon=False
        )