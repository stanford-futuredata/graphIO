import sys
import os
import numpy as np
sys.path.append('..')
import core.solver as solver
from convolve import convolve
from fft import fft_example
from matmult import matmult, strassen_matmult
from core.elango_solver import get_elango_bound
from dct import dct_example


t = int(sys.argv[1])
M = int(sys.argv[2])

#dct_example(t)
#fft_example(t)
#convolve(t)
#matmult(t)
strassen_matmult(t)
print(get_elango_bound(M))
