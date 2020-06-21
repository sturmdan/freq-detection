# auto_corr

# this file will implement the moving autocorrelation function 

import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import time

lenSeg = 441
numDelay = lenSeg + 1
lenWindow = lenSeg + numDelay

delaySkip = 45

rawVals = np.zeros(lenWindow)
delayCorr_raw = np.zeros(numDelay)
delayCorr = np.zeros(numDelay)
delayMS = np.zeros(numDelay)

# one question here - should delayCorr_raw, delayMS, and delayCorr be global 
# or belong to the function? 
# in the actual c implementation, should they be global or be static variables
# belonging to the function? 
time0 = 0
time1 = 0
time2 = 0
time3 = 0

def update_vector(newVal):
    global time1
    global time2
    global time3
    global time0
    startTime = time.time()
    #if newVal != 0:
       #import pdb
       #pdb.set_trace()
    curValInd = update_vector.curValInd
    rawVals[curValInd] = newVal
    oldVal = rawVals[curValInd - lenSeg]
    
    time0 += time.time() - startTime
    
    #import pdb
    #pdb.set_trace()
    #print("here")
    
    recentVals = rawVals.take(range(curValInd         , curValInd - numDelay         , -1))
    oldVals    = rawVals.take(range(curValInd - lenSeg, curValInd - numDelay - lenSeg, -1))
    
    time1 += time.time() - startTime
    
    #import pdb 
    #pdb.set_trace()
    global delayCorr_raw
    global delayMS
    global delayCorr
    
    delayCorr_raw += newVal * recentVals - oldVal * oldVals
    delayMS += recentVals * recentVals - oldVals * oldVals
    
    #delayCorr = (delayCorr_raw * delayCorr_raw * np.sign(delayCorr_raw)) / (delayMS[0] * delayMS)
    delayCorr = delayCorr_raw / (np.sqrt(delayMS[0] * delayMS))
    delayCorr[np.isnan(delayCorr)] = 0
    
    time2 += time.time() - startTime
    
    #maxDelay = np.argmax(delayCorr[delaySkip:]) + delaySkip
    delaySkip = 45
    relCorr = delayCorr[delaySkip:]
    maxCorr = np.max(relCorr)
    corrPeaks = find_peaks(relCorr, distance = 50)[0] 
    if corrPeaks.size != 0:
        indexFirstPeak = np.argmax(relCorr[corrPeaks] > 0.8 * maxCorr)
        maxDelay = corrPeaks[indexFirstPeak] + delaySkip
    else:
        maxDelay = numDelay - 1
    
    
    
    '''
    peaks = find_peaks(delayCorr[delaySkip:], distance = 170)[0] + delaySkip
    if peaks.size != 0:
        maxDelay = np.min(peaks)
    else: 
        maxDelay = numDelay - 1
    '''
        
    update_vector.curValInd = (update_vector.curValInd + 1) % lenWindow 
    time3 += time.time() - startTime
    return maxDelay

def return_data():
    return((delayCorr_raw, delayCorr, delayMS))


def print_time():
    print(time0)
    print(time1 - time0)
    print(time2 - time1)
    print(time3 - time2)


def reset():    
    update_vector.curValInd = 0
    
    global rawVals
    global delayCorr_raw
    global delayCorr
    global delayMS 
    
    rawVals = np.zeros(lenWindow)
    delayCorr_raw = np.zeros(numDelay)
    delayCorr = np.zeros(numDelay)
    delayMS = np.zeros(numDelay)


update_vector.curValInd = 0
