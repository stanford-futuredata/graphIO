import numpy as np 
import matplotlib.pyplot as plt 
import sys
import csv
import matplotlib
import plotconfig


idx = int(sys.argv[1])

titles = ["Strassen MatMult", "FFT", "DCT", "Naive MatMult"]
title = "Spectral I/O Bound vs Published Bound for %s Graph" % titles[idx]

fname = "data/eig.csv"
with open(fname, "r") as f:
    reader = csv.reader(f, delimiter=",")
    next(reader)
    y = []
    x = []
    for r in reader:
        x.append(float(r[0]))
        val = r[idx+1]
        if val != "":
            y.append(float(val))
    x = x[:len(y)]
    if idx == 0:
        x = [(1/np.sqrt(q))**(np.log2(7)) * q for q in x]
    elif idx == 1 or idx == 2:
        x = [1/np.log(q) for q in x]
    else:
        x = [1/np.sqrt(q) for q in x] 
    plt.plot(x,y, "rd-", label="Spectral I/O Bound") 
xlabels = [r"$M\left(\frac{1}{\sqrt{M}}\right)^{\log_2 7}$", r"$\frac{1}{\log(M)}$", r"$\frac{1}{\log(M)}$", r"$\frac{1}{\sqrt{M}}$"]
plt.xlabel(xlabels[idx])
plt.ylabel("Computed I/O Bound")
plt.title(title)
plt.tight_layout()
outnames =["strassen", "fft", "dct", "matmult"]
plt.savefig("plots/eigplotsScaled/%s.png" % outnames[idx], figsize=(5,6))
# plt.show()

