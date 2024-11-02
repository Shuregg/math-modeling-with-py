import numpy as np
import matplotlib.pyplot as plt

# Константы и параметры
TSW = 7
order = 32
a = 28621495321396
b = 29171251135283
scale = 2 ** order

# Создание фильтра CIC4
cic1 = np.ones(2 ** TSW)
cic2 = np.convolve(cic1, cic1)
cic4 = np.convolve(cic2, cic2)
cic4 = cic4 / np.sum(cic4)

# Формирование сигнала
p = np.concatenate((a * np.ones(1000), b * np.ones(1000)))

# Масштабированный сигнал
am = a // scale
bm = b // scale
pm = np.concatenate((am * np.ones(1000), bm * np.ones(1000)))

# Применение фильтра CIC4 к сигналу
pf = np.convolve(cic4, p)
pfm = np.convolve(cic4, pm) * scale

# Визуализация результатов
plt.figure()
plt.plot(p, label="Исходный сигнал")
plt.plot(pf, label="Сглаженный сигнал (pf)")
plt.plot(pfm, label="Сглаженный масштабированный сигнал (pfm)")
plt.legend()
plt.grid()
plt.show()
