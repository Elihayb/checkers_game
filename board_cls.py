from copy import deepcopy

from soldier_cls import Soldier
from square_cls import Square
from types_cls import Types


class Board:
    SQUARE_ROW_NUM = 8

    def __init__(self):
        self.row_start_with_black = (Square(color=Types.BLACK), Square(color=Types.WHITE), Square(color=Types.BLACK),
                                     Square(color=Types.WHITE), Square(color=Types.BLACK), Square(color=Types.WHITE),
                                     Square(color=Types.BLACK), Square(color=Types.WHITE))
        self.row_start_with_white = (Square(color=Types.WHITE), Square(color=Types.BLACK), Square(color=Types.WHITE),
                                     Square(color=Types.BLACK), Square(color=Types.WHITE), Square(color=Types.BLACK),
                                     Square(color=Types.WHITE), Square(color=Types.BLACK))

        self.board = (
            # line 1
            deepcopy(self.row_start_with_white),
            # line 2
            deepcopy(self.row_start_with_black),
            # line 3
            deepcopy(self.row_start_with_white),
            # line 4
            deepcopy(self.row_start_with_black),
            # line 5
            deepcopy(self.row_start_with_white),
            # line 6
            deepcopy(self.row_start_with_black),
            # line 7
            deepcopy(self.row_start_with_white),
            # line 8
            deepcopy(self.row_start_with_black)
        )

    def init_start_game(self):
        for i in range(Board.SQUARE_ROW_NUM):
            for j in range(Board.SQUARE_ROW_NUM):
                self.board[i][j].set_location(x=i, y=j)
        for i in range(3):
            for j in range(Board.SQUARE_ROW_NUM):
                if self.board[i][j].color == Types.BLACK:
                    self.board[i][j].soldier = Soldier(color=Types.WHITE)
                    self.board[i][j].soldier.set_location(x=i, y=i)
        for i in range(5, Board.SQUARE_ROW_NUM):
            for j in range(Board.SQUARE_ROW_NUM):
                if self.board[i][j].color == Types.BLACK:
                    self.board[i][j].soldier = Soldier(color=Types.BLACK)
                    self.board[i][j].soldier.set_location(x=i, y=i)

    def move_soldier(self, old_square: Square, new_square: Square):
        self.validate_legal_move(old_square, new_square)
        new_square.soldier = old_square.soldier
        old_square.remove_soldier()

    @staticmethod
    def validate_legal_move(old_square: Square, new_square: Square) -> None:
        """
        Raises:
        ValueError:
        If any coordinate is out of range,
        the move is illegal - (more the one row or column),
        there's no soldier in old position,
        a soldier already exists in new position,
        a BLACK soldier is not moving down, a WHITE soldier is not moving up,
        or the new location is a WHITE square.
        :param old_square: The old square.
        :param new_square: The new square.
        :return: None
        """
        old_x, old_y = old_square.get_location()
        new_x, new_y = new_square.get_location()
        if abs(new_x - old_x) != 1 or abs(new_y - old_y) != 1:
            raise ValueError("The new location is illegal")
        if old_square.soldier is None:
            raise ValueError(f"There is no soldier in {old_x = }, {old_y = }")
        if new_square.soldier is not None:
            raise ValueError(f"There is soldier in {new_x =}, {new_y = }")
        if old_square.soldier.color == Types.BLACK:
            if old_x <= new_x:
                raise ValueError(f"The BLACK soldier must to move down. {old_x =} should be bigger than {new_x =}")
        else:
            if old_x >= new_x:
                raise ValueError(f"The WHITE soldier must to move up. {old_x =} should be smaller than {new_x =}")
        if new_square.color == Types.WHITE:
            raise ValueError("The new location is color WHITE - it is not possible to put soldier on WHITE square")

    @staticmethod
    def validate_coordinate_out_of_range(*params):
        for p in params:
            if p < 0 or p > Board.SQUARE_ROW_NUM:
                return False
        return True

    def eat_enemy(self, current_square, enemy_square):
        ...

    def get_enemy_for_eat(self, soldier: Soldier) -> list:
        enemies = []
        x, y = soldier.get_location()
        enemy_color = Types.WHITE if soldier.color == Types.BLACK else Types.BLACK
        right_col = y + 1
        left_col = y - 1
        if soldier.color == Types.WHITE:
            next_row = x + 1
            third_row = x + 2
        else:
            next_row = x - 1
            third_row = x - 2
        if self.validate_coordinate_out_of_range(next_row, third_row, right_col):
            if (self.board[next_row][right_col].soldier is not None
                    and self.board[next_row][right_col].soldier.color == enemy_color):
                enemies.append(self.board[next_row][right_col])
        if self.validate_coordinate_out_of_range(next_row, third_row, left_col):
            if (self.board[next_row][left_col].soldier is not None
                    and self.board[next_row][left_col].soldier.color == enemy_color):
                enemies.append(self.board[next_row][left_col])
        return enemies

    def __str__(self):
        string = ""
        for i in range(Board.SQUARE_ROW_NUM):
            for j in range(Board.SQUARE_ROW_NUM):
                string += f"{self.board[i][j]}"
                if j == Board.SQUARE_ROW_NUM - 1:
                    string += "\n"
        return string
