import numpy as np
import sys
sys.path.append('..')
import core.solver as solver
from convolve import convolve
import core.state as state
from fft import fft_example
from matmult import matmult

def relabel_graph(X):
    G = state.GRAPH
    n = len(G.nodes)
    for i in range(n):
        num = np.argmax(X[:,i])
        G.nodes[num]['label'] = i
    solver.render()

filename = "results/matmult/5.gz"
X = np.loadtxt(filename)
print(X)
matmult(2)
# convolve(3)
# fft_example(2)
relabel_graph(X)
solver.render("pics/matmult5.png")

