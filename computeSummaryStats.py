import numpy as np

def computeSummaryStats(dist,printEn=False,name=""):
    samples = dist @ 5000
    samplesArr = np.array(samples)
    sumStats = np.percentile(samplesArr, [5, 50, 95]) 
    if printEn:
        print("Summary Statistics: {}".format(name))
        print("5th, 50th, 95th percentiles: {}".format(sumStats))
    return sumStats