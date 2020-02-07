# import strassen_data as dat
# import matmult_data as dat
# import fft_data as dat
import dct_data as dat


import matplotlib.pyplot as plt

line_styles = ['-', ':', '-.']

from matplotlib import rc
import matplotlib
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
matplotlib.rcParams.update(
    {
    'axes.labelsize': '14',
    'axes.titlesize': '18',
    }  
)

def plot_all(scaled):
    n = dat.n
    if scaled:
        n = [dat.get_bound(u) for u in n]
    for i, M in enumerate(dat.M):
        plot(n, M, line_styles[i])
    plt.legend()
    if not scaled:
        plt.xticks(n)
    if scaled:
        title = "Analytical bound " + dat.graph_name
        xlabel = dat.x_bound_label
        
    else:
        title =  "I/O bound " + dat.graph_name
        xlabel = dat.x_label
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Computed I/O Bound")
    if scaled:
        plt.savefig(f"scaled_{dat.out_name}.png")
    else:
        plt.savefig(f"{dat.out_name}.png")
    plt.show()

def plot(n, M, style):
    spectral = dat.spectral[M]
    conv_cut = dat.convcut[M]
    plt.plot(n[:len(spectral)], spectral, 'rd' + style, label=f"Spectral, M={M}")
    plt.plot(n[:len(conv_cut)], conv_cut, 'b.' + style, label=f"Convex Min-cut, M={M}")

plot_all(True)
plot_all(False)
    