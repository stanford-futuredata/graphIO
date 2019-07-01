import numpy as np 
import matplotlib.pyplot as plt 
import sys
import csv


import plotconfig

idx = int(sys.argv[1])

titles = ["Strassen MatMult", "FFT", "DCT", "Naive MatMult"]
title = "Spectral I/O Bound vs M for %s Graph" % titles[idx]

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
    plt.plot(x,y, "rd-", label="Spectral I/O Bound") 

plt.xlabel(r"$M$")
plt.ylabel("Computed I/O Bound")
plt.title(title)
# plt.tight_layout()
outnames =["strassen", "fft", "dct", "matmult"]
plt.savefig("plots/eigplots/%s.png" % outnames[idx], figsize=(5,6))
# plt.show()

