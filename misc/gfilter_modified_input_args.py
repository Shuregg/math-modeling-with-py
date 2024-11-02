import numpy as np
import matplotlib.pyplot as plt
import argparse

# Константы и параметры
TSW = 7
order = 32
scale = 2 ** order

# Функция для создания фильтра CIC4
def create_cic4(tsw):
    cic1 = np.ones(2 ** tsw)
    cic2 = np.convolve(cic1, cic1)
    cic4 = np.convolve(cic2, cic2)
    return cic4 / np.sum(cic4)

# Функция для применения фильтра к входному сигналу
def apply_gaussian_filter(signal, cic4, scale):
    scaled_signal = np.floor(np.array(signal) / scale)
    smoothed_signal = np.convolve(cic4, signal)
    smoothed_scaled_signal = np.convolve(cic4, scaled_signal) * scale
    return smoothed_signal, smoothed_scaled_signal

# Основная функция
def main(input_signal):
    # Преобразование строки чисел в список целых чисел
    signal = list(map(int, input_signal.split(',')))

    # Создаем фильтр
    cic4 = create_cic4(TSW)

    # Применяем фильтр к входному сигналу
    pf, pfm = apply_gaussian_filter(signal, cic4, scale)

    # Визуализация
    plt.figure()
    plt.plot(signal, label="Исходный сигнал")
    plt.plot(pf, label="Сглаженный сигнал (pf)")
    plt.plot(pfm, label="Сглаженный масштабированный сигнал (pfm)")
    plt.legend()
    plt.grid()
    plt.show()

# Парсинг аргументов командной строки
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gaussian filter for smoothing step-like input signals.")
    parser.add_argument("input_signal", type=str, help="Comma-separated list of input signal values")
    args = parser.parse_args()

    main(args.input_signal)
