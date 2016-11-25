# This script will import .csv counter log files, perform statistics, and generate a plot.
# Plot structure is histogram with an overlaid normal distribution.


import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from pylab import savefig as sf
import numpy as np
import os
import sys
from datetime import datetime


def main():
    printHeader()

    #logFilePath = os.getcwd()
    #logFile = os.path.join(logFilePath, "counterLog.{}.{:03d}.csv".format(timeStamp, ind))
    #logFile = "counterLog.test.csv"
    # logFile = "counterLog.20161112.003-60hrs-realMeas.csv"

    logFile = str(sys.argv[1])


    datArray = readIntoArray(logFile)

    buildPlot(datArray)

    showPlot(logFile)


def printHeader():
    print("---------------------------------")
    print("      Counter Data Plotter")
    print("     " + str(datetime.now())[:-3])
    print("---------------------------------")


def readIntoArray(log):

    datArray = np.genfromtxt(log, delimiter=",", skiprows=1, usecols=1)

    return datArray


def buildPlot(dat):

    # first, shift all data by 10e6 to preserve 8 decimal places
    datCenter = dat - 10000000

    datMean = np.mean(datCenter)
    datMedian = np.median(dat)
    datStd = np.std(datCenter)
    # datVar = np.var(dat)
    countBins = 100

    datShift = datCenter - datMean
    datShiftAxis = np.linspace(min(datShift), max(datShift), countBins)

    fig = plt.figure()
    subPlot = fig.add_subplot(1,1,1)

    subPlot.hist(datShift, countBins, normed=True, facecolor="g", alpha=0.75)
    subPlot.plot(datShiftAxis, mlab.normpdf(datShiftAxis, 0, datStd), "r--", linewidth=2, alpha=0.75)

    plt.xlabel("Standard Deviations [Hz]")
    plt.ylabel("Readings")
    plt.title("10MHz Reference - 12Nov2016 + 60hrs")

    x_ticks = np.arange(-4*datStd, 4*datStd, datStd).round(3)
    # x_labels = [r"${} \sigma$".format(i) for i in range(-4, 5)]
    subPlot.set_xticks(x_ticks)
    # subPlot.set_xticklabels(x_labels)

    plt.grid(True, color="b", linewidth=2, alpha=0.5)
    plt.xlim(-4*datStd, 4*datStd)
    # for x in np.arange(-3*datStd, 4*datStd, datStd):
    #     plt.axvline(x)

    # text box with statistics
    textStr = "$\mu$={:.3f}\n$\sigma$={:.4f}".format(datMean, datStd)
    textStyle = dict(boxstyle="round", facecolor="wheat", alpha=0.75)
    subPlot.text(-.024, 42, textStr, fontsize=20, bbox=textStyle)


def showPlot(logFile):
    sf(logFile[:-3] + "png", bbox_inches="tight")
    plt.show()


if __name__ == '__main__':
    main()