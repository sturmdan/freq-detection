# auto_corr

# this file will implement the moving autocorrelation function 

import numpy as np
from scipy.signal import find_peaks

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

def update_vector(newVal):
    #if newVal != 0:
       #import pdb
       #pdb.set_trace()
    curValInd = update_vector.curValInd
    rawVals[curValInd] = newVal
    oldVal = rawVals[curValInd - lenSeg]
    
    #import pdb
    #pdb.set_trace()
    #print("here")
    
    recentVals = rawVals.take(range(curValInd         , curValInd - numDelay         , -1))
    oldVals    = rawVals.take(range(curValInd - lenSeg, curValInd - numDelay - lenSeg, -1))
    
    #import pdb 
    #pdb.set_trace()
    global delayCorr_raw
    global delayMS
    global delayCorr
    
    delayCorr_raw += newVal * recentVals - oldVal * oldVals
    delayMS += recentVals * recentVals - oldVals * oldVals
    
    delayCorr = (delayCorr_raw * delayCorr_raw) / (delayMS[0] * delayMS)
    delayCorr[np.isnan(delayCorr)] = 0
    
    #maxDelay = np.argmax(delayCorr[delaySkip:]) + delaySkip
    
    peaks = find_peaks(delayCorr[delaySkip:], height = 0.9, distance = 170)[0]
    if peaks.size != 0:
        maxDelay = np.min(peaks)
    else: 
        maxDelay = numDelay - 1
        
    update_vector.curValInd = (update_vector.curValInd + 1) % lenWindow 
    return maxDelay

def return_data():
    return((delayCorr_raw, delayCorr, delayMS))


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
