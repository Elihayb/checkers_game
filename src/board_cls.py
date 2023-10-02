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

    def remove(self, soldiers: list):
        for s in soldiers:
            self.board[s.row][s.col] = 0
            if s != 0:
                if s.color == Config.BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.black_left <= 0:
            return Config.WHITE
        elif self.white_left <= 0:
            return Config.BLACK
        else:
            return None

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
        soldier.move(row, col)
        if (row == Config.ROWS - 1 or row == 0) and soldier.is_king is False:
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

    def get_valid_moves(self, soldier):
        moves = {}
        left = soldier.col - 1
        right = soldier.col + 1
        row = soldier.row
        if soldier.color == Config.BLACK or soldier.is_king:
            moves.update(
                self._traverse_left(start=row - 1, stop=max(row - 3, -1), step=-1, color=soldier.color, left=left))
            moves.update(
                self._traverse_right(start=row - 1, stop=max(row - 3, -1), step=-1, color=soldier.color, right=right))
        if soldier.color == Config.WHITE or soldier.is_king:
            moves.update(self._traverse_left(start=row + 1, stop=min(row + 3, Config.ROWS), step=1, color=soldier.color,
                                             left=left))
            moves.update(
                self._traverse_right(start=row + 1, stop=min(row + 3, Config.ROWS), step=1, color=soldier.color,
                                     right=right))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, Config.ROWS)
                    moves.update(self._traverse_left(start=r + step, stop=row, step=step, left=left - 1, color=color,
                                                     skipped=last))
                    moves.update(
                        self._traverse_right(start=r + step, stop=row, step=step, right=left + 1, color=color,
                                             skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= Config.COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, Config.ROWS)
                    moves.update(self._traverse_left(start=r + step, stop=row, step=step, left=right - 1, color=color,
                                                     skipped=last))
                    moves.update(
                        self._traverse_right(start=r + step, stop=row, step=step, right=right + 1, color=color,
                                             skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves
