from .Layout import TimeSeriesPlot
from ..Circuit.solution import TimeDomainSolution

from dataclasses import dataclass
import numpy as np

@dataclass
class VoltageTimeSeriesPlot:
    time_series_plot: TimeSeriesPlot
    solution: TimeDomainSolution
    tmax: float
    tmin: float = 0
    N_samples: int = 200

    def add_voltage(self, id: str, **kwargs):
        t = np.linspace(self.tmin, self.tmax, self.N_samples)
        x = self.solution.get_voltage(id)
        self.time_series_plot.add_signal(t, x(t), f'V({id})', **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.time_series_plot.draw()

@dataclass
class CurrentTimeSeriesPlot:
    time_series_plot: TimeSeriesPlot
    solution: TimeDomainSolution
    tmax: float
    tmin: float = 0
    N_samples: int = 200

    def add_current(self, id: str, **kwargs):
        t = np.linspace(self.tmin, self.tmax, self.N_samples)
        x = self.solution.get_current(id)
        self.time_series_plot.add_signal(t, x(t), f'I({id})', **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.time_series_plot.draw()
