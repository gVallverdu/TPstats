import numpy as np
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


def make_box_plot(ax, data, disp=0.05, shift=-.4):

    colors = ["butter", "chameleon", "skyblue", "plum", "scarletred"]
    colorsx2 = [c for c in colors for i in range(2)]

    # make the box plots
    bp = ax.boxplot(list(data.values()), sym="", patch_artist=True)
    for box, color in zip(bp["boxes"], colors):
        box.set(color=TANGO_HTML_COLORS[color + "3"],
                linewidth=2,
                facecolor=TANGO_HTML_COLORS[color + "2"],
                alpha=.6)

    for median, color in zip(bp["medians"], colors):
        median.set(color=TANGO_HTML_COLORS[color + "3"],
                   linewidth=2)

    for whisker, color in zip(bp["whiskers"], colorsx2):
        whisker.set(color=TANGO_HTML_COLORS[color + "3"],
                    linestyle="-",
                    linewidth=2)

    for cap, color in zip(bp["caps"], colorsx2):
        cap.set(color=TANGO_HTML_COLORS[color + "3"],
                linewidth=2)

    # add data as points
    ndata = len(data)
    for pos, measures, label, color in zip(range(ndata), data.values(), data.keys(), colors):
        position = pos + 1 + shift
        x = disp * (2 * np.random.random(len(measures))) + position
        ax.plot(x, list(measures), "o", color=TANGO_HTML_COLORS[color + "2"], label=label, alpha=.5)

    ax.set_xlim(0, ndata + .5)
    ax.set_xticks(range(1, ndata + 1))
    ax.set_xticklabels(data.keys())
    ax.set_ylabel("Volume (mL)")
    ax.grid(axis="x")

    return ax
