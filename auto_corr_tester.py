import numpy as np
import sounddevice as sd
import math
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import time
import auto_corr
import auto_corr_no_mem

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

sampleAudioFreq = 110
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

#%% print heatmap of correlation
ax = sns.heatmap(delayCorr)

#%% run memoryless autocorrelation
auto_corr_no_mem.reset()
maxDelay = np.zeros(signal.size)
startTime = time.time()
for i in range(signal.size):
    #if i == 40300:
     #   import pdb
      #  pdb.set_trace()
    newVal = signal[i]
    maxDelay[i] = auto_corr_no_mem.update_vector(newVal)
    
print(time.time() - startTime)

plt.plot(maxDelay[0:44100])

#%% test a tone 
delay = 220
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
    
    
    
    
    


