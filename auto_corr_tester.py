import numpy as np
import sounddevice as sd
import math
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import time

#%%
fs = 44100
recLength = 1 # seconds
numSamplesRec = int(fs * recLength)
minFreq = 100 
lenSeg = math.ceil(fs / minFreq) 
lenWindow = 2 * lenSeg
numDelay = lenSeg + 1
numSamplesAnalyze = lenWindow * 2

#%%
numSamples = fs * recLength
times = np.linspace(0, recLength, numSamplesRec)

rec = sd.rec(numSamplesRec, samplerate = fs, channels = 2)
rec = rec[:, 0]

sd.wait()

#%%
plt.figure(3)
plt.plot(times, rec)
plt.xlabel("time")
plt.ylabel("signal value")
plt.title("og recording")

sd.play(rec, fs)
sd.wait()

#%%
startSampleShort = 1000
timesShort = times[startSampleShort : startSampleShort + numSamplesAnalyze]
signal = rec[startSampleShort : startSampleShort + numSamplesAnalyze]

sd.play(signal, fs)
sd.wait()

plt.figure(3)
plt.plot(timesShort, signal)
plt.xlabel("time")
plt.ylabel("signal value")
plt.title("shortened recording")

#%%
dummyData = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2])
lenSeg = 3
numDelay = lenSeg + 1
lenWindow = lenSeg * 2
numSamplesTotal = dummyData.size
rec = dummyData

#%%
import auto_corr
auto_corr.reset()
startTime = time.time()
for i in range(signal.size):
    newVal = signal[i]
    auto_corr.update(newVal)
    
print(time.time() - startTime)
    
#%%
(delayCorr_raw, delayCorr, delayMS) = auto_corr.return_data()

#%%
ax = sns.heatmap(delayCorr )
