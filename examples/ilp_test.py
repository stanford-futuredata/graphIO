import sys
import numpy as np
sys.path.append('..')
import core.solver as solver
from matmult import strassen_matmult
from convolve import convolve
from dct import dct_example
from core.partition_solver import ILP_Bound, relabel_graph

def run_test(M):
    S = ILP_Bound()
    X, _ = S.solve_ILP(M)
    X, value = X
    print(X)
    np.savetxt("outstras.gz", X)
    # relabel_graph(X)
    print(value)

#dct_example(2)
strassen_matmult(1)
run_test(4)
