  
from typing import Callable, Tuple
import numpy as np

TimeDomainFunction = Callable[[np.ndarray], np.ndarray]
FrequencyDomainFunction = Tuple[np.ndarray, np.ndarray]