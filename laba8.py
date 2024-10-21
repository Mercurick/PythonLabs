import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import random

class Circle:
    def __init__(self, x, y, radius, color='black'):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.segment_colors = [color, color, color, color]  # Цвета сегментов по умолчанию
        self.segmented = True

    def segment(self, canvas):
        # Сегментация круга на 4 части с случайной окраской каждого сегмента
        self.segment_colors = [random.choice(['red', 'blue', 'green', 'yellow', 'purple']) for _ in range(4)]

        # Закрашивание каждого из 4-х сегментов (четвертей круга)
        self.draw_segments(canvas)

    def draw_segments(self, canvas):
        # Рисование 4-х сегментов круга
        canvas.create_arc(self.x - self.radius, self.y - self.radius,
                          self.x + self.radius, self.y + self.radius,
                          start=0, extent=90, fill=self.segment_colors[0], outline=self.color)
        canvas.create_arc(self.x - self.radius, self.y - self.radius,
                          self.x + self.radius, self.y + self.radius,
                          start=90, extent=90, fill=self.segment_colors[1], outline=self.color)
        canvas.create_arc(self.x - self.radius, self.y - self.radius,
                          self.x + self.radius, self.y + self.radius,
                          start=180, extent=90, fill=self.segment_colors[2], outline=self.color)
        canvas.create_arc(self.x - self.radius, self.y - self.radius,
                          self.x + self.radius, self.y + self.radius,
                          start=270, extent=90, fill=self.segment_colors[3], outline=self.color)

    def visualize(self, canvas, highlight=False):
        # Визуализация круга, включая сегментацию, если она есть
        if all(color == self.color for color in self.segment_colors):  # Если круг не сегментирован
            canvas.create_oval(self.x - self.radius, self.y - self.radius,
                               self.x + self.radius, self.y + self.radius,
                               fill=self.color, outline='red' if highlight else self.color, width=2 if highlight else 1)
        else:  # Если круг сегментирован, рисуем сегменты
            self.draw_segments(canvas)
            if highlight:
                canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                   self.x + self.radius, self.y + self.radius,
                                   outline='red', width=2)

    def colorize(self, new_color):
        # Изменение цвета круга (если он не сегментирован)
        if all(color == self.color for color in self.segment_colors):
            self.color = new_color  # Изменить цвет круга
        else:
            # Если сегментирован, изменить цвет сегментов и сбросить сегментацию
            self.segment_colors = [new_color] * 4  # Установить новый цвет для всех сегментов
            self.segmented = False  # Вернуться к несегментированному состоянию
            self.color = new_color  # Обновить цвет круга

    def mirror(self, axis):
        # Зеркальное отображение сегментов относительно оси, меняя местами цвета
        if not self.segmented:
            messagebox.showinfo("Info", "Сначала сегментируйте круг перед отзеркаливанием, иначе ничего не произойдет.")
            return

        if axis == 'X':
            # Поменять местами верхние и нижние сегменты
            self.segment_colors[0], self.segment_colors[2] = self.segment_colors[2], self.segment_colors[0]
            self.segment_colors[1], self.segment_colors[3] = self.segment_colors[3], self.segment_colors[1]
        elif axis == 'Y':
            # Поменять местами левый и правый сегменты
            self.segment_colors[0], self.segment_colors[1] = self.segment_colors[1], self.segment_colors[0]
            self.segment_colors[2], self.segment_colors[3] = self.segment_colors[3], self.segment_colors[2]

    def to_string(self):
        # Сохранение данных круга в строковом формате для записи в файл
        segment_data = ','.join(self.segment_colors)
        return f"{self.x},{self.y},{self.radius},{self.color},{segment_data}"


# Основное окно программы
class CircleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("КОВАРНЫЙ МАНИПУЛЯТОР КРУЖКОВ")
        self.file_path = "circles.txt"  # Автоматическое сохранение в этом файле

        # Полотно для отрисовки
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()

        # Кнопки для взаимодействия
        self.load_button = tk.Button(root, text="Обзор..", command=self.load_circles)
        self.load_button.pack(side=tk.LEFT, padx=7, pady=5)

        self.color_button = tk.Button(root, text="Цвет", command=self.change_color)
        self.color_button.pack(side=tk.LEFT, padx=7)

        self.mirror_button = tk.Button(root, text="Отзеркалить", command=lambda: self.mirror('X'))
        self.mirror_button.pack(side=tk.LEFT, padx=7)

        self.segment_button = tk.Button(root, text="Сегментация", command=self.segment_circle)
        self.segment_button.pack(side=tk.LEFT, padx=7)

        self.add_button = tk.Button(root, text="Добавить круг", command=self.add_circle)
        self.add_button.pack(side=tk.LEFT, padx=7)

        self.delete_button = tk.Button(root, text="Удалить круг", command=self.delete_circle)
        self.delete_button.pack(side=tk.LEFT, padx=7)

        # Список для хранения кругов и индикатор текущего выбора
        self.circles = []
        self.selected_circle = None

        # Привязка событий
        self.canvas.bind("<Button-1>", self.select_circle)
        self.root.bind("<KeyPress>", self.move_circle)

    def load_circles(self):
        # Открытие файла и чтение данных
        file_path = filedialog.askopenfilename(title="Select file", filetypes=(("Text files", "*.txt"),))
        if not file_path:
            return
        self.file_path = file_path
        try:
            with open(self.file_path, 'r') as file:
                self.circles.clear()
                self.canvas.delete("all")
                for line in file:
                    data = line.strip().split(',')
                    x, y, radius = map(int, data[:3])
                    color = data[3]
                    segment_colors = data[4:8] if len(data) > 4 else [color] * 4
                    circle = Circle(x, y, radius, color)
                    circle.segment_colors = segment_colors
                    self.circles.append(circle)
                    circle.visualize(self.canvas)
        except Exception as e:
            messagebox.showerror("Error", f"Ошибка при загрузке файла: {e}")

    def add_circle(self):
        # Добавление нового круга в центр
        center_x = 20
        center_y = 20
        radius = 20
        circle = Circle(center_x, center_y, radius)
        self.circles.append(circle)
        self.redraw_circles()
        self.save_circles()

    def delete_circle(self):
        # Удаление выбранного круга
        if self.selected_circle:
            self.circles.remove(self.selected_circle)
            self.selected_circle = None  # Сбросить выделение
            self.redraw_circles()
            self.save_circles()

    def save_circles(self):
        # Автоматическое сохранение данных в файл
        if not self.file_path:
            return
        try:
            with open(self.file_path, 'w') as file:
                for circle in self.circles:
                    file.write(circle.to_string() + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Ошибка при сохранении файла: {e}")

    def change_color(self):
        # Изменение цвета выбранного круга через диалог выбора цвета
        if self.selected_circle:
            color = colorchooser.askcolor()[1]  # Получаем выбранный цвет
            if color:
                if self.selected_circle.segmented:
                    # Если круг сегментирован, сбрасываем сегментацию
                    self.selected_circle.segment_colors = [color] * 4  # Устанавливаем новый цвет для всех сегментов
                    self.selected_circle.segmented = False  # Убираем сегментацию
                else:
                    # Если круг не сегментирован, просто изменяем его цвет
                    self.selected_circle.colorize(color)
                self.redraw_circles()  # Перерисовываем круги
                self.save_circles()  # Сохраняем изменения

    def mirror(self, axis):
        # Зеркальное отображение выбранного круга
        if self.selected_circle:
            self.selected_circle.mirror(axis)
            self.redraw_circles()
            self.save_circles()

    def segment_circle(self):
        # Сегментация выбранного круга
        if self.selected_circle:
            self.selected_circle.segment(self.canvas)
            self.redraw_circles()
            self.save_circles()

    def select_circle(self, event):
        # Выбор круга по клику мыши
        for circle in self.circles:
            if (circle.x - circle.radius <= event.x <= circle.x + circle.radius) and (
                    circle.y - circle.radius <= event.y <= circle.y + circle.radius):
                self.selected_circle = circle
                self.redraw_circles()
                break

    def move_circle(self, event):
        # Перемещение выбранного круга стрелками
        if self.selected_circle:
            if event.keysym == 'Up':
                self.selected_circle.y -= 5
            elif event.keysym == 'Down':
                self.selected_circle.y += 5
            elif event.keysym == 'Left':
                self.selected_circle.x -= 5
            elif event.keysym == 'Right':
                self.selected_circle.x += 5
            elif event.keysym == 'plus':
                self.selected_circle.radius += 1
            elif event.keysym == 'minus':
                self.selected_circle.radius -= 1
            self.redraw_circles()
            self.save_circles()

    def redraw_circles(self):
        # Перерисовка всех кругов с выделением выбранного
        self.canvas.delete("all")
        for circle in self.circles:
            circle.visualize(self.canvas, highlight=(circle == self.selected_circle))


# Запуск программы
if __name__ == "__main__":
    root = tk.Tk()
    app = CircleApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.save_circles(), root.destroy()))
    root.mainloop()