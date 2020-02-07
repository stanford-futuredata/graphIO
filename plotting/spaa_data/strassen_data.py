# t = [2,3,4,5,6]
import numpy as np

graph_name = r"vs $n$ for $n \times n$ Strassen Matmult"
x_label = r"$n$"
x_bound_label = r"$n^{\log_2 7}$"
out_name = "strassen"

n = [4,8,16,32,64]
M = [8, 16, 32]
def get_bound(n_):
    return n_**np.log2(7)

spectral = {
    8: [0, 3.769102254, 225.5542139, 1184.771386, 4807.50277],
    16: [0, 0, 111.8051403, 1040.771386, 4663.5027],
    32: [0, 0, 0, 752.7713864, 4375.5027],
}
convcut = {
    8: [10, 42, 106],
    16: [0, 26, 90],
    32: [0, 0, 58],
}

