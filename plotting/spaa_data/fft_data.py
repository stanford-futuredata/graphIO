# t = [2,3,4,5,6]
import numpy as np

graph_name = r"for $2^l$ point FFT"
x_label = r"$l$"
x_bound_label = r"$l2^l$"
out_name = "fft"
n=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
M = [4, 8, 16]
def get_bound(n_):
    return n_ * 2**n_
spectral = {
    4: [0, 0, 0, 0, 6.376856849, 32.40394228, 86.24047963, 208.9615057, 475.4957759, 1044.543809, 2084.001946, 3975.91029, 7444.191387, 13842.58248],
    8: [0, 0, 0, 0, 0, 7.229978328, 49.41899139, 143.5412504, 352.2457386, 801.2226984, 1772.001946, 3663.91029, 7132.191387, 13530.58248],
    16: [0, 0, 0, 0, 0, 0, 5.830126578, 74.62271264, 242.7002573, 603.7707516, 1374.91235, 3040.277448, 6508.191387, 12906.58248],
}

convcut = {
    4: [0, 0, 0, 8, 8, 24, 24, 56, 56, 120],
    8: [0, 0, 0, 0, 0, 16, 16, 48, 48, 112],
    16: [0, 0, 0, 0, 0, 0, 0, 32, 32, 96],
}
