import pygame
from src.soldier_cls import Soldier
from config import Config


class Board:

    def __init__(self):
        self.white_left = self.black_left = 12
        self.board = []
        self.init_start_game()
        self.white_king = self.black_kings = 0

    @staticmethod
    def draw_squares(win):
        win.fill(Config.RED)
        for row in range(Config.ROWS):
            for col in range(row % 2, Config.ROWS, 2):
                pygame.draw.rect(win, Config.WHITE, (
                    row * Config.SQUARE_SIZE, col * Config.SQUARE_SIZE, Config.SQUARE_SIZE, Config.SQUARE_SIZE))

    def draw(self, win):
        self.draw_squares(win)
        for row in range(Config.ROWS):
            for col in range(Config.COLS):
                if self.board[row][col] != 0:
                    self.board[row][col].draw(win)

    def init_start_game(self):
        for row in range(Config.ROWS):
            self.board.append([])
            for col in range(Config.ROWS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Soldier(row=row, col=col, color=Config.WHITE))
                    elif row > 4:
                        self.board[row].append(Soldier(row=row, col=col, color=Config.BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def move(self, soldier, row, col):
        if not isinstance(soldier, Soldier):
            return
        self.board[row][col] = self.board[soldier.row][soldier.col]
        self.board[soldier.row][soldier.col] = 0
        soldier.row = row
        soldier.col = col
        soldier.calc_pos()
        if (row == Config.ROWS or row == 0) and soldier.is_king is False:
            soldier.make_king()
            if soldier.color == Config.WHITE:
                self.white_king += 1
            else:
                self.black_kings += 1

    def get_soldier(self, row, col):
        return self.board[row][col]

    def __str__(self):
        string = ""
        for i in range(Config.ROWS):
            for j in range(Config.ROWS):
                string += f"{self.board[i][j]}"
                if j == Config.ROWS - 1:
                    string += "\n"
        return string
