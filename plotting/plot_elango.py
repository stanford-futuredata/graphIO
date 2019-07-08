import numpy as np 
import matplotlib.pyplot as plt
import plotconfig
X = np.loadtxt("data/elango.csv", delimiter=",").T
disk = X[0]
elango = X[1]
x = np.arange(2, 9)
plt.plot(x,disk,"*-",label="Trivial I/O")
plt.plot(x, elango, ".-",label="2S Partition Bound")
plt.legend()
plt.title("2S Partition Bound and Trivial I/O for FFT Graph")
plt.xlabel("FFT Level")
plt.ylabel("I/O")
plt.savefig("plots/elango.png")
# plt.show()
