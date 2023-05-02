from .Layout import Layout, grid_layout

from ..Circuit.solution import TimeDomainSolution, TimeDomainFunction
from dataclasses import dataclass

from typing import Any
import numpy as np

@dataclass
class TimeSeriesSignalPlot:
    solution: TimeDomainSolution
    tmax: float
    tmin: float = 0
    N_samples: int = 200
    signal_label: str = ''
    layout: Layout = grid_layout

    def __post_init__(self):
        self.fig, self.ax = self.layout()
        self._signal_plot_config: dict[str, dict[str, Any]] = {}
        self.ax.set_xlabel('$t\\rightarrow$')
        self.ax.set_ylabel(f'${self.signal_label}\\rightarrow$')
        self.ax.set_xlim(xmin=self.tmin, xmax=self.tmax)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        t = np.linspace(self.tmin, self.tmax, self.N_samples)
        for signal, kwargs in self._signal_plot_config.items():
            x = self._signal(signal)
            self.ax.plot(t, x(t), **kwargs)
        self.ax.legend(
            handles=[line for line in self.ax.lines],
            ncol=len(self.ax.lines),
            loc='upper center',
            bbox_to_anchor=(0.5, 1.1),
            frameon=False
        )

    def _signal(self, _) -> TimeDomainFunction:
        return lambda _: np.zeros(1)

class VoltageTimeSeriesPlot(TimeSeriesSignalPlot):
    def __init__(self, solution: TimeDomainSolution, tmax: float, tmin: float = 0, layout: Layout = grid_layout):
        super().__init__(signal_label='v(t)', solution=solution, tmin=tmin, tmax=tmax, layout=layout)

    def _signal(self, signal: str) -> TimeDomainFunction:
        return self.solution.get_voltage(signal)

    def add_voltage(self, id: str, **kwargs):
        kwargs.update({'label' : f'V({id})'})
        self._signal_plot_config.update({id : kwargs})

class CurrentTimeSeriesPlot(TimeSeriesSignalPlot):
    def __init__(self, solution: TimeDomainSolution, tmax: float, tmin: float = 0, layout: Layout = grid_layout):
        super().__init__(signal_label='i(t)', solution=solution, tmin=tmin, tmax=tmax, layout=layout)

    def _signal(self, signal: str) -> TimeDomainFunction:
        return self.solution.get_current(signal)

    def add_current(self, id: str, **kwargs):
        kwargs.update({'label' : f'I({id})'})
        self._signal_plot_config.update({id : kwargs})
