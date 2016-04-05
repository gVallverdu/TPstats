# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.special import erf
from scipy.optimize import curve_fit


def normpdf(x, mu, sigma):
    """ normal distribution """
    return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu)**2 / (2 * sigma**2))


def normcdf(x, mu, sigma, alpha=1):
    """ cdf of the normal distribution """
    return 0.5 * (1 + erf(alpha * (x - mu) / (sigma * np.sqrt(2))))


def skewed(x, mu, sigma, alpha, a):
    """ a skewed distribution """
    return a * normpdf(x, mu, sigma) * normcdf(x, mu, sigma, alpha)

print(matplotlib.backends.backend)
# load data on becher
becher = np.loadtxt("grid.csv", usecols=(0,), unpack=True, skiprows=1, delimiter=",")

arrowprops = {'arrowstyle': '<|-|>', "linewidth": 2, "color": "#204a87"}

# -------------------------------------------------------------
print("# make hist plot")
# -------------------------------------------------------------
plt.figure(figsize=(8, 6))
plt.rc("font", **{"family": "sans", "size": 18})
plt.grid(False)
plt.title("Histogram plot")
plt.xlabel("Volume (mL)")
plt.ylabel("Normalized histogram")
xmin = 6
xmax = 12
nbins = 12
plt.xlim(xmin, xmax)
step = (xmax - xmin) / nbins
print(step)
bins = [xmin + i * step for i in range(13)]
print(bins)
h, b, p = plt.hist(becher, bins=bins, normed=True, alpha=.8, linewidth=3, color="#3465a4")
print(h)
plt.savefig("collectDatas/static/collectDatas/img/hist_plot.png")

# -------------------------------------------------------------
print("# make hist plot with normal distribution")
# -------------------------------------------------------------
plt.figure(figsize=(8, 6))
plt.rc("font", **{"family": "sans", "size": 18})
plt.grid(False)
plt.title("Normal distribution")
plt.xlabel("Volume (mL)")
plt.ylabel("Normalized distribution")
xmin = 6
xmax = 12
nbins = 12
plt.xlim(xmin, xmax)
step = (xmax - xmin) / nbins
bins = [xmin + i * step for i in range(13)]
h, b, p = plt.hist(becher, bins=bins, normed=True, alpha=.8, linewidth=3, color="#3465a4")
mu, sigma = becher.mean(), becher.std()
print("mu    = ", mu)
print("sigma = ", sigma)
x = np.linspace(xmin, xmax, 200)
y = normpdf(x, mu, sigma)
plt.plot(x, y, color="#cc0000", linewidth=3)
halfmax = max(y) / 2
plt.annotate(
    '', xy=(mu - sigma, normpdf(mu - sigma, mu, sigma)), xycoords='data',
    xytext=(mu + sigma, normpdf(mu + sigma, mu, sigma)), textcoords='data',
    arrowprops={'arrowstyle': '<|-|>', "linewidth": 2, "color": "#cc0000"})
plt.annotate(
    r'2$\sigma$',
    xy=(mu - 0.2, normpdf(mu - sigma, mu, sigma)), xycoords='data',
    xytext=(7, 0.5), textcoords='data',
    color="#204a87", fontsize=24,
    arrowprops={'arrowstyle': '-|>', "linewidth": 2, "color": "#cc0000"})

plt.savefig("collectDatas/static/collectDatas/img/hist_plot_normal.png")

# -------------------------------------------------------------
print("# make hist plot with skewed distribution")
# -------------------------------------------------------------

plt.figure(figsize=(8, 6))
plt.rc("font", **{"family": "sans", "size": 18})
plt.grid(False)
plt.title("Skewed distribution")
plt.xlabel("Volume (mL)")
plt.ylabel("Normalized distribution")
xmin = 6
xmax = 12
nbins = 12
plt.xlim(xmin, xmax)
step = (xmax - xmin) / nbins
bins = [xmin + i * step for i in range(13)]
h, b, p = plt.hist(becher, bins=bins, normed=True, alpha=.8, linewidth=3, color="#3465a4")
mu, sigma = becher.mean(), becher.std()
xval = [bi + (b[1] - b[0]) / 2 for bi in b[:-1]]
popt, pcov = curve_fit(skewed, xval, h, p0=(mu, sigma, 1, 1))
print("mu    = ", popt[0])
print("sigma = ", popt[1])
print("alpha = ", popt[2])
print("a     = ", popt[3])
x = np.linspace(xmin, xmax, 200)
plt.plot(x, normpdf(x, mu, sigma), color="#cc0000", linewidth=2, label="normal")
plt.plot(x, skewed(x, *popt), color="#f57900", linewidth=3, label="skewed")
plt.legend()
plt.savefig("collectDatas/static/collectDatas/img/hist_plot_skewed.png")

# -------------------------------------------------------------
print("# make the box plot")
# -------------------------------------------------------------

plt.figure(figsize=(6, 8))
plt.rc("font", **{"family": "sans", "size": 18})
plt.title("Box plot")
plt.ylabel("Volume (mL)")
plt.ylim(6, 12)
plt.grid(False)

bp = plt.boxplot(becher, sym="", patch_artist=True)
[boxes.set(color="#204a87", linewidth=2, alpha=.8, facecolor="#3465a4") for boxes in bp["boxes"]]
[median.set(color="#204a87", linewidth=2) for median in bp["medians"]]
[whisker.set(color="#204a87", linestyle="solid", linewidth=2) for whisker in bp["whiskers"]]
[cap.set(color="#204a87", linewidth=2) for cap in bp["caps"]]
plt.xlim(0.5, 2)

x = 0.05 * np.random.random(len(becher)) + 0.8
plt.plot(x, becher, "o", color="#3465a4", alpha=.75)
plt.xticks([1], ["beaker"])

plt.text(1.1, 9.6, "median", fontsize=18, color="#204a87")
plt.text(1.1, 10.1, "Q3", fontsize=18, color="#204a87")
plt.text(1.1, 8.8, "Q1", fontsize=18, color="#204a87")


Q1, median, Q3 = np.percentile(becher, [25, 50, 75])
IQR = Q3 - Q1

wiskhi = np.compress(becher <= Q3 + 1.5 * IQR, becher)
wisklo = np.compress(becher >= Q1 - 1.5 * IQR, becher)
hival = np.max(wiskhi)
loval = np.min(wisklo)


# for Qi in [Q1, median, Q3, Q3 + 1.5 * IQR, Q1 - 1.5 * IQR]:
#     plt.axhline(Qi, linewidth=2, color="k")

print("median = ", median)
print("Q1     = ", Q1, hival)
print("Q3     = ", Q3, loval)
print("IQR    = ", IQR)


plt.annotate(
    '', xy=(1.5, Q1), xycoords='data',
    xytext=(1.5, Q3), textcoords='data',
    arrowprops=arrowprops)
plt.text(1.51, Q1 + .5 * IQR, '50%', color="#204a87", rotation=270)
plt.annotate(
    '', xy=(1.7, loval), xycoords='data',
    xytext=(1.7, hival), textcoords='data',
    arrowprops=arrowprops)
plt.text(1.71, Q1 + .5 * IQR, '99.3%', color="#204a87", rotation=-90)

plt.savefig("collectDatas/static/collectDatas/img/box_plot.png")
