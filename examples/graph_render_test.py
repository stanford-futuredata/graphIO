import sys
import numpy as np
sys.path.append('..')
import core.solver as solver
from fft import fft_example
from dct import dct_example
from matmult import matmult, strassen_matmult

# dct_example(3)
# solver.render("dct.png")

# matmult(2)
# solver.render("matmult.png")

# strassen_matmult(1)
# solver.render("strassen.png")

a = np.array(solver.transform_array([1,2]))
b = np.array(solver.transform_array([1,2]))
np.dot(a,b)
solver.render("dot.png")