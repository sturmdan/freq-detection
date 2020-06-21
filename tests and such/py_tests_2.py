import numpy as np
import time 



length = 1000
rpt = 1000
vec1 = np.zeros(length) + 3
vec2 = np.zeros(length) + 4

startTime = time.time()

for i in range(rpt):
    res1 = np.multiply(vec1, vec2)

print(time.time() - startTime)

startTime = time.time()

for i in range(rpt):
    res2 = np.bitwise_xor(vec1, vec2)

print(time.time() - startTime)