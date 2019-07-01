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

def run_long_test(k):
    M=range(4, 50)
    _, val = compute_eigenvalue_bound(M, k=k)
    print(val)
    for v in val:
        print(v[0])

def run_test(k):
    M=[4,5]
    dc, vals = compute_eigenvalue_bound(M, k=k)
    print(vals)
    v1, v2 = np.real(vals[0][0]), np.real(vals[1][0])
    print("%f,%f" % (v1, v2))
t = int(sys.argv[1])
k = int(sys.argv[2])

dct_example(t)
#fft_example(t)
#convolve(t)
#matmult(t)
#strassen_matmult(t)
#checkerboard(t)
run_test(k)
