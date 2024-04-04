# Вариант 18

# Задана рекуррентная функция. Область определения функции – натуральные числа. Написать программу сравнительного вычисления данной функции рекурсивно и итерационно.
# Определить границы применимости рекурсивного и итерационного подхода. Результаты сравнительного исследования времени вычисления представить в табличной и графической форме.

# F(0) = 1, F(1) = 1, F(n) = (-1)^n * (F(n–1) /(2n)!*F(n-2)+1), при n > 1

import numpy as np
import matplotlib.pyplot as plt
import time

# Рекурсивное вычисление функции
def recursive_F(n):
    if n == 0 or n == 1:
        return 1
    else:
        return ((-1)**n) * (recursive_F(n-1) / (2*n) * recursive_F(n-2) + 1)

# Итерационное вычисление функции
def iterative_F(n):
    if n == 0 or n == 1:
        return 1
    else:
        F_n_minus_1 = 1
        F_n_minus_2 = 1
        F_n = 0
        for i in range(2, n+1):
            F_n = ((-1)**i) * (F_n_minus_1 / (2*i) * F_n_minus_2 + 1)
            F_n_minus_2 = F_n_minus_1
            F_n_minus_1 = F_n
        return F_n

# Функция для замера времени выполнения
def measure_time(func, n):
    start_time = time.time()
    func(n)
    end_time = time.time()
    return end_time - start_time

# Сравнение времени выполнения для рекурсивной и итерационной функций
def compare_execution_time(n):
    recursive_time = measure_time(recursive_F, n)
    iterative_time = measure_time(iterative_F, n)
    return recursive_time, iterative_time

# Функция для построения графика времени выполнения
def plot_execution_time(n_values):
    recursive_times = []
    iterative_times = []
    for n in n_values:
        recursive_time, iterative_time = compare_execution_time(n)
        recursive_times.append(recursive_time)
        iterative_times.append(iterative_time)

    plt.plot(n_values, recursive_times, label="Рекурсивное время")
    plt.plot(n_values, iterative_times, label="Итерационное время")
    plt.xlabel('Значение n')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Сравнение времени выполнения рекурсивного и итерационного методов')
    plt.legend()
    plt.show()

# Зададим значения n для исследования
n_values = np.arange(1, 21)  # Пример значений от 1 до 20

# Построим график
plot_execution_time(n_values)