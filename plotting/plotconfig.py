from matplotlib import rc
import matplotlib
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
matplotlib.rcParams.update(
    {'axes.labelsize': 'x-large',
    'axes.titlesize': 'x-large'}  
)