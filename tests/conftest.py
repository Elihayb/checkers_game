from pytest import fixture

from board_cls import Board


@fixture
def init_board():
    board = Board()
    board.init_start_game()
    return board
