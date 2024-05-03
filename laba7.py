"""
Лабораторная работа №7 с графическим интерфейсом по заданию из ЛР №6:
Задание состоит из двух частей.
1 часть – написать программу в соответствии со своим вариантом задания. Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.
2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно ограничение на характеристики объектов (которое будет сокращать количество переборов)  и целевую функцию для нахождения оптимального  решения.
Вариант 18. Вывести все натуральные числа до n, в записи которых встречается ровно одна нечетная цифра на четной позиции.
"""
import tkinter as tk
from tkinter import scrolledtext
import timeit
import itertools

# Проверка условия для одной нечетной цифры на четной позиции
def is_valid_alg(number):
    number_str = str(number)
    return sum(1 for i, d in enumerate(number_str, start=1) if i % 2 == 0 and int(d) % 2 == 1) == 1

# Алгоритмический подход
def algorithmic_approach(n):
    result = []
    for number in range(n):
        if is_valid_alg(number):
            result.append(number)
    return result

# Функциональный подход с использованием itertools
def functional_approach_itertools(n):
    result = []
    for digits in itertools.product('0123456789', repeat=len(str(n - 1))):
        number = int(''.join(digits))
        if number < n and is_valid_alg(number):
            result.append(number)
    return result

# Усложненный алгоритмический подход с дополнительным условием кратности 5
def complex_algorithmic_approach(n):
    result = []
    for number in range(0, n, 5):  # Перебор с шагом 5
        if is_valid_alg(number):
            result.append(number)
    return result

# Усложненный функциональный подход с использованием itertools и условием кратности 5
def complex_functional_approach_itertools(n):
    result = []
    for digits in itertools.product('0123456789', repeat=len(str(n - 1))):
        number = int(''.join(digits))
        if number < n and number % 5 == 0 and is_valid_alg(number):
            result.append(number)
    return result

# Функция, вызываемая при нажатии кнопки
def on_run_clicked():
    n = int(entry_n.get())
    start_time = timeit.default_timer()

    if var.get() == 1:
        result = algorithmic_approach(n)
    elif var.get() == 2:
        result = functional_approach_itertools(n)
    elif var.get() == 3:
        result = complex_algorithmic_approach(n)
    else:  # var.get() == 4
        result = complex_functional_approach_itertools(n)

    elapsed = timeit.default_timer() - start_time
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.INSERT, f"Результаты: {result}\n")
    text_area.insert(tk.INSERT, f"Время выполнения: {elapsed:.6f} секунд")



root = tk.Tk()
root.title("Поиск чисел")
root.geometry("800x1000")  # Изменяем размеры окна

# Метка для поля ввода
label = tk.Label(root, text="Введите число n:", font=("Helvetica", 12))
label.pack(pady=10)

# Поле ввода
entry_n = tk.Entry(root, font=("Helvetica", 12))
entry_n.pack(pady=5)

# Радиокнопки для выбора метода
var = tk.IntVar()
var.set(1)
radio_alg = tk.Radiobutton(root, text="Алгоритмический подход", variable=var, value=1, font=("Helvetica", 10))
radio_alg.pack(anchor=tk.W)
radio_func = tk.Radiobutton(root, text="Функциональный подход (itertools)", variable=var, value=2, font=("Helvetica", 10))
radio_func.pack(anchor=tk.W)
radio_complex_alg = tk.Radiobutton(root, text="Усложненный алгоритмический подход", variable=var, value=3, font=("Helvetica", 10))
radio_complex_alg.pack(anchor=tk.W)
radio_complex_func = tk.Radiobutton(root, text="Усложненный функциональный подход (itertools)", variable=var, value=4, font=("Helvetica", 10))
radio_complex_func.pack(anchor=tk.W)

# Кнопка выполнения
run_button = tk.Button(root, text="Найти числа", command=on_run_clicked, font=("Helvetica", 12), bg="#4CAF50", fg="white", relief=tk.RAISED)
run_button.pack(pady=10)

# Текстовое поле с прокруткой для вывода результатов
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10, font=("Helvetica", 10))
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Запуск основного цикла Tkinter
root.mainloop()