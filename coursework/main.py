from tkinter import Tk, Canvas, PhotoImage, Button, Label, Entry, StringVar, Frame
from checkers.game import Game
from checkers.constants import X_SIZE, Y_SIZE, CELL_SIZE
from checkers.enums import SideType, CheckerType
import json
import base64
import os

# Дизайн, выбор фигуры, кнопка выйти из профиля, сохранение статистики против компа

# Path to users.json
users_file_path = 'users.json'


# Helper functions for user management
def load_users(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_users(file_path, users):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4)


def encrypt_password(password):
    return base64.b64encode(password.encode()).decode()


def decrypt_password(encoded_password):
    return base64.b64decode(encoded_password.encode()).decode()


class CheckersApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Шашки-поддавки')
        self.root.resizable(0, 0)
        self.root.iconphoto(False, PhotoImage(file='icon.png'))

        # Current user and main canvas
        self.current_user = None
        self.main_canvas = None

        # Frames for login and main menu
        self.login_frame = Frame(root)
        self.menu_frame = Frame(root)
        self.game_frame = Frame(root)

        self.show_login_frame()

    def show_login_frame(self):
        # Display the login/registration interface
        self.clear_frames()
        self.login_frame.pack()

        Label(self.login_frame, text="     Шашки-поддавки     ", font=("Arial", 16)).pack(pady=10)

        Label(self.login_frame, text="Имя пользователя:").pack(pady=5)
        username_var = StringVar()
        Entry(self.login_frame, textvariable=username_var).pack(pady=5)

        Label(self.login_frame, text="Пароль:").pack(pady=5)
        password_var = StringVar()
        Entry(self.login_frame, textvariable=password_var, show="*").pack(pady=5)

        def login():
            users = load_users(users_file_path)
            username = username_var.get()
            password = password_var.get()
            if username in users and decrypt_password(users[username]) == password:
                self.current_user = username
                self.show_menu_frame()
            else:
                Label(self.login_frame, text="Неверные имя пользователя или пароль!", fg="red").pack()

        def register():
            users = load_users(users_file_path)
            username = username_var.get()
            password = password_var.get()
            if username in users:
                Label(self.login_frame, text="Имя пользователя уже занято!", fg="red").pack()
            else:
                users[username] = encrypt_password(password)
                save_users(users_file_path, users)
                Label(self.login_frame, text="Регистрация успешна!", fg="green").pack()

        Button(self.login_frame, text="Вход", command=login).pack(pady=5)
        Button(self.login_frame, text="Регистрация", command=register).pack(pady=5)

    def show_menu_frame(self):
        # Display the main menu interface
        self.clear_frames()
        self.menu_frame.pack()

        Label(self.menu_frame, text=f"Добро пожаловать, {self.current_user}!", font=("Arial", 16)).pack(pady=10)
        Button(self.menu_frame, text="Игра с компьютером", command=self.start_game_with_computer, width=30).pack(pady=5)
        Button(self.menu_frame, text="Игра для двух игроков", command=self.start_two_player_game, width=30).pack(pady=5)
        Button(self.menu_frame, text="Выход", command=self.root.quit, width=30).pack(pady=5)

    def start_game_with_computer(self):
        # Start a game against the computer
        self.start_game(player_vs_computer=True)

    def start_two_player_game(self):
        # Start a two-player game
        self.start_game(player_vs_computer=False)

    def start_game(self, player_vs_computer):
        # Initialize the game
        self.clear_frames()
        self.game_frame.pack()

        # Создаем левую панель для информации
        left_panel = Frame(self.game_frame)
        left_panel.pack(side='left', padx=20)

        # Добавляем информационные метки
        self.turn_label = Label(left_panel, text="Ход: Белые", font=("Arial", 14))
        self.turn_label.pack(pady=10)

        # Счетчики шашек
        score_frame = Frame(left_panel)
        score_frame.pack(pady=10)

        self.white_score_label = Label(score_frame, text="Белые шашки: 12", font=("Arial", 12))
        self.white_score_label.pack()

        self.black_score_label = Label(score_frame, text="Черные шашки: 12", font=("Arial", 12))
        self.black_score_label.pack()

        # Кнопки управления
        Button(left_panel, text="Рестарт", command=lambda: self.restart_game(player_vs_computer),
               width=15).pack(pady=5)
        Button(left_panel, text="В главное меню", command=self.show_menu_frame,
               width=15).pack(pady=5)

        # Создаем игровое поле
        self.main_canvas = Canvas(self.game_frame, width=CELL_SIZE * X_SIZE, height=CELL_SIZE * Y_SIZE)
        self.main_canvas.pack(side='left')

        # Создаем игру и сохраняем ссылку на нее
        self.current_game = Game(self.main_canvas, X_SIZE, Y_SIZE, self.update_game_info)

        if player_vs_computer:
            self.main_canvas.bind("<Motion>", self.current_game.mouse_move)
            self.main_canvas.bind("<Button-1>", self.current_game.mouse_down)
        else:
            self.current_game.enable_two_player_mode()
            self.main_canvas.bind("<Motion>", self.current_game.mouse_move)
            self.main_canvas.bind("<Button-1>", self.current_game.mouse_down)

    def update_game_info(self, current_side: SideType, white_count: int, black_count: int):
        """Обновление информации об игре"""
        self.turn_label.config(text=f"Ход: {'Белые' if current_side == SideType.WHITE else 'Черные'}")
        self.white_score_label.config(text=f"Белые шашки: {white_count}")
        self.black_score_label.config(text=f"Черные шашки: {black_count}")

    def restart_game(self, player_vs_computer):
        """Перезапуск игры"""
        # Очищаем текущее состояние
        if hasattr(self, 'current_game'):
            del self.current_game

        # Очищаем метки перед новой игрой
        self.turn_label.config(text="Ход: Белые")
        self.white_score_label.config(text="Белые шашки: 12")
        self.black_score_label.config(text="Черные шашки: 12")

        # Запускаем новую игру
        self.start_game(player_vs_computer)

    def clear_frames(self):
        # Clear all frames
        for frame in [self.login_frame, self.menu_frame, self.game_frame]:
            frame.pack_forget()
            for widget in frame.winfo_children():
                widget.destroy()


if __name__ == '__main__':
    root = Tk()
    app = CheckersApp(root)
    root.mainloop()
