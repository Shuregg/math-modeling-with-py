import numpy as np
import matplotlib.pyplot as plt

# Params
TSW = 7
order = 32
scale = 2 ** order

# CIC func
def cic(tsw):
    cic1 = np.ones(2 ** tsw)
    cic2 = np.convolve(cic1, cic1)
    cic4 = np.convolve(cic2, cic2)
    return cic4 / np.sum(cic4)

# Gaussian filter func
def gaussian_filter(signal, cic4, scale):
    scaled_signal = np.floor(np.array(signal) / scale)
    smoothed_signal = np.convolve(cic4, signal)
    smoothed_scaled_signal = np.convolve(cic4, scaled_signal) * scale
    return smoothed_signal, smoothed_scaled_signal

input_signal = [28621495321396] * 500 + [28000000000000] * 2000 + [29171251135283] * 1000 + [28000000000000] * 1000
print(input_signal)

cic4 = cic(TSW)

pf, pfm = gaussian_filter(input_signal, cic4, scale)

plt.figure()
plt.plot(input_signal, label="Input signal")
plt.plot(pf, label="Smoothed output signal")
plt.plot(pfm, label="Smoothed scaled output signal")
plt.legend()
plt.grid()
plt.show()
