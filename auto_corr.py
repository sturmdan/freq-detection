# auto_corr

# this file will implement the moving autocorrelation function 

import numpy as np

lenSeg = 441
numDelay = lenSeg + 1
lenWindow = lenSeg + numDelay

numSamplesTotal = 1764

rawVals = np.zeros(lenWindow)
delayCorr_raw = np.zeros([numSamplesTotal, numDelay])
delayCorr = np.zeros([numSamplesTotal, numDelay])
delayMS = np.zeros([numSamplesTotal, numDelay])


def update(newVal):
    curValInd = update.curValInd
    i = update.i
    rawVals[curValInd] = newVal
    
    
    # have new val
    fullSegVal = rawVals[(curValInd - lenSeg) % lenWindow]
    for delay in range(numDelay):   
        delayVal = rawVals[(curValInd - delay) % lenWindow]
        fullSegDelayVal = rawVals[(curValInd - lenSeg - delay) % lenWindow]
        
        if i - delay >= 0:
            newTermCorr = newVal * delayVal
            newTermMag  = delayVal * delayVal
        else: 
            newTermCorr = 0
            newTermMag  = 0
        
        if i - lenSeg - delay >= 0:
            oldTermCorr = fullSegVal  * fullSegDelayVal
            oldTermMag  = fullSegDelayVal * fullSegDelayVal
        else:
            oldTermCorr = 0
            oldTermMag  = 0
            
        if i > 0:
            delayCorr_raw[i][delay] = delayCorr_raw[i - 1][delay] + newTermCorr - oldTermCorr
            delayMS[i][delay] = delayMS[i - 1][delay] + newTermMag - oldTermMag
        else: 
            delayCorr_raw[i][delay] = 0
            delayMS[i][delay] = 0
              
        normTerm = (delayMS[i][delay] * delayMS[i][0])
        if (normTerm != 0):
            delayCorr[i][delay] = (delayCorr_raw[i][delay]**2) / (delayMS[i][delay] * delayMS[i][0])
    
    update.curValInd = (update.curValInd + 1) % lenWindow 
    update.i += 1


def return_data():
    return((delayCorr_raw, delayCorr, delayMS))


def reset():
    update.curValInd = 0
    update.i = 0
    


update.curValInd = 0
update.i = 0