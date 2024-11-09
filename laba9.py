import tkinter as tk
from tkinter import messagebox
import time

# Стилизация
font_big = ("Helvetica", 36, "bold")
font_small = ("Helvetica", 18)
button_color_x = "#ff6347"
button_color_o = "#32cd32"
button_color_empty = "#327669"
button_text_color = "#ffffff"
bg_global_color = "#3e9382"
font_color_main = "#1fffd3"
font_color_second = "#40c3a9"
button_color = "#2c786a"
button_active_color = "#7eb8ae"

# Настройки окна
window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("750x750")
window.resizable(False, False)
window.configure(bg=bg_global_color)

# Инициализация переменных игры
current_player = "❌"
board = [""] * 9
play_vs_computer = False
game_start_time = None

# Главное меню
def show_main_menu():
    main_menu_frame.pack(pady=20)
    hide_game_screen()

def hide_main_menu():
    main_menu_frame.pack_forget()

def show_game_screen():
    game_screen_frame.pack(pady=20)

def hide_game_screen():
    game_screen_frame.pack_forget()

# Проверка на победителя
def check_winner():
    winning_combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in winning_combos:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    return "Ничья" if "" not in board else None

# Логика хода компьютера
def minimax(is_maximizing):
    winner = check_winner()
    if winner == "❌":
        return -1
    elif winner == "⚫":
        return 1
    elif winner == "Ничья":
        return 0

    best_score = -float('inf') if is_maximizing else float('inf')
    symbol = "⚫" if is_maximizing else "❌"
    for i in range(9):
        if board[i] == "":
            board[i] = symbol
            score = minimax(not is_maximizing)
            board[i] = ""
            best_score = max(score, best_score) if is_maximizing else min(score, best_score)
    return best_score

# Ход компьютера
def computer_turn():
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "⚫"
            score = minimax(False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i
    if best_move is not None:
        board[best_move] = "⚫"
        buttons[best_move].config(text="⚫", state="disabled", disabledforeground=button_text_color, bg=button_color_o)
        if check_winner():
            show_result(check_winner())
        else:
            switch_turn()

# Обработка нажатия на кнопку
def button_click(index):
    global current_player
    if board[index] == "" and not check_winner():
        board[index] = current_player
        buttons[index].config(text=current_player, state="disabled", disabledforeground=button_text_color, bg=button_color_x if current_player == "❌" else button_color_o)
        if check_winner():
            show_result(check_winner())
        else:
            if play_vs_computer and current_player == "❌":
                switch_turn()
                computer_turn()
            else:
                switch_turn()

# Переключение хода между игроками
def switch_turn():
    global current_player
    current_player = "⚫" if current_player == "❌" else "❌"
    label_turn.config(text=f"Ходят {current_player}")
    label_turn.config(fg=button_color_x if current_player == "❌" else button_color_o)

# Отображение результата игры
def show_result(winner):
    messagebox.showinfo("Результат", f"{'Игра закончилась в ничью!' if winner == 'Ничья' else f'Выиграл игрок {winner}!'}")
    reset_game()

# Перезапуск игры
def reset_game():
    global board, current_player, game_start_time
    board = [""] * 9
    current_player = "❌"
    game_start_time = time.time()  # Сбрасываем таймер
    for button in buttons:
        button.config(text="", state="normal", bg=button_color_empty)
    label_turn.config(text=f"Ходят {current_player}", fg=button_color_x)
    label_time.config(text="Время: 00:00")

# Начало игры против компьютера
def start_vs_computer():
    global play_vs_computer
    play_vs_computer = True
    hide_main_menu()
    show_game_screen()
    label_status.config(text="Игра против компьютера", fg=font_color_main)
    reset_game()

# Начало игры против другого игрока
def start_vs_player():
    global play_vs_computer
    play_vs_computer = False
    hide_main_menu()
    show_game_screen()
    label_status.config(text="Игра против игрока", fg=font_color_main)
    reset_game()

# Обновление таймера
def update_timer():
    if game_start_time:
        elapsed_time = time.time() - game_start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        label_time.config(text=f"Время: {minutes:02}:{seconds:02}")
    window.after(1000, update_timer)

# Главное меню
main_menu_frame = tk.Frame(window, bg=bg_global_color)
main_menu_frame.pack(pady=20)

title_label = tk.Label(main_menu_frame, text="Игра «крестики-нолики»", font=font_big, bg=bg_global_color, fg=font_color_main)
title_label.pack(pady=20)

play_button = tk.Button(main_menu_frame, text="1 Игрок", font=font_small, command=start_vs_computer, bg=button_color, fg="#e9e9e9", padx="100", activebackground=button_active_color, relief="flat", bd=0)
play_button.pack(pady=10)

player_vs_player_button = tk.Button(main_menu_frame, text="2 Игрока", font=font_small, command=start_vs_player, bg=button_color, fg="#e9e9e9", padx="94", activebackground=button_active_color, relief="flat", bd=0)
player_vs_player_button.pack(pady=10)

exit_button = tk.Button(main_menu_frame, text="Выход", font=font_small, command=window.quit, bg="#ff6f6a", fg="#e9e9e9", padx="108", activebackground="#ffa4a1", relief="flat", bd=0)
exit_button.pack(pady=10)

# Экран игры
game_screen_frame = tk.Frame(window, bg=bg_global_color)

label_status = tk.Label(game_screen_frame, text="Игра против игрока", font=font_big, bg=bg_global_color, fg=font_color_main)
label_status.pack(pady=20)

label_turn = tk.Label(game_screen_frame, text=f"Ходят {current_player}", font=font_small, bg=button_color_empty, fg=button_color_x, padx="110")
label_turn.pack()

# Таймер
label_time = tk.Label(game_screen_frame, text="Время: 00:00", font=font_small, bg=button_color_empty, fg="#e9e9e9", padx="90")
label_time.pack()

# Создаем игровое поле
frame = tk.Frame(game_screen_frame, bg=bg_global_color)
frame.pack(pady=30)

buttons = []
for i in range(9):
    button = tk.Button(frame, text="", font=font_big, width=3, height=1,
                       command=lambda i=i: button_click(i), relief="flat", bd=0, fg=button_text_color, bg=button_color_empty)
    button.grid(row=i // 3, column=i % 3, padx=10, pady=10)
    buttons.append(button)

# Панель управления
control_frame = tk.Frame(game_screen_frame, bg=bg_global_color)
control_frame.pack(pady=20)

reset_button = tk.Button(control_frame, text="Рестарт", font=font_small, command=reset_game, bg=button_color, fg="#e9e9e9", activebackground=button_active_color, relief="flat", bd=0)
reset_button.grid(row=0, column=0, padx=20)

back_button = tk.Button(control_frame, text="Выход в меню", font=font_small, command=show_main_menu, bg="#ff6f6a", fg="#e9e9e9", activebackground="#ffa4a1", relief="flat", bd=0)
back_button.grid(row=0, column=1, padx=20)

update_timer()  # Начинаем обновление таймера

# Показ главного меню при старте
show_main_menu()

window.mainloop()