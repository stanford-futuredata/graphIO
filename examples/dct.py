import sys
import os
import numpy as np
sys.path.append('..')
import core.solver  as solver
import math

def transform(vector):
    n = len(vector)
    if n == 1:
        return list(vector)
    elif n == 0 or n % 2 != 0:
        raise ValueError()
    else:
        half = n // 2
        alpha = [(vector[i] + vector[-(i + 1)]) for i in range(half)]
        beta  = [(vector[i] - vector[-(i + 1)]) for i in range(half)]
        # beta  = [(vector[i] - vector[-(i + 1)]) / (math.cos((i + 0.5) * math.pi / n) * 2.0) for i in range(half)]
        alpha = transform(alpha)
        beta  = transform(beta)
        result = []
        for i in range(half - 1):
            result.append(alpha[i])
            result.append(beta[i] + beta[i + 1])
        result.append(alpha[-1])
        result.append(beta [-1])
        return result


def dct_example(t):
    n = 2**t
    arr = np.array(solver.transform_array(range(n)))
    transform(arr)


