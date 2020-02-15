fft = {
    "3_upper": [15,11,8],
    "3_lower": [11, 5, 3],
    "4_upper": [61, 55, 38]
}
M = [4, 5, 6]

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

plt.xticks(M)
plt.plot(M, fft['3_upper'], 'bo-', label=r"$2^3$ point FFT, upper")
plt.plot(M, fft['3_lower'], 'bo:', label=r"$2^3$ point FFT, lower")
plt.plot(M, fft['4_upper'], 'ro-', label=r"$2^4$ point FFT, upper")
plt.fill_between(M, fft['3_upper'], fft['3_lower'], edgecolor='b', hatch='//', color="none", linewidth=0.0)
plt.title("ILP Upper/Lower Bounds for FFT")
plt.xlabel(r"$M$")
plt.ylabel(r"Computed I/O Bound")
plt.legend()
plt.savefig("ilp_fft.pdf")
plt.show()
    