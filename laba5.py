# Вариант 18

# Задана рекуррентная функция. Область определения функции – натуральные числа. Написать программу сравнительного вычисления данной функции рекурсивно и итерационно.
# Определить границы применимости рекурсивного и итерационного подхода. Результаты сравнительного исследования времени вычисления представить в табличной и графической форме.

# F(0) = 1, F(1) = 1, F(n) = (-1)^n * (F(n–1) /(2n)!*F(n-2)+1), при n > 1

import numpy as np
import matplotlib.pyplot as plt
import time

# Кэш для факториалов
factorial_cache = {0: 1, 1: 1}

# Рекурсивное вычисление функции
def recursive_F(n):
    if n == 0 or n == 1:
        return 1
    else:
        return ((-1)**n) * (recursive_F(n-1) / (factorial(n)) * recursive_F(n-2) + 1)

# Итерационное вычисление функции
def iterative_F(n):
    if n == 0 or n == 1:
        return 1
    else:
        F_n_minus_1 = 1
        F_n_minus_2 = 1
        F_n = 0
        for i in range(2, n+1):
            F_n = ((-1)**i) * (F_n_minus_1 / (factorial(i)) * F_n_minus_2 + 1)
            F_n_minus_2 = F_n_minus_1
            F_n_minus_1 = F_n
        return F_n

# Эффективное вычисление факториала
def factorial_efficient(n):
    result = 1
    for i in range(2, n+1, 2):
        result *= i
    return result

# Рекурсивное вычисление факториала
def factorial_recursive(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial_recursive(n - 1)

# Функция для вычисления факториала
def factorial(n, efficient=True):
    if efficient:
        return factorial_efficient(n)
    else:
        return factorial_recursive(n)

# Функция для замера времени выполнения
def measure_time(func, n):
    start_time = time.time()
    func(n)
    end_time = time.time()
    return end_time - start_time

# Сравнение времени выполнения для рекурсивной, итерационной и эффективной функций
def compare_execution_time(n):
    recursive_time = measure_time(recursive_F, n)
    iterative_time = measure_time(iterative_F, n)
    efficient_time = measure_time(lambda n: factorial(n), n)  # Исправлено здесь
    return recursive_time, iterative_time, efficient_time

# Функция для построения графика времени выполнения
def plot_execution_time(n_values):
    recursive_times = []
    iterative_times = []
    efficient_times = []
    for n in n_values:
        recursive_time, iterative_time, efficient_time = compare_execution_time(n)
        recursive_times.append(recursive_time)
        iterative_times.append(iterative_time)
        efficient_times.append(efficient_time)

    print(f"{'n':<10}{'Рекурсивное время (мс)':<25}{'Итерационное время (мс)':<25}{'Эффективное время (мс)':<25}")
    for i, n in enumerate(n_values):
        print(f"{n:<10}{recursive_times[i]:<25}{iterative_times[i]:<25}{efficient_times[i]:<25}")


    plt.plot(n_values, recursive_times, label="Рекурсивное время")
    plt.plot(n_values, iterative_times, label="Итерационное время")
    plt.plot(n_values, efficient_times, label="Эффективное время")
    plt.xlabel('Значение n')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Сравнение времени выполнения различных методов')
    plt.xticks(n_values)  # Устанавливаем значения n на оси X
    plt.legend()
    plt.show()

# Зададим значения n для исследования (целые числа)
n_values = np.arange(1, 21, dtype=int)  # Пример значений от 1 до 20

# Построим график
plot_execution_time(n_values)
