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
    
    #import pdb
    #pdb.set_trace()
    
    
    # have new val
    fullSegVal = rawVals[(curValInd - lenSeg)]
    for delay in range(numDelay):   
        delayVal = rawVals[(curValInd - delay)]
        fullSegDelayVal = rawVals[(curValInd - lenSeg - delay)]
        
        newTermCorr = newVal * delayVal
        newTermMag  = delayVal * delayVal

        oldTermCorr = fullSegVal  * fullSegDelayVal
        oldTermMag  = fullSegDelayVal * fullSegDelayVal
            
        if i > -1:
            delayCorr_raw[i][delay] = delayCorr_raw[i - 1][delay] + newTermCorr - oldTermCorr
            delayMS[i][delay] = delayMS[i - 1][delay] + newTermMag - oldTermMag
              
        normTerm = (delayMS[i][delay] * delayMS[i][0])
        if (normTerm != 0):
            delayCorr[i][delay] = (delayCorr_raw[i][delay]**2) / (delayMS[i][delay] * delayMS[i][0])
    
    update.curValInd = (update.curValInd + 1) % lenWindow 
    update.i += 1
    
    
def update_vector(newVal):
    curValInd = update_vector.curValInd
    i = update_vector.i
    rawVals[curValInd] = newVal
    oldVal = rawVals[curValInd - lenSeg]
    
    #import pdb
    #pdb.set_trace()
    
    recentVals = rawVals.take(range(curValInd, curValInd - numDelay, -1))
    oldVals    = rawVals.take(range(curValInd - lenSeg, curValInd - lenSeg - numDelay, -1))
    
    #import pdb 
    #pdb.set_trace()
    delayCorr_raw[i][:] = delayCorr_raw[i-1][:] + newVal * recentVals - oldVal * oldVals
    delayMS[i][:] = delayMS[i-1][:] + recentVals * recentVals - oldVals * oldVals
    
    delayCorr[i][:] = (delayCorr_raw[i][:] * delayCorr_raw[i][:]) / (delayMS[i][0] * delayMS[i][:])
    
    update_vector.curValInd = (update_vector.curValInd + 1) % lenWindow 
    update_vector.i += 1
    


def return_data():
    return((delayCorr_raw, delayCorr, delayMS))


def reset():
    update.curValInd = 0
    update.i = 0
    
    update_vector.curValInd = 0
    update_vector.i = 0
    
    global rawVals
    global delayCorr_raw
    global delayCorr
    global delayMS 
    
    rawVals = np.zeros(lenWindow)
    delayCorr_raw = np.zeros([numSamplesTotal, numDelay])
    delayCorr = np.zeros([numSamplesTotal, numDelay])
    delayMS = np.zeros([numSamplesTotal, numDelay])
    
        

update.curValInd = 0
update.i = 0

update_vector.curValInd = 0
update_vector.i = 0