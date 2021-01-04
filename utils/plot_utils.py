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

def plotFrequencies(frequenciesOfAlignments, title='', ylabel='', showXValues=False, xlimit=None, ylimit=None):
    plt.figure()
    outputTable = []
    for origWord in frequenciesOfAlignments.keys():
        frequency_ = frequenciesOfAlignments[origWord]
        frequencyValues_ = list(frequency_.values)
        total = 0
        for value in frequencyValues_:
            total += value
        # print(f"for {origWord} total is {total}")
        if showXValues:
            x = list(frequency_.index)
        else:
            x = range(len(frequencyValues_))
        y = frequencyValues_ / total * 100 # scale to percent
        plt.plot(x,y)

        data = {}
        for i in range(len(x)):
            x_ = str(x[i])
            y_ = y[i]
            data[x_] = y_
        outputTable.append(data)

    if xlimit:
        plt.xlim(xlimit)
    plt.ylabel(ylabel)

    if ylimit:
        plt.ylim(ylimit)
    else:
        plt.ylim([0,50])

    plt.suptitle(title, fontsize=16)

    plt.show()
    return outputTable

def plotXYdataDict(dataDict, title='', ylabel='', xlabel='', showXValues=False, xlimit=None, ylimit=None):
    plt.figure()
    for origWord in dataDict.keys():
        data = dataDict[origWord]
        total = 0
        Y = data['Y']
        normalizedY = []
        for value in Y: # get total
            total += value
        # print(f"total = {total}")
        for value in Y: # get percent
            normalizedY.append(value / total * 100) # scale to percent
        plt.plot(data['X'], normalizedY)
        if len(data) > 6:
            print(f"for {origWord} original data: {dataDict[origWord]}")
            print(f"normalized data: {data}")

    if ylimit:
        plt.ylim(ylimit)
    else:
        plt.ylim([0,105])

    if xlimit:
        plt.xlim(xlimit)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.suptitle(title, fontsize=16)

    plt.show()

