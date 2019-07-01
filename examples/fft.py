import numpy as np 
import core.state as state
import core.solver as solver

def combine_fns(N):
    factor = np.exp(-2j * np.pi * np.arange(N) / N)
    half = int(N/2)
    factor_top = factor[:half]
    factor_bottom = factor[half:]
    def outer(i, top):
        def inner(vals):
            a, b = vals[0], vals[1]
            if top:
                v = factor_top[i]
            else:
                v = factor_bottom[i]
            return np.round(a + v*b, 5)
        return inner
    return [outer(i,True) for i in range(half)], [outer(i, False) for i in range(half)]

def fft(x):
    N = len(x)
    if N == 1:
        return x 
    assert N%2 == 0
    X_even = fft(x[::2])
    X_odd = fft(x[1::2])
    top_fns, bottom_fns = combine_fns(N)
    top_result = [solver.genop([X_even[i], X_odd[i]], f) for i,f in enumerate(top_fns)]
    bottom_result = [solver.genop([X_even[i], X_odd[i]], f) for i,f in enumerate(bottom_fns)]
    return np.array(top_result + bottom_result)

def fft_example(t):
    transformA = np.array(solver.transform_array(list(range(2**t))))
    fft(transformA)
