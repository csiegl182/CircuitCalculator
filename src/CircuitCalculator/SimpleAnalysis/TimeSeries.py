from .Layout import Layout, grid_layout

from ..Network.solution import NetworkSolution

from typing import Any
import numpy as np

class TimeSeriesSignalPlot:
    def __init__(self, solution: NetworkSolution, w: float, tmax: float, tmin: float = 0, signal_label: str = '', layout: Layout = grid_layout):
        self.fig, self.ax = layout()
        self._solution = solution
        self._w = w
        self._tmin = tmin
        self._tmax = tmax
        self._signal_plot_config: dict[str, dict[str, Any]] = {}
        self.ax.set_xlabel('$t\\rightarrow$')
        self.ax.set_ylabel(f'${signal_label}\\rightarrow$')
        self.ax.set_xlim(xmin=self._tmin, xmax=self._tmax)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        t = np.linspace(self._tmin, self._tmax, 200)
        for signal, kwargs in self._signal_plot_config.items():
            X = self._amplitude_phase(signal)
            v = np.abs(X)*np.cos(self._w*t+np.angle(X))
            self.ax.plot(t, v, **kwargs)
        self.ax.legend(
            handles=[line for line in self.ax.lines],
            ncol=len(self.ax.lines),
            loc='upper center',
            bbox_to_anchor=(0.5, 1.1),
            frameon=False
        )

    def _amplitude_phase(self, _: str) -> complex:
        return 0

class VoltageTimeSeriesPlot(TimeSeriesSignalPlot):
    def __init__(self, solution: NetworkSolution, w: float, tmax: float, tmin: float = 0, layout: Layout = grid_layout):
        super().__init__(signal_label='v(t)', solution=solution, w=w, tmin=tmin, tmax=tmax, layout=layout)

    def _amplitude_phase(self, signal: str) -> complex:
        return self._solution.get_voltage(signal)

    def add_voltage(self, id: str, **kwargs):
        kwargs.update({'label' : f'V({id})'})
        self._signal_plot_config.update({id : kwargs})

class CurrentTimeSeriesPlot(TimeSeriesSignalPlot):
    def __init__(self, solution: NetworkSolution, w: float, tmax: float, tmin: float = 0, layout: Layout = grid_layout):
        super().__init__(signal_label='i(t)', solution=solution, w=w, tmin=tmin, tmax=tmax, layout=layout)

    def _amplitude_phase(self, signal: str) -> complex:
        return self._solution.get_current(signal)

    def add_current(self, id: str, **kwargs):
        kwargs.update({'label' : f'I({id})'})
        self._signal_plot_config.update({id : kwargs})
