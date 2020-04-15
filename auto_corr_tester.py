import numpy as np
import sounddevice as sd
import math
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import time
import auto_corr

#%%
fs = 44100
recLength = 1 # seconds
numSamplesRec = int(fs * recLength)
minFreq = 100 
lenSeg = math.ceil(fs / minFreq) 
lenWindow = 2 * lenSeg
numDelay = lenSeg + 1
numSamplesAnalyze = lenWindow * 2
numSamplesAnalyze = 4410

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
startSampleShort = 0
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
signal = dummyData

#%%
auto_corr.reset()
startTime = time.time()
for i in range(signal.size):
    newVal = signal[i]
    auto_corr.update_vector(newVal)
    
print(time.time() - startTime)
    
#%%
(delayCorr_raw, delayCorr, delayMS, maxDelay) = auto_corr.return_data()
#delayCorr[np.isnan(delayCorr)] = 0

firstSamples = 1000
plt.plot(maxDelay[0:firstSamples])

#%%
ax = sns.heatmap(delayCorr)

#%%
delay = 215
freq = fs / delay
sampleTone = np.sin(2 * math.pi * freq * times)

sd.play(sampleTone, fs)

#%%
# test how long things run 
vec = np.ones([100000, 1])
startTime = time.time()

for i in range(10000):
    #result = vec + vec
    #result = np.add(vec, vec)
    
    #result = vec * vec
    #result = np.multiply(vec, vec)
    
    result = vec / vec
    #result = np.divide(vec, vec)
    
print(time.time() - startTime)





