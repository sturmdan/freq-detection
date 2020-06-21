import numpy as np
import sounddevice as sd
import math
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import time
import auto_corr
import auto_corr_no_mem
from scipy.signal import find_peaks


#%%
fs = 44100
recLength = 1 # seconds
numSamplesRec = int(fs * recLength)
minFreq = 100 
lenSeg = math.ceil(fs / minFreq) 
lenWindow = 2 * lenSeg
numDelay = lenSeg + 1
numSamplesAnalyze = lenWindow * 2
numSamplesAnalyze = 44100

sampleAudioFreq = 440
sampleAudio = np.sin(2 * math.pi * sampleAudioFreq * np.arange(0, numSamplesAnalyze / fs, 1 / fs))

#%% record audio
numSamples = fs * recLength
times = np.linspace(0, recLength, numSamplesRec)

rec = sd.rec(numSamplesRec, samplerate = fs, channels = 2)
rec = rec[:, 0]


sd.wait()

#%% plot and play audio
plt.figure(3)
plt.plot(times, rec)
plt.xlabel("time")
plt.ylabel("signal value")
plt.title("og recording")

sd.play(rec, fs)
sd.wait()

#%% shorten audio
startSampleShort = 0
timesShort = times[startSampleShort : startSampleShort + numSamplesAnalyze]
signal = rec[startSampleShort : startSampleShort + numSamplesAnalyze]
#signal = sampleAudio

sd.play(signal, fs)
sd.wait()

plt.figure(3)
plt.plot(timesShort, signal)
plt.xlabel("time")
plt.ylabel("signal value")
plt.title("shortened recording")

#%% run autocorrelation
auto_corr.reset()
startTime = time.time()
for i in range(signal.size):
    newVal = signal[i]
    auto_corr.update_vector(newVal)
    
print(time.time() - startTime)
    
#%% return data
(delayCorr_raw, delayCorr, delayMS, maxDelay_2) = auto_corr.return_data()
#delayCorr[np.isnan(delayCorr)] = 0

firstSamples = 44100
plt.plot(maxDelay_2[0:firstSamples])

#%%
iteration = 40000
delayStartIndex = 45

relCorr = delayCorr[iteration, delayStartIndex:]
maxCorr = np.max(relCorr)
corrPeaks = find_peaks(relCorr, distance = 50)[0] 
indexFirstPeak = np.argmax(relCorr[corrPeaks] > 0.95 * maxCorr)
maxDelay = corrPeaks[indexFirstPeak] + delayStartIndex


#%% print heatmap of correlation
ax = sns.heatmap(delayCorr)

#%% run memoryless autocorrelation
auto_corr_no_mem.reset()
maxDelay = np.zeros(signal.size)
startTime = time.time()

numSamples = signal.size
for i in range(numSamples):
    if 0:
        if i == 900:
            import pdb
            pdb.set_trace()
            
    newVal = signal[i]
    maxDelay[i] = auto_corr_no_mem.update_vector(newVal)
    
    if 0:
        if (maxDelay[i] > 300 and i > 10000):
            import pdb 
            pdb.set_trace()
    
print(time.time() - startTime)
auto_corr_no_mem.print_time()

#%%
fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.plot(signal, color = color)
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.plot(maxDelay, color = color)

plt.show()
#plt.plot(maxDelay[0:44100])

#%% test a tone 
delay = 90
freq = fs / delay
sampleTone = np.sin(2 * math.pi * freq * times)

sd.play(sampleTone, fs)

#%% basic reconstruction

samplesPerTone = 100 
finalAudio = np.zeros(signal.size)
toneTime = np.linspace(0, samplesPerTone / fs, samplesPerTone)
allFreqs = np.zeros(math.ceil(signal.size / samplesPerTone))
endingPhase = 0 
#import pdb 
#pdb.set_trace()

for i in range(0, signal.size, samplesPerTone):
    #print(i)
    #print(math.floor(i / samplesPerTone))
    freq = fs / maxDelay[i]
    allFreqs[math.floor(i / samplesPerTone)] = freq
    sinWave = np.cos(2 * math.pi * (freq * toneTime + endingPhase))
    endingPhase += (freq * (samplesPerTone + 1) / fs) % 1

    if (i + samplesPerTone > finalAudio.size):
        finalAudio[i:finalAudio.size] = sinWave[finalAudio.size - i]
    else:
        finalAudio[i:i+samplesPerTone] = sinWave
    
sizeRamp = 10000
rampStart = np.linspace(0, 1, sizeRamp)
rampEnd   = np.linspace(1, 0, sizeRamp)
finalAudio[:sizeRamp] = finalAudio[:sizeRamp] * rampStart
finalAudio[-sizeRamp:] = finalAudio[-sizeRamp:] * rampEnd

x = 44100
plt.plot(finalAudio[0 : x])
    
#%%
sd.play(finalAudio)
sd.wait()


#%%
startTime = time.time()
sd.play(signal)
print(time.time() - startTime)
    
    
    
    
    


