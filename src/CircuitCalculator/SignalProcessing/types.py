  
from typing import Callable, Tuple
import numpy as np
from .state_space_model import NumericStateSpaceModel

TimeDomainFunction = Callable[[np.ndarray], np.ndarray]
TimeDomainSeries = Tuple[np.ndarray, np.ndarray]
FrequencyDomainSeries = Tuple[np.ndarray, np.ndarray]

StateSpaceSolver = Callable[[NumericStateSpaceModel, np.ndarray, np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray, np.ndarray]]