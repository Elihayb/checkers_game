"""Board class tests: initial state, move, king promotion, remove, winner, valid moves."""
import pytest
from config import Config
from src.board_cls import Board
from src.soldier_cls import Soldier


# ── initial state ──────────────────────────────────────────────────────────

def test_initial_white_piece_count(fresh_board):
    assert fresh_board.white_left == 12

def test_initial_black_piece_count(fresh_board):
    assert fresh_board.black_left == 12

def test_board_is_8x8(fresh_board):
    assert len(fresh_board.board) == 8
    for row in fresh_board.board:
        assert len(row) == 8

def test_white_pieces_in_top_three_rows(fresh_board):
    for row in range(3):
        for col in range(Config.COLS):
            cell = fresh_board.board[row][col]
            if cell != 0:
                assert cell.color == Config.WHITE

def test_black_pieces_in_bottom_three_rows(fresh_board):
    for row in range(5, 8):
        for col in range(Config.COLS):
            cell = fresh_board.board[row][col]
            if cell != 0:
                assert cell.color == Config.BLACK

def test_middle_rows_are_empty(fresh_board):
    for row in range(3, 5):
        for col in range(Config.COLS):
            assert fresh_board.board[row][col] == 0

def test_total_24_pieces_at_start(fresh_board):
    count = sum(
        1 for r in range(8) for c in range(8)
        if fresh_board.board[r][c] != 0
    )
    assert count == 24


# ── move ───────────────────────────────────────────────────────────────────

def test_move_updates_destination_cell(fresh_board):
    soldier = fresh_board.get_soldier(2, 1)
    fresh_board.move(soldier, 3, 0)
    assert fresh_board.get_soldier(3, 0) is soldier

def test_move_clears_source_cell(fresh_board):
    soldier = fresh_board.get_soldier(2, 1)
    fresh_board.move(soldier, 3, 0)
    assert fresh_board.get_soldier(2, 1) == 0

def test_move_updates_soldier_row_col(fresh_board):
    soldier = fresh_board.get_soldier(2, 1)
    fresh_board.move(soldier, 3, 0)
    assert soldier.row == 3
    assert soldier.col == 0

def test_move_non_soldier_does_not_crash(fresh_board):
    fresh_board.move(0, 3, 3)
    assert fresh_board.white_left == 12
    assert fresh_board.black_left == 12


# ── king promotion ─────────────────────────────────────────────────────────

def test_white_soldier_becomes_king_at_row_7(fresh_board):
    soldier = Soldier(row=6, col=1, color=Config.WHITE)
    fresh_board.board[6][1] = soldier
    fresh_board.move(soldier, 7, 0)
    assert soldier.is_king is True
    assert fresh_board.white_king == 1

def test_black_soldier_becomes_king_at_row_0(fresh_board):
    soldier = Soldier(row=1, col=2, color=Config.BLACK)
    fresh_board.board[1][2] = soldier
    fresh_board.move(soldier, 0, 1)
    assert soldier.is_king is True
    assert fresh_board.black_kings == 1

def test_soldier_not_crowned_in_mid_board(fresh_board):
    soldier = fresh_board.get_soldier(2, 1)
    fresh_board.move(soldier, 3, 0)
    assert soldier.is_king is False


# ── remove ─────────────────────────────────────────────────────────────────

def test_remove_decrements_white(fresh_board):
    soldier = fresh_board.get_soldier(0, 1)
    fresh_board.remove([soldier])
    assert fresh_board.white_left == 11

def test_remove_decrements_black(fresh_board):
    soldier = fresh_board.get_soldier(5, 0)
    fresh_board.remove([soldier])
    assert fresh_board.black_left == 11

def test_remove_clears_cell(fresh_board):
    soldier = fresh_board.get_soldier(0, 1)
    row, col = soldier.row, soldier.col
    fresh_board.remove([soldier])
    assert fresh_board.board[row][col] == 0

def test_remove_multiple_soldiers(fresh_board):
    s1 = fresh_board.get_soldier(0, 1)
    s2 = fresh_board.get_soldier(0, 3)
    fresh_board.remove([s1, s2])
    assert fresh_board.white_left == 10


# ── winner ─────────────────────────────────────────────────────────────────

def test_no_winner_at_start(fresh_board):
    assert fresh_board.winner() is None

def test_white_wins_when_black_left_zero(fresh_board):
    fresh_board.black_left = 0
    assert fresh_board.winner() == Config.WHITE

def test_black_wins_when_white_left_zero(fresh_board):
    fresh_board.white_left = 0
    assert fresh_board.winner() == Config.BLACK

def test_no_winner_when_one_piece_each(fresh_board):
    fresh_board.white_left = 1
    fresh_board.black_left = 1
    assert fresh_board.winner() is None


# ── valid moves ────────────────────────────────────────────────────────────

def test_valid_moves_not_empty_for_open_piece(fresh_board):
    soldier = fresh_board.get_soldier(2, 1)
    assert len(fresh_board.get_valid_moves(soldier)) > 0

def test_valid_moves_land_on_empty_cells(fresh_board):
    soldier = fresh_board.get_soldier(2, 1)
    for (r, c) in fresh_board.get_valid_moves(soldier):
        assert fresh_board.get_soldier(r, c) == 0

def test_king_can_move_in_both_directions(fresh_board):
    b = Board()
    for r in range(8):
        for c in range(8):
            b.board[r][c] = 0
    king = Soldier(4, 4, Config.BLACK)
    king.make_king()
    b.board[4][4] = king
    rows = {r for (r, _) in b.get_valid_moves(king)}
    assert any(r < 4 for r in rows)
    assert any(r > 4 for r in rows)

def test_capture_move_includes_skipped_soldier(fresh_board):
    b = Board()
    for r in range(8):
        for c in range(8):
            b.board[r][c] = 0
    b.white_left = b.black_left = 0
    black = Soldier(4, 3, Config.BLACK)
    white = Soldier(3, 2, Config.WHITE)
    b.board[4][3] = black
    b.board[3][2] = white
    b.black_left = b.white_left = 1
    moves = b.get_valid_moves(black)
    assert (2, 1) in moves
    assert white in moves[(2, 1)]
