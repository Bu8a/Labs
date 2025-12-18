import tkinter as tk
from tkinter import messagebox, ttk
import hashlib

class UserManager:
    def __init__(self):
        self.users = {"admin": self.hash_password("1234")}

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def is_valid_username(self, username):
        if not username or not ('a' <= username[0].lower() <= 'z'):
            return False
        for char in username:
            if not (('a' <= char.lower() <= 'z') or ('0' <= char <= '9')):
                return False
        return True

    def register(self, username, password):
        if username in self.users:
            return False, "Пользователь уже существует"
        if len(username) < 3:
            return False, "Логин минимум 3 символа"
        if not self.is_valid_username(username):
            return False, "Логин: только латынь и цифры, начиная с буквы"
        if len(password) < 4:
            return False, "Пароль минимум 4 символа"
        self.users[username] = self.hash_password(password)
        return True, "Регистрация успешна"

    def login(self, username, password):
        if username not in self.users:
            return False, "Пользователь не найден"
        if self.users[username] != self.hash_password(password):
            return False, "Неверный пароль"
        return True, "Вход выполнен"

class AuthWindow:
    def __init__(self, root):
        self.root = root
        self.user_manager = UserManager()
        self.current_user = None
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Король и Ферзь против Короля")
        self.root.geometry("350x400")

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Король и Ферзь против Короля", font=('Arial', 14, 'bold')).pack(pady=10)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(pady=10, fill=tk.BOTH, expand=True)

        login_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(login_frame, text="Вход")
        ttk.Label(login_frame, text="Логин:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.login_user = ttk.Entry(login_frame)
        self.login_user.grid(row=0, column=1, pady=5)
        ttk.Label(login_frame, text="Пароль:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.login_pass = ttk.Entry(login_frame, show="*")
        self.login_pass.grid(row=1, column=1, pady=5)
        ttk.Button(login_frame, text="Войти", command=self.do_login).grid(row=2, column=0, columnspan=2, pady=15)

        reg_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(reg_frame, text="Регистрация")
        ttk.Label(reg_frame, text="Логин:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.reg_user = ttk.Entry(reg_frame)
        self.reg_user.grid(row=0, column=1, pady=5)
        ttk.Label(reg_frame, text="Пароль:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_pass = ttk.Entry(reg_frame, show="*")
        self.reg_pass.grid(row=1, column=1, pady=5)
        ttk.Button(reg_frame, text="Зарегистрироваться", command=self.do_register).grid(row=2, column=0, columnspan=2,
                                                                                        pady=15)

        self.status = ttk.Label(main_frame, text="", foreground='red')
        self.status.pack()

    def do_login(self):
        user = self.login_user.get().strip()
        password = self.login_pass.get()
        success, msg = self.user_manager.login(user, password)
        if success:
            self.current_user = user
            self.start_game()
        else:
            self.status.config(text=msg, foreground='red')

    def do_register(self):
        user = self.reg_user.get().strip()
        password = self.reg_pass.get()
        success, msg = self.user_manager.register(user, password)
        self.status.config(text=msg, foreground='green' if success else 'red')
        if success:
            self.notebook.select(0)
            self.login_user.delete(0, tk.END)
            self.login_user.insert(0, user)

    def start_game(self):
        self.root.withdraw()
        game_window = tk.Toplevel(self.root)
        GameWindow(game_window, self.current_user, self)

class GameWindow:
    def __init__(self, root, username, auth_app):
        self.root = root
        self.username = username
        self.auth_app = auth_app
        self.board_size = 8
        self.cell_size = 60
        self.padding = 35

        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.game_over = False
        self.selected_piece = None
        self.possible_moves = []

        self.setup_ui()
        self.reset_game()

    def setup_ui(self):
        self.root.title("Король и Ферзь против Короля")
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(top_frame, text=f"Игрок: {self.username}").pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Выйти из игры", command=self.logout).pack(side=tk.RIGHT)

        self.status_label = ttk.Label(self.root, text="", font=('Arial', 12, 'bold'))
        self.status_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=550, height=550, bg="#f0f0f0")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        ttk.Button(self.root, text="Начать новую партию", command=self.reset_game).pack(pady=10)

    def reset_game(self):
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.board[7][4] = 'WK'
        self.board[7][3] = 'WQ'
        self.board[0][4] = 'BK'
        self.game_over = False
        self.current_player = 'white'
        self.selected_piece = None
        self.possible_moves = []
        self.update_status()
        self.draw_board()

    def update_status(self):
        turn = "Черных " if self.current_player == 'white' else "Белых"
        color = "#000000" if self.current_player == 'white' else "#000000"

        k_pos = self.find_king('W' if self.current_player == 'white' else 'B')
        msg = f"Ход {turn}"
        if self.is_under_attack(k_pos[0], k_pos[1], 'B' if self.current_player == 'white' else 'W'):
            msg += " — ВАМ ШАХ!"

        self.status_label.config(text=msg, foreground=color)

    def find_king(self, color_prefix):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == color_prefix + 'K':
                    return (r, c)
        return (0, 0)

    def is_under_attack(self, r, c, attacker_color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece.startswith(attacker_color):
                    if piece.endswith('K'):
                        if abs(row - r) <= 1 and abs(col - c) <= 1:
                            return True
                    else:
                        moves = self.get_raw_moves(row, col)
                        if (r, c) in moves:
                            return True
        return False

    def get_raw_moves(self, r, c):
        piece = self.board[r][c]
        moves = []
        if piece.endswith('K'):
            dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if not self.board[nr][nc].startswith(piece[0]):
                        moves.append((nr, nc))
        elif piece.endswith('Q'):
            dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc].startswith(piece[0]): break
                    moves.append((nr, nc))
                    if self.board[nr][nc] != '': break
                    nr += dr
                    nc += dc
        return moves

    def get_legal_moves(self, r, c):
        raw_moves = self.get_raw_moves(r, c)
        legal_moves = []
        piece = self.board[r][c]
        my_color = piece[0]
        enemy_color = 'B' if my_color == 'W' else 'W'

        for nr, nc in raw_moves:
            old_piece = self.board[nr][nc]
            self.board[nr][nc] = piece
            self.board[r][c] = ''

            kr, kc = self.find_king(my_color)

            if not self.is_under_attack(kr, kc, enemy_color):
                legal_moves.append((nr, nc))

            self.board[r][c] = piece
            self.board[nr][nc] = old_piece

        return legal_moves

    def on_click(self, event):
        if self.game_over: return

        col = (event.x - self.padding) // self.cell_size
        row = (event.y - self.padding) // self.cell_size

        if not (0 <= row < 8 and 0 <= col < 8): return

        if self.selected_piece:
            if (row, col) in self.possible_moves:
                fr, fc = self.selected_piece
                self.board[row][col] = self.board[fr][fc]
                self.board[fr][fc] = ''

                self.current_player = 'black' if self.current_player == 'white' else 'white'
                self.selected_piece = None
                self.possible_moves = []
                self.draw_board()
                self.update_status()
                self.check_end_condition()
            else:
                self.selected_piece = None
                self.possible_moves = []
                self.draw_board()
        else:
            piece = self.board[row][col]
            if (self.current_player == 'white' and piece.startswith('W')) or \
                    (self.current_player == 'black' and piece.startswith('B')):
                self.selected_piece = (row, col)
                self.possible_moves = self.get_legal_moves(row, col)
                self.draw_board()

    def check_end_condition(self):
        my_color = 'W' if self.current_player == 'white' else 'B'
        enemy_color = 'B' if my_color == 'W' else 'W'

        all_pieces = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != '':
                    all_pieces.append(self.board[r][c])

        if len(all_pieces) == 2:
            if 'WK' in all_pieces and 'BK' in all_pieces:
                messagebox.showinfo("Конец игры", "ПАТ! Ничья.")
                self.game_over = True
                return

        has_legal_moves = False
        for r in range(8):
            for c in range(8):
                if self.board[r][c].startswith(my_color):
                    if self.get_legal_moves(r, c):
                        has_legal_moves = True
                        break
            if has_legal_moves: break

        if not has_legal_moves:
            kr, kc = self.find_king(my_color)
            in_check = self.is_under_attack(kr, kc, enemy_color)

            if in_check:
                winner = "Черные" if my_color == 'W' else "Белые"
                messagebox.showinfo("Конец игры", f"ШАХ И МАТ! Победили {winner}.")
            else:
                messagebox.showinfo("Конец игры", "ПАТ! Ничья.")

            self.game_over = True

    def draw_board(self):
        self.canvas.delete("all")
        letters = "ABCDEFGH"
        for i in range(8):
            self.canvas.create_text(self.padding + i * self.cell_size + 30, 15, text=letters[i], font=("Arial", 10))
            self.canvas.create_text(15, self.padding + i * self.cell_size + 30, text=str(8 - i), font=("Arial", 10))

        for r in range(8):
            for c in range(8):
                x1, y1 = self.padding + c * self.cell_size, self.padding + r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "#F0D9B5" if (r + c) % 2 == 0 else "#B58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

                if (r, c) in self.possible_moves:
                    self.canvas.create_oval(x1 + 22, y1 + 22, x2 - 22, y2 - 22, fill="#45a049")

                p = self.board[r][c]
                if p:
                    fill_c = "#333" if p.startswith('W') else "#eee"
                    text_c = "white" if p.startswith('W') else "black"
                    self.canvas.create_oval(x1 + 8, y1 + 8, x2 - 8, y2 - 8, fill=fill_c, outline="black")
                    label = "Кр" if p.endswith('K') else "Ф"
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=label, fill=text_c,
                                            font=("Arial", 14, "bold"))

        if self.selected_piece:
            r, c = self.selected_piece
            self.canvas.create_rectangle(self.padding + c * self.cell_size, self.padding + r * self.cell_size,
                                         self.padding + (c + 1) * self.cell_size,
                                         self.padding + (r + 1) * self.cell_size,
                                         outline="#4a9eff", width=3)

    def logout(self):
        self.root.destroy()
        self.auth_app.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthWindow(root)
    root.mainloop()
