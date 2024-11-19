import tkinter as tk
from tkinter import messagebox
import time
import random
import os
import json  # Используем JSON для хранения данных
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

button_color = "#2c786a"
button_active_color = "#7eb8ae"
button_active_text_color = "#7eb8ae"
button_disabled_text_color = "#7eb8ae"
font_big = ("Arial", 24, "bold")
font_small = ("Arial", 16)

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Проверка скорости печати")
        self.style = ttk.Style("cosmo")

        # Проверяем и создаем stats.txt, если его нет
        self.initialize_stats_file()

        # Метка над текстом
        self.text_label = tk.Label(root, text="Текст", font=font_big, anchor="w")
        self.text_label.pack(pady=(10, 5))

        # Поле для отображения текста
        self.text_display = tk.Text(root, height=5, width=60, font=font_small, wrap="word")
        self.text_display.pack(pady=(0, 5))
        self.text_display.insert("1.0", self.get_random_text("text.txt"))  # Вставляем текст
        self.text_display.configure(state="disabled")  # Запрещаем редактирование

        # Метка над полем ввода
        self.input_label = tk.Label(root, text="Ввод", font=font_big, anchor="w")
        self.input_label.pack(pady=(5, 5))

        # Поле ввода
        self.text_entry = tk.Entry(root, font=font_small, fg="black", justify="left")
        self.text_entry.pack(pady=(0, 10))
        self.text_entry.bind('<space>', self.check_word)  # Пробел переключает на следующее слово
        self.text_entry.bind('<KeyRelease>', self.update_highlight)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.restart_button = tk.Button(self.button_frame, text="Начать заново", command=self.reset_game, font=font_small)
        self.restart_button.grid(row=0, column=0, padx=5)

        self.record_button = tk.Button(self.button_frame, text="Статистика", command=self.show_record, font=font_small)
        self.record_button.grid(row=0, column=1, padx=5)

        # Инициализация подсветки
        self.words = self.text_display.get("1.0", tk.END).strip().split()
        self.current_word_index = 0
        self.correct_words = 0
        self.start_time = 0
        self.highlight_current_word()

    def initialize_stats_file(self):
        """Создает stats.txt с начальной статистикой, если файла нет."""
        record_file = "stats.txt"
        if not os.path.exists(record_file):
            initial_stats = {"best_speed": None, "sessions": 0}
            with open(record_file, "w") as file:
                json.dump(initial_stats, file, indent=4)

    def get_random_text(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                return random.choice(lines).strip() if lines else ""
        except FileNotFoundError:
            return "Файл text.txt не найден. Проверьте наличие файла."

    def highlight_current_word(self):
        """Выделяет текущее слово красным цветом."""
        if self.current_word_index < len(self.words):  # Проверяем допустимость индекса
            self.text_display.configure(state="normal")
            self.text_display.tag_remove("highlight", "1.0", "end")  # Убираем предыдущее выделение

            words = self.text_display.get("1.0", tk.END).strip().split()
            start_idx = "1.0"
            for i, word in enumerate(words):
                end_idx = f"{start_idx} + {len(word)}c"
                if i == self.current_word_index:
                    self.text_display.tag_add("highlight", start_idx, end_idx)
                    self.text_display.tag_config("highlight", foreground="red")  # Красный цвет текущего слова
                start_idx = f"{end_idx} + 1c"  # Переход к следующему слову

            self.text_display.configure(state="disabled")

    def update_highlight(self, event=None):
        """Обновляет подсветку текущего слова, если пользователь вводит текст."""
        if self.current_word_index < len(self.words):  # Проверяем допустимость индекса
            typed_text = self.text_entry.get().strip()
            current_word = self.words[self.current_word_index]

            # Если ввод больше текущего слова, не делаем ничего
            if len(typed_text) > len(current_word):
                return

    def check_word(self, event):
        if self.start_time == 0:  # Начинаем таймер на первом слове
            self.start_time = time.time()

        if self.current_word_index < len(self.words):  # Проверяем допустимость индекса
            typed_word = self.text_entry.get().strip()  # Получаем введённое слово
            self.text_entry.delete(0, tk.END)  # Очищаем поле ввода

            # Проверяем правильность ввода текущего слова
            if typed_word == self.words[self.current_word_index]:
                self.correct_words += 1  # Увеличиваем счётчик правильных слов

            self.current_word_index += 1  # Переходим к следующему слову только на пробеле

            if self.current_word_index < len(self.words):
                # Обновляем подсветку на следующее слово
                self.highlight_current_word()
            else:
                # Все слова введены, завершаем игру
                self.calculate_speed()

    def calculate_speed(self):
        end_time = time.time()
        total_time = end_time - self.start_time

        total_words = len(self.words)
        words_per_minute = (total_words / total_time) * 60 if total_time > 0 else 0
        accuracy = (self.correct_words / total_words) * 100 if total_words > 0 else 0  # Рассчитываем точность

        messagebox.showinfo("Результат",
                            f"Время: {total_time:.2f} секунд\n"
                            f"Скорость печати: {words_per_minute:.2f} слов в минуту\n"
                            f"Точность: {accuracy:.2f}%")

        # Сохраняем рекорд, только если точность 100%
        self.update_stats(words_per_minute if accuracy == 100 else None)
        self.reset_game()

    def update_stats(self, words_per_minute):
        """Обновляет статистику: рекорд и количество сессий."""
        record_file = "stats.txt"
        stats = {"best_speed": None, "sessions": 0}

        # Читаем текущую статистику
        if os.path.exists(record_file):
            with open(record_file, "r") as file:
                stats = json.load(file)

        # Обновляем количество сессий
        stats["sessions"] += 1

        # Обновляем лучший результат, если точность 100% и результат лучше текущего
        if words_per_minute is not None:
            if stats["best_speed"] is None or words_per_minute > stats["best_speed"]:
                stats["best_speed"] = words_per_minute

        # Сохраняем обновленную статистику
        with open(record_file, "w") as file:
            json.dump(stats, file, indent=4)

    def show_record(self):
        """Отображает рекорд и количество тренировок из файла stats.txt."""
        record_file = "stats.txt"
        if os.path.exists(record_file):
            with open(record_file, "r") as file:
                stats = json.load(file)
                best_speed = stats.get("best_speed", None)
                sessions = stats.get("sessions", 0)

                # Проверяем, установлен ли рекорд
                if best_speed is None:
                    best_speed_text = "Рекорд не установлен"
                else:
                    best_speed_text = f"{best_speed:.2f} слов в минуту"

                # Выводим информацию
                messagebox.showinfo("Статистика",
                                    f"Лучшая скорость печати: {best_speed_text}\n"
                                    f"Всего тренировок: {sessions}")
        else:
            messagebox.showinfo("Статистика", "Файл с рекордами не найден.")

    def reset_game(self):
        # Сбрасываем игру для нового теста
        self.text_to_type = self.get_random_text("text.txt")
        self.words = self.text_to_type.split()
        self.current_word_index = 0
        self.correct_words = 0
        self.start_time = 0
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", "end")
        self.text_display.insert("1.0", self.text_to_type)
        self.text_display.configure(state="disabled")
        self.text_entry.delete(0, tk.END)
        self.highlight_current_word()


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.geometry("600x400")  # Увеличиваем высоту окна
    root.mainloop()