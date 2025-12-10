import tkinter as tk
from tkinter import messagebox

board = [["" for _ in range(3)] for _ in range(3)]
buttons = []

def create_pole():
    global buttons
    window = tk.Tk()
    window.title("Крестики-нолики")
    window.resizable(False, False)
    for i in range(3):
        row_buttons = []
        for j in range(3):
            button = tk.Button(window, text="", font=("Veranda", 21, "bold"), fg="navy", bg="lightblue", activebackground="steelblue", width=5, height=2, command=lambda row=i, col=j: hod_player_1(row, col))
            button.grid(row=i, column=j, padx=2, pady=2)
            row_buttons.append(button)
        buttons.append(row_buttons)
    return window

def hod_player_1(row, col):
    if board[row][col] != "" or check_winner() or is_board_full(): return
    board[row][col] = "X"
    buttons[row][col].config(text="X")
    if check_winner(): messagebox.showinfo("Победа!", "Вы победили!")
    elif is_board_full(): messagebox.showinfo("Ничья!", "Ничья!")
    else: hod_bot()

def hod_bot():
    best_score, best_move = float('-inf'), None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "0"
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score: best_score, best_move = score, (i, j)
    if best_move:
        i, j = best_move
        board[i][j] = "0"
        buttons[i][j].config(text="0")
        if check_winner(): messagebox.showinfo("Проигрыш!", "Вы проиграли")
        elif is_board_full(): messagebox.showinfo("Ничья!", "Ничья!")

def minimax(board, depth, is_maximizing):
    winner = check_winner_minimax(board)
    if winner == "0": return 10 - depth
    elif winner == "X": return depth - 10
    elif is_board_full_minimax(board): return 0
    best_score = float('-inf') if is_maximizing else float('inf')
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "0" if is_maximizing else "X"
                score = minimax(board, depth + 1, not is_maximizing)
                board[i][j] = ""
                best_score = max(score, best_score) if is_maximizing else min(score, best_score)
    return best_score

def check_winner():
    return check_winner_minimax(board)

def check_winner_minimax(current_board):
    for i in range(3):
        if current_board[i][0] == current_board[i][1] == current_board[i][2] != "": return current_board[i][0]
    for j in range(3):
        if current_board[0][j] == current_board[1][j] == current_board[2][j] != "": return current_board[0][j]
    if current_board[0][0] == current_board[1][1] == current_board[2][2] != "": return current_board[0][0]
    if current_board[0][2] == current_board[1][1] == current_board[2][0] != "": return current_board[0][2]
    return None

def is_board_full():
    return all(board[i][j] != "" for i in range(3) for j in range(3))
def is_board_full_minimax(current_board):
    return all(current_board[i][j] != "" for i in range(3) for j in range(3))

def start_game():
    window = create_pole()
    window.mainloop()

if __name__ == "__main__":
    start_game()
