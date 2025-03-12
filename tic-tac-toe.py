import math
import tkinter as tk
from tkinter import messagebox

# Function to check for a winner
def check_winner(board, player):
    # Check rows, columns, and diagonals
    for row in board:
        if all([spot == player for spot in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

# Function to check if the board is full
def is_full(board):
    return all([spot != " " for row in board for spot in row])

# Minimax algorithm to find the optimal move
def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if is_full(board):
        return 0
    
    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

# Function to find the best move for the AI
def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# GUI-based Tic-Tac-Toe game using tkinter
class TicTacToe:
    def __init__(self, root):  # Fixed constructor method
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_buttons()

    # Function to create buttons for the board
    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text=" ", font=('normal', 40), width=5, height=2,
                                               command=lambda i=i, j=j: self.player_move(i, j))
                self.buttons[i][j].grid(row=i, column=j)

    # Player's move function
    def player_move(self, i, j):
        if self.buttons[i][j]["text"] == " " and not check_winner(self.board, 'X') and not check_winner(self.board, 'O'):
            self.buttons[i][j]["text"] = 'X'
            self.board[i][j] = 'X'
            if check_winner(self.board, 'X'):
                self.show_result("You win!")
            elif is_full(self.board):
                self.show_result("It's a tie!")
            else:
                self.ai_move()

    # AI's move function
    def ai_move(self):
        move = best_move(self.board)
        if move:
            self.buttons[move[0]][move[1]]["text"] = 'O'
            self.board[move[0]][move[1]] = 'O'
        if check_winner(self.board, 'O'):
            self.show_result("AI wins!")
        elif is_full(self.board):
            self.show_result("It's a tie!")

    # Show result using a message box
    def show_result(self, result):
        messagebox.showinfo("Game Over", result)
        self.reset_board()

    # Reset the board for a new game
    def reset_board(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = " "

# Main function to start the game
def play_game():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

# Run the game
play_game()
