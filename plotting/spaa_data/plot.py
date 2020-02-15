# import strassen_data as dat
# import matmult_data as dat
# import fft_data as dat
import tsp_data as dat


import matplotlib.pyplot as plt

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

def plot_all(scaled):
    n = dat.n
    if scaled:
        n = [dat.get_bound(u) for u in n]
    num_ticks = 0
    for i, M in enumerate(dat.M):
        num_ticks = max(num_ticks, plot(n, M, line_styles[i], plot_both=(not scaled)))
    plt.legend()
    if not scaled:
        plt.xticks(n[:num_ticks])
    if scaled:
        title = "I/O bound vs " + dat.x_bound_label + " " + dat.graph_name
        xlabel = dat.x_bound_label
        
    else:
        title =  "I/O bound vs " + dat.x_label + " " +  dat.graph_name
        xlabel = dat.x_label
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Computed I/O Bound")
    plt.tick_params(labelsize=15)
    if scaled:
        plt.savefig(f"scaled_{dat.out_name}.pdf", bbox_inches="tight")
    else:
        plt.savefig(f"{dat.out_name}.pdf", bbox_inches="tight")
    plt.show()

def plot(n, M, style, plot_both):
    spectral = dat.spectral[M]
    conv_cut = dat.convcut[M]
    if plot_both:
        plt.plot(n[:len(conv_cut)], spectral[:len(conv_cut)], 'rd' + style, label=f"Spectral, M={M}")
        plt.plot(n[:len(conv_cut)], conv_cut, 'b.' + style, label=f"Convex Min-cut, M={M}")
        return len(conv_cut)
    else:
        plt.plot(n[:len(spectral)], spectral, 'rd' + style, label=f"Spectral, M={M}")
        return len(spectral)
        # plt.plot(n[:len(conv_cut)], conv_cut, 'b.' + style, label=f"Convex Min-cut, M={M}")

plot_all(True)
plot_all(False)
    