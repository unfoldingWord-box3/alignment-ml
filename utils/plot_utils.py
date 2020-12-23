import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np

# doing plots
def plotFieldFrequency(frequency, fieldName, xAxisLabel, yAxisLabel = None, max=-1, xNumbers=True, xShowTicks=True, title=None, ylogPlot=False):
    fig = plt.figure()
    if title is None: # use default title
        title = f"Frequency of {xAxisLabel} ('{fieldName}')"
    fig.suptitle(title, fontsize=16)
    if yAxisLabel is None:
        yAxisLabel = "Log of Count" if ylogPlot else "Count"
    ax = fig.add_axes([0,0,1,0.9],
                      yscale="log" if ylogPlot else "linear",
                      xlabel=xAxisLabel,
                      ylabel=yAxisLabel)
    x = list(frequency.index)
    if not xNumbers: # text labels
        labels = x
        x_range = np.arange(len(x))
        ax.set_xticks(x_range)
        ax.set_xticklabels(labels)
        x = x_range
    y = list(frequency.values)
    ax.bar(x,y)
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(formatter)
    if xNumbers:
        if max > -1:
            xticks = np.arange(0, max, 1)
            if max > 10:
                xticks = np.arange(0, max, 2)
            ax.set_xticks(xticks)
    if not xShowTicks:
        plt.setp(ax.get_xticklabels(), visible=False)
        ax.tick_params(axis='x', which='both', length=0)
    plt.show()
