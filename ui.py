import tkinter as tk
from tkinter import messagebox

from tictactoe import TicTacToe, QLearningAgent

class TicTacToeUI:
    def __init__(self, master):
        self.master = master
        self.game = TicTacToe()
        self.agent = QLearningAgent()
        self.agent.import_qtable('qtable')
        self.agent.epsilon = 0
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.init_symbol_selection_ui()

    def init_symbol_selection_ui(self):
        self.master.title("Select Your Symbol")
        self.x_button = tk.Button(self.master, text='O', command=lambda: self.set_symbols('O'))
        self.x_button.pack(side=tk.LEFT, padx=(100, 20), pady=20)
        
        self.o_button = tk.Button(self.master, text='X', command=lambda: self.set_symbols('X'))
        self.o_button.pack(side=tk.RIGHT, padx=(20, 100), pady=20)

    def set_symbols(self, player_symbol):
        self.player_symbol = player_symbol
        self.o_button.destroy()
        self.x_button.destroy()
        self.init_ui()

    def init_ui(self):
        self.master.title("Tic Tac Toe")
        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.master, text='', font=('Arial', 24), height=2, width=5,
                                command=lambda r=r, c=c: self.on_cell_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn
        restart_button = tk.Button(self.master, text='Restart', command=self.restart_game)
        restart_button.grid(row=3, column=0, columnspan=3)
        if self.player_symbol == 'X':
            agent_move = self.agent.choose_action(self.game.board, self.game.available_actions())
            self.game.make_move(agent_move)
            self.update_board_ui()
    
    def on_cell_click(self, row, col):
            self.game.make_move((row, col))
            self.update_board_ui()
            winner = self.game.check_winner()
            if winner == 1:
                messagebox.showinfo("Game Over", "You won!" if self.player_symbol == 'O' else "You lost!")
                self.restart_game()
                return
            elif winner == 0:
                messagebox.showinfo("Game Over", "Tie!")
                self.restart_game()
                return
            elif winner == -1:
                messagebox.showinfo("Game Over", "You won!" if self.player_symbol == 'X' else "You lost!")
                self.restart_game()
                return
                
            agent_move = self.agent.choose_action(self.game.board, self.game.available_actions())
            self.game.make_move(agent_move)
            self.update_board_ui()
            winner = self.game.check_winner()
            if winner == 1:
                messagebox.showinfo("Game Over", "You won!" if self.player_symbol == 'O' else "You lost!")
                self.restart_game()
            elif winner == 0:
                messagebox.showinfo("Game Over", "Tie!")
                self.restart_game()
            elif winner == -1:
                messagebox.showinfo("Game Over", "You won!" if self.player_symbol == 'X' else "You lost!")
                self.restart_game()


    def update_board_ui(self):
        for r in range(3):
            for c in range(3):
                value = self.game.board[r][c]
                text = 'X' if value == -1 else 'O' if value == 1 else ''
                self.buttons[r][c]['text'] = text

    def restart_game(self):
        self.game = TicTacToe()  # Reset the game
        self.update_board_ui()  # Reset the UI
        if self.player_symbol == 'X':
            agent_move = self.agent.choose_action(self.game.board, self.game.available_actions())
            self.game.make_move(agent_move)
            self.update_board_ui()

# Commenting out the Tkinter main loop to prevent execution here.
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeUI(root)
    root.mainloop()
