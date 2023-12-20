import numpy as np

def step(t: np.ndarray, t0: float, X0: float = 0, X1: float = 1):
    return (X1-X0)*np.array(t > t0, dtype=float)+X0