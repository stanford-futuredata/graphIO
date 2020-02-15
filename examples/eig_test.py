import sys
import os
import numpy as np
sys.path.append('..')
import core.solver as solver
from convolve import convolve
from fft import fft_example
from matmult import matmult, strassen_matmult
from core.eig_solver import compute_eigenvalue_bound
from dct import dct_example
from hypercube import tsp

def run_long_test(k):
    M=range(4, 50)
    _, val = compute_eigenvalue_bound(M, k=k)
    print(val)
    for v in val:
        print(v[0])

def run_test(k, M):
    dc, vals = compute_eigenvalue_bound(M, k=k)
    out = []
    for i, M_ in enumerate(M):
        val = vals[i]
        out.append((M_, val[0], val[1]))
    print(out)

def matmult_test():
    M = [64, 128, 256]
    t = np.arange(4, 65, 4)
    for t_ in t:
        print(t_)
        matmult(t_, alltogether=True)
        solver.stats()
        run_test(10, M)
        solver.clear_graph()

def strassen_matmult_test():
    M = [64, 128, 256]
    t = [6]
    for t_ in t:
        print(t_, 2**t_)
        strassen_matmult(t_, alltogether=True)
        solver.stats()
        run_test(10, M)
        solver.clear_graph()

def hypercube_test():
    M = [8, 16, 32, 64]
    t = list(range(4, 20))
    for t_ in t:
        tsp(t_)
        solver.stats()
        max_eigs = min(2**t_ - 5, 100)
        print("max eigs", max_eigs)
        run_test(max_eigs, M)
        solver.clear_graph()

hypercube_test()

# t = int(sys.argv[1])
# k = int(sys.argv[2])

# fft_example(t)
# dct_example(t)
# matmult(t, alltogether=True)
# strassen_matmult(t, alltogether=True)

# solver.stats()
#convolve(t)
#matmult(t)
#checkerboard(t)
# run_test(k)
