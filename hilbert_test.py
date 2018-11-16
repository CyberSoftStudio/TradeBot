import numpy as np
from scipy.fftpack import fft, ifft
import math
import matplotlib.pyplot as plt
from scipy.signal import chirp, hilbert

# math.pi = 3
print(math.pi)
# math.cos = lambda x : x + 2
print(math.cos(2))

x = np.linspace(0, 10 * math.pi, 100)
signal = chirp(x, 20.0, x[-1], 100.0)
signal *= (1.0 + 0.5 * np.sin(2.0*np.pi*3.0*x) )
# signal = 2 * np.sin(0.5* x) + np.cos(2 * x) + np.cos(3 * x)

plt.figure()
plt.plot(x, signal)

fftsig = fft(signal)

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(x, np.abs(fftsig))
ax2.plot(x, np.angle(fftsig))
# plt.show()

hilbertsig = -1j * fftsig
# hilbertsig[0] = 0

recsignal = np.imag(ifft(hilbertsig))

scipyhilb = hilbert(signal)

plt.figure()
plt.plot(signal)
plt.plot(np.abs(recsignal))
plt.show()

print(np.imag(recsignal) - np.imag(hilbertsig))