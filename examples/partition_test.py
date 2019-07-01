import sys
import os
import numpy as np
sys.path.append('..')
import core.solver as solver
from convolve import convolve
from fft import fft_example
from matmult import matmult, strassen_matmult
from core.partition_solver import ILP_Bound, relabel_graph
from dct import dct_example
def run_test(M, dirname):
    S = ILP_Bound()
    os.makedirs(dirname)
    value = S.solve_lb(M, dirname)
    # np.savetxt("out.gz", X)
    print(value)

t = int(sys.argv[1])
M = int(sys.argv[2])
print("---------------------------------------------------------------")
print("---------------------------------------------------------------")
print("----------------------%d, %d-----------------------------------" % (t,M))
dirname = "interm_results/strass%d/%d/" % (t, M)
#fft_example(t)
#matmult(t)
#convolve(t)
#dct_example(t)
strassen_matmult(t)
run_test(M, dirname)
