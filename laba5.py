# Вариант 18

# Задана рекуррентная функция. Область определения функции – натуральные числа. Написать программу сравнительного вычисления данной функции рекурсивно и итерационно.
# Определить границы применимости рекурсивного и итерационного подхода. Результаты сравнительного исследования времени вычисления представить в табличной и графической форме.

# F(0) = 1, F(1) = 1, F(n) = (-1)^n * (F(n–1) /(2n)!*F(n-2)+1), при n > 1

import timeit
import matplotlib.pyplot as plt

"""
Кэш для хранения вычисленных значений факториалов
"""
factorial_cache = {0: 1, 1: 1}

"""
Динамическая функция для вычисления факториала
"""
def dynamic_factorial(n):
    if n in factorial_cache:
        return factorial_cache[n]

    # Вычисляем факториалы последовательно до n и сохраняем их в кэше
    for i in range(2, n + 1):
        factorial_cache[i] = factorial_cache[i - 1] * i

    return factorial_cache[n]

"""
Рекурсивная функция для вычисления факториала
"""
def recursive_factorial(n):
    if n == 0:
        return 1
    else:
        return n * recursive_factorial(n-1)

"""
Итеративная функция для вычисления факториала
"""
def iterative_factorial(n):
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

"""
Динамическая функция для вычисления F(n)
"""
k=1
def dynamic_F(n, cache={0: 1, 1: 1}):
    if n in cache:
        return cache[n]
    else:
        """
        Здесь используем dynamic_factorial для вычисления факториалов
        """
        k *= -1
        result = k * (dynamic_F(n-1, cache) / (dynamic_factorial(2*n)) * dynamic_F(n-2, cache) + 1)
        #F(0) = 1, F(1) = 1, F(n) = (-1) ^ n * (F(n–1) / (2n)!*F(n - 2) + 1), при n > 1
        cache[n] = result
        return result

"""
Функция для измерения времени выполнения
"""
def score_time(func, n):
    return timeit.timeit(lambda: func(n), number=1000)

"""
Значения n для которых мы хотим измерить время выполнения
"""
n_values = range(1, 10)
recursive_times = []
iterative_times = []
dynamic_times = []

"""
Измерение времени выполнения для каждого значения n
"""
for n in n_values:
    recursive_times.append(score_time(recursive_factorial, n))
    iterative_times.append(score_time(iterative_factorial, n))
    dynamic_times.append(score_time(lambda n=n: dynamic_F(n), n))

"""
Вывод результатов в табличной форме
"""
print(f"{'n':<10}{'Рекурсивное время (мс)':<25}{'Итерационное время (мс)':<25}{'Динамическое время (мс)':<25}")
for i, n in enumerate(n_values):
    print(f"{n:<10}{recursive_times[i]:<25}{iterative_times[i]:<25}{dynamic_times[i]:<25}")

"""
Построение и вывод графика результатов
"""
colors = ['red', 'green', 'blue']
markers = ['o', 's', 'D']
"""
Рисуем графики
"""
plt.figure(figsize=(8, 6))
for i, (times, label) in enumerate(zip([recursive_times, iterative_times, dynamic_times], ['Рекурсивно', 'Итерационно', 'Динамическое'])):
    plt.plot(n_values, times, label=label, color=colors[i], marker=markers[i])
"""
Добавляем сетку и легенду
"""
plt.grid(True)
plt.legend()
"""
Задаем заголовок и метки осей
"""
plt.title('Сравнение времени вычисления функции F(n)', fontsize=14)
plt.xlabel('n', fontsize=12)
plt.ylabel('Время (в миллисекундах)', fontsize=12)
"""
Изменяем размер шрифта на осях
"""
plt.tick_params(axis='both', which='major', labelsize=10)
"""
Показываем график
"""
plt.show()