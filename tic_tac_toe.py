from tkinter import Tk, Button
from tkinter.messagebox import showinfo
import ttt

# Initialize the game window
root = Tk()
root.title("Tic Tac Toe")

# Initialize game variables
player = True  # True for X's turn, False for O's turn
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]

def check_win():
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "" or board[0][2] == board[1][1] == board[2][0] != "":
        return board[1][1]
    return ""

def check_draw():
    for row in board:
        if "" in row:
            return False
    return True

def reset_game():
    global player, board
    player = True
    board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal")

def button_click(i, j):
    global player
    if player:
        buttons[i][j].config(text="X", state="disabled")
        board[i][j] = "X"
    else:
        buttons[i][j].config(text="O", state="disabled")
        board[i][j] = "O"
    winner = check_win()
    if winner != "":
        showinfo("Game Over", f"{winner} wins!")
        reset_game()
        return
    if check_draw():
        showinfo("Game Over", "It's a draw!")
        reset_game()
        return
    player = not player

def create_board():
    for i in range(3):
        for j in range(3):
            button = Button(root, text="", width=10, height=3, 
                            command=lambda i=i, j=j: button_click(i, j))
            button.grid(row=i, column=j)
            buttons[i][j] = button

create_board()

# Uncomment the following line to start the Tkinter event loop
root.mainloop()
