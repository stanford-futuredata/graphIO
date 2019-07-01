import core.solver as solver
import numpy as np

def convolve(n):
    transformA = np.array(solver.transform_array(list(range(n))))
    transformB = np.array(solver.transform_array(list(range(n))))
    np.convolve(transformA, transformB)