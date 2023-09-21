import pygame.draw

from config import Config


class Soldier:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        if color != Config.BLACK and color != Config.WHITE:
            raise ValueError("Invalid square color, Must be WHITE or BLACK")
        self.color = color
        self.is_king = False
        self.row = row
        self.col = col
        self.direction = 1 if Config.WHITE else -1
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = Config.SQUARE_SIZE * self.col + Config.SQUARE_SIZE // 2
        self.y = Config.SQUARE_SIZE * self.row + Config.SQUARE_SIZE // 2

    def make_king(self):
        self.is_king = True

    def draw(self, win):
        pygame.draw.circle(surface=win, color=self.color, center=(self.x, self.y),
                           radius=Config.SQUARE_SIZE // 2 - self.PADDING)
        if self.is_king:
            x = self.x - Config.CROWN.get_width() // 2
            y = self.y - Config.CROWN.get_height() // 2
            win.blit(Config.CROWN, (x, y))

    def move(self, new_row, new_col):
        self.row = new_row
        self.col = new_col
        self.calc_pos()

    def get_location(self):
        if self.row is None or self.col is None:
            raise ValueError("Location was not initialized")
        return self.row, self.col

    def get_next_row_index(self, index: int = 1):
        if self.row is None:
            raise ValueError("Location was not initialized")
        if self.color == Config.WHITE:
            return self.row + (1 * index)
        else:
            return self.row - (1 * index)

    def get_next_column_index(self, direction, index: int = 1):
        if self.col is None:
            raise ValueError("Location was not initialized")
        if direction not in [Config.LEFT, Config.RIGHT]:
            raise ValueError("The direction should be LEFT or RIGHT")
        if self.color == Config.WHITE:
            if direction == Config.LEFT:
                next_column = self.col - (1 * index)
            else:
                next_column = self.col + (1 * index)
        else:
            if direction == Config.LEFT:
                next_column = self.col + (1 * index)
            else:
                next_column = self.col - (1 * index)
        if 0 > next_column > Config.ROWS - 1:
            return -1
        else:
            return next_column

    def set_location(self, x, y):
        self.row = x
        self.col = y

    def __str__(self):
        return f"{self.color},{self.is_king = }"
