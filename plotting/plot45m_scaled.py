import matplotlib.pyplot as plt
import csv
import sys
import numpy as np

import plotconfig

titles = ["FFT", "Naive MatMult", "Strassen", "DCT"]
titles = ["I/O Bound vs Analytical Bound for %s" % t for t in titles]

filenames =["fft", "matmult", "strassen", "dct"]
filenames = ["data/45plots/%s.csv" % t for t in filenames]

xlabels = [r"$l2^l$", r"$n^3$", r"$n^{\log_2 7}$", r"$l2^l$"]

idx = int(sys.argv[1])

def get_vals(a,b):
    b = [x for x in b if x != -1]
    a = a[:len(b)]
    if idx == 0 or idx == 3:
        a = [q*(2**q) for q in a]
    elif idx == 1:
        a = [q**3 for q in a]
    else:
        a = [(q)**(np.log2(7)) for q in a]
    return a,b

with open(filenames[idx], "r") as f:
    reader = csv.reader(f, delimiter=",")
    # next(reader, None) # skip header
    vals = []
    for r in reader:
        arr = []
        for x in r:
            if x == "":
                arr.append(-1)
            else:
                arr.append(float(x))
        vals.append(arr)
    vals = np.array(vals).T
    # vals = np.array([ [float(x) for x in r] for r in reader]).T

    x, y = get_vals(vals[0], vals[3])
    plt.plot(x,y, "rd-", label="Spectral, M=4")
    x, y = get_vals(vals[0], vals[4])
    plt.plot(x,y, "rd:", label="Spectral, M=5")
    x, y = get_vals(vals[0], vals[1])
    plt.plot(x, y, "b*-", label="Partitioned ILP, M=4")
    x, y = get_vals(vals[0], vals[2])
    plt.plot(x,y, "b*:", label="Partitioned ILP, M=5")
    x,y = get_vals(vals[0], vals[5])
    plt.plot(x,y,"co-", label="Convex min-cut, M=4")
    x,y = get_vals(vals[0], vals[6])
    plt.plot(x,y,"co:", label="Convex min-cut, M=5")
    # plt.plot(vals[0], vals[5], label="Inputs + Outputs")

# if idx == 2: # strassen:
#     plt.xticks(vals[0])
plt.title(titles[idx])
plt.xlabel(xlabels[idx])
plt.ylabel("Computed I/O Bound")
plt.legend()

outnames =["fft", "matmult", "strassen", "dct"]
plt.savefig("plots/45plotsScaled/%s.png" % outnames[idx])
# plt.show()

