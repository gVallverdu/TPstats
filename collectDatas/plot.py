import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from matplotlib.gridspec import GridSpec

# import matplotlib.pyplot as plt

TANGO_HTML_COLORS = {"butter1": "#fce94f",
                     "butter2": "#edd400",
                     "butter3": "#c4a000",
                     "orange1": "#fcaf3e",
                     "orange2": "#f57900",
                     "orange3": "#ce5c00",
                     "chocolate1": "#e9b96e",
                     "chocolate2": "#c17d11",
                     "chocolate3": "#8f5902",
                     "chameleon1": "#8ae234",
                     "chameleon2": "#73d216",
                     "chameleon3": "#4e9a06",
                     "skyblue1": "#729fcf",
                     "skyblue2": "#3465a4",
                     "skyblue3": "#204a87",
                     "plum1": "#ad7fa8",
                     "plum2": "#75507b",
                     "plum3": "#5c3566",
                     "scarletred1": "#ef2929",
                     "scarletred2": "#cc0000",
                     "scarletred3": "#a40000",
                     "aluminium1": "#eeeeec",
                     "aluminium2": "#d3d7cf",
                     "aluminium3": "#babdb6",
                     "aluminium4": "#888a85",
                     "aluminium5": "#555753",
                     "aluminium6": "#2e3436"}

COLOR_NAMES = ["scarletred", "chameleon", "skyblue", "orange", "plum",
               "chocolate", "butter", "aluminium"]

# COLOR_NAMES = ["butter", "chameleon", "skyblue", "plum",
#                "scarletred", "orange", "chocolate", "aluminium"]
COLOR_NAMES2 = [c for c in COLOR_NAMES for i in range(2)]


def normpdf(x, mu, sigma):
    """ normal distribution """
    return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu)**2 / (2 * sigma**2))


def normcdf(x, mu, sigma, alpha=1):
    """ cdf of the normal distribution """
    return 0.5 * (1 + erf(alpha * (x - mu) / (sigma * np.sqrt(2))))


def skewed(x, mu, sigma, alpha, a):
    """ a skewed distribution """
    return a * normpdf(x, mu, sigma) * normcdf(x, mu, sigma, alpha)


def make_box_plot(ax, data, disp=0.05, shift=-.4):
    """
    Returns a box plot of the data. `data` must be a dictionnary where the keys
    are the labels to be used as abscissa and the values are a list or an iterable
    and plotable object.

    Args :
        ax (matplotlib.Axes): axes of the plot
        data (dict): dict such as {"label": [x1, x2, ...], "label": [x1, x2, ...]}
        disp (float): dispertion of the points
        shift (float): shift between the box and the points

    Returns:
        ax
    """

    # look for the plot range
    minval = np.floor(min([v for values in data.values() for v in values]))
    maxval = np.ceil(max([v for values in data.values() for v in values]))

    # make the box plots
    bp = ax.boxplot(list(data.values()), sym="", patch_artist=True)
    for box, color in zip(bp["boxes"], COLOR_NAMES):
        box.set(color=TANGO_HTML_COLORS[color + "3"],
                linewidth=2,
                facecolor=TANGO_HTML_COLORS[color + "2"],
                alpha=.6)

    for median, color in zip(bp["medians"], COLOR_NAMES):
        median.set(color=TANGO_HTML_COLORS[color + "3"],
                   linewidth=2)

    for whisker, color in zip(bp["whiskers"], COLOR_NAMES2):
        whisker.set(color=TANGO_HTML_COLORS[color + "3"],
                    linestyle="-",
                    linewidth=2)

    for cap, color in zip(bp["caps"], COLOR_NAMES2):
        cap.set(color=TANGO_HTML_COLORS[color + "3"],
                linewidth=2)

    # add data as points
    ndata = len(data)
    for pos, measures, label, color in zip(range(ndata), data.values(), data.keys(), COLOR_NAMES):
        position = pos + 1 + shift
        x = disp * (2 * np.random.random(len(measures))) + position
        ax.plot(x, list(measures), "o", color=TANGO_HTML_COLORS[color + "2"], label=label, alpha=.5)

    ax.set_xlim(0, ndata + .5)
    ax.set_ylim(minval, maxval)
    ax.set_xticks(range(1, ndata + 1))
    ax.set_xticklabels(data.keys())
    ax.set_ylabel("Volume (mL)")
    ax.grid(axis="x")

    return ax


def make_hist_plot(fig, data, nbins=10, target=10., ylabel="Volume (mL)"):
    """
    Returns a plot of the data as histograms. `data` must be a dictionnary where
    the keys are the labels to be used as abscissa and the values are a list or
    an iterable and plotable object.

    Args :
        fig (matplotlib.figure): figure for the plot
        data (dict): dict such as {"label": [x1, x2, ...], "label": [x1, x2, ...]}
        target (float): expected values of the measurements
        ylabel (string): label of y axis

    Returns:
        ax
    """

    # make a grid
    gs = GridSpec(1, 2, width_ratios=[1, 1])
    gs.update(wspace=0)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    # look for the plot range
    minval = np.floor(min([v for values in data.values() for v in values]))
    maxval = np.ceil(max([v for values in data.values() for v in values]))
    xfunc = np.linspace(minval, maxval, 200)

    # make plot for each data
    for key, color in zip(data, COLOR_NAMES):
        measures = data[key]
        hval, bins = np.histogram(measures, bins=nbins, normed=True)
        xval = [b + (bins[1] - bins[0]) / 2 for b in bins[:-1]]

        sigma = np.std(measures)
        mu = np.mean(measures)
        maxd = np.max(measures)
        try:
            popt, pcov = curve_fit(skewed, xval, hval, p0=(mu, sigma, 1, maxd))
            ax2.plot(skewed(xfunc, *popt), xfunc,
                     linewidth=2,
                     alpha=.8,
                     color=TANGO_HTML_COLORS[color + "3"],
                     label=key + " (s)")
        except:
            popt, pcov = curve_fit(normpdf, xval, hval, p0=(mu, sigma))
            ax2.plot(normpdf(xfunc, *popt), xfunc,
                     linewidth=2,
                     alpha=.8,
                     color=TANGO_HTML_COLORS[color + "3"],
                     label=key + " (n)")

        ax1.plot(data[key], "o", color=TANGO_HTML_COLORS[color + "3"], alpha=.75)

    ax1.axhline(target, color="gray", linestyle="dashed", linewidth=2)
    ax2.axhline(target, color="gray", linestyle="dashed", linewidth=2)

    ax2.set_yticklabels([])
    ax2.set_xticklabels([])
    ax2.set_xlabel("Densities")
    ax2.set_ylim(minval, maxval)
    ax2.grid(True)

    ax1.set_ylabel(ylabel)
    ax1.set_xlabel("Measures")
    ax1.set_xticklabels([])
    ax1.set_ylim(minval, maxval)
    ax1.grid(True)

    ax2.legend(ncol=int(len(data) / 2 + 1), loc="upper right",
               bbox_to_anchor=(1, 1.12), fontsize=14)

    return fig
