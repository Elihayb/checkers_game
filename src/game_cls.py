import pygame

from config import Config
from src.board_cls import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves()
        pygame.display.update()

    def _init(self):
        self.board = Board()
        self.selected = None
        self.turn = Config.BLACK
        self.valid_moves = {}

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if result is False:
                self.selected = None
                self.select(row, col)
        else:
            soldier = self.board.get_soldier(row, col)
            if soldier != 0 and soldier.color == self.turn:
                self.selected = soldier
                self.valid_moves = self.board.get_valid_moves(soldier)
                return True
            else:
                self.selected = None
                self.valid_moves = {}
        return False

    def draw_valid_moves(self):
        for move in self.valid_moves:
            row, col = move
            center = (
                col * Config.SQUARE_SIZE + Config.SQUARE_SIZE // 2, row * Config.SQUARE_SIZE + Config.SQUARE_SIZE // 2)
            pygame.draw.circle(self.win, color=Config.BLUE, center=center, radius=15)

    def _move(self, row, col):
        soldier = self.board.get_soldier(row, col)
        if self.selected and soldier == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
            return True
        return False

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == Config.BLACK:
            self.turn = Config.WHITE
        else:
            self.turn = Config.BLACK

    def reset(self):
        self._init()
