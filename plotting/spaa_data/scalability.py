import matplotlib.pyplot as plt
import numpy as np
line_styles = ['-', '--', ':']

from matplotlib import rc
import matplotlib
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
matplotlib.rcParams.update(
    {
    'figure.figsize': (7, 5),
    'axes.labelsize': '20',
    'axes.titlesize': '22',
    'legend.fontsize': '15'
    }  
)

conv_cut = [0.2716805935, 0.559458971, 1.429104567, 3.763284445, 14.65016651, 68.40330386, 302.4113715, 1828.702686, 7084.760864, 30528.0612]

spectral = [0.009168148041, 0.08392333984, 5.758724928, 10.03717852, 13.07910752, 15.95279455, 26.88208318, 30.17740083, 81.54666233, 98.2076473]

t_ = np.arange(6, 16)

plt.plot(t_, spectral, 'rd-', label="Spectral")
plt.plot(t_, conv_cut, 'b.-', label="Convex Min-cut")
plt.tick_params(labelsize=15)
plt.xticks(t_)
plt.legend()
plt.title(r"Runtime (s) vs $l$ for $l$ city TSP")
plt.xlabel(r"$l$")
plt.ylabel("Runtime (s)")
plt.savefig(f"scalability.pdf", bbox_inches="tight")
plt.show()