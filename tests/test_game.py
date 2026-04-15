"""Game class tests: initial state, turn management, select, invalid moves, captures, reset."""
import pytest
from config import Config
from src.soldier_cls import Soldier


# ── helpers ────────────────────────────────────────────────────────────────

def _empty(game):
    for r in range(8):
        for c in range(8):
            game.board.board[r][c] = 0
    game.board.white_left = 0
    game.board.black_left = 0


def _place(game, soldier):
    game.board.board[soldier.row][soldier.col] = soldier
    if soldier.color == Config.WHITE:
        game.board.white_left += 1
    else:
        game.board.black_left += 1


# ── initial state ──────────────────────────────────────────────────────────

def test_initial_turn_is_black(fresh_game):
    assert fresh_game.turn == Config.BLACK

def test_initial_selected_is_none(fresh_game):
    assert fresh_game.selected is None

def test_initial_valid_moves_empty(fresh_game):
    assert fresh_game.valid_moves == {}


# ── turn management ────────────────────────────────────────────────────────

def test_change_turn_black_to_white(fresh_game):
    fresh_game.change_turn()
    assert fresh_game.turn == Config.WHITE

def test_change_turn_white_to_black(fresh_game):
    fresh_game.turn = Config.WHITE
    fresh_game.change_turn()
    assert fresh_game.turn == Config.BLACK

def test_change_turn_clears_valid_moves(fresh_game):
    fresh_game.valid_moves = {(3, 2): []}
    fresh_game.change_turn()
    assert fresh_game.valid_moves == {}

def test_successful_move_flips_turn(fresh_game):
    _empty(fresh_game)
    black = Soldier(4, 3, Config.BLACK)
    _place(fresh_game, black)
    fresh_game.turn = Config.BLACK
    fresh_game.select(4, 3)
    dest = next(iter(fresh_game.valid_moves))
    fresh_game.select(*dest)
    assert fresh_game.turn == Config.WHITE

def test_failed_move_does_not_flip_turn(fresh_game):
    _empty(fresh_game)
    _place(fresh_game, Soldier(4, 3, Config.BLACK))
    fresh_game.turn = Config.BLACK
    fresh_game.select(4, 3)
    fresh_game._move(0, 0)
    assert fresh_game.turn == Config.BLACK


# ── select ─────────────────────────────────────────────────────────────────

def test_select_empty_cell_returns_false(fresh_game):
    assert fresh_game.select(3, 3) is False

def test_select_wrong_color_returns_false(fresh_game):
    assert fresh_game.select(0, 1) is False   # WHITE piece on BLACK's turn

def test_select_correct_color_returns_true(fresh_game):
    assert fresh_game.select(5, 0) is True

def test_select_sets_selected(fresh_game):
    fresh_game.select(5, 0)
    assert fresh_game.selected is not None

def test_select_populates_valid_moves(fresh_game):
    fresh_game.select(5, 0)
    assert len(fresh_game.valid_moves) > 0


# ── invalid move rejection ─────────────────────────────────────────────────

def test_move_without_selection_returns_false(fresh_game):
    fresh_game.selected = None
    assert fresh_game._move(3, 2) is False

def test_move_to_occupied_cell_returns_false(fresh_game):
    _empty(fresh_game)
    _place(fresh_game, Soldier(4, 3, Config.BLACK))
    _place(fresh_game, Soldier(3, 2, Config.BLACK))
    fresh_game.turn = Config.BLACK
    fresh_game.select(4, 3)
    assert fresh_game._move(3, 2) is False

def test_move_to_non_valid_square_returns_false(fresh_game):
    _empty(fresh_game)
    _place(fresh_game, Soldier(4, 3, Config.BLACK))
    fresh_game.turn = Config.BLACK
    fresh_game.select(4, 3)
    assert fresh_game._move(0, 0) is False


# ── captures ───────────────────────────────────────────────────────────────

def _setup_capture(game):
    """BLACK at (4,3) can jump WHITE at (3,2) landing on (2,1)."""
    _empty(game)
    black = Soldier(4, 3, Config.BLACK)
    white = Soldier(3, 2, Config.WHITE)
    _place(game, black)
    _place(game, white)
    game.turn = Config.BLACK
    return black, white


def test_capture_removes_opponent_from_board(fresh_game):
    _setup_capture(fresh_game)
    fresh_game.select(4, 3)
    assert (2, 1) in fresh_game.valid_moves
    fresh_game.select(2, 1)
    assert fresh_game.board.board[3][2] == 0

def test_capture_decrements_opponent_count(fresh_game):
    _setup_capture(fresh_game)
    before = fresh_game.board.white_left
    fresh_game.select(4, 3)
    fresh_game.select(2, 1)
    assert fresh_game.board.white_left == before - 1

def test_capture_does_not_decrement_attacker_count(fresh_game):
    _setup_capture(fresh_game)
    before = fresh_game.board.black_left
    fresh_game.select(4, 3)
    fresh_game.select(2, 1)
    assert fresh_game.board.black_left == before

def test_capture_moves_attacker_to_landing_square(fresh_game):
    black, _ = _setup_capture(fresh_game)
    fresh_game.select(4, 3)
    fresh_game.select(2, 1)
    assert fresh_game.board.board[2][1] is black
    assert fresh_game.board.board[4][3] == 0

def test_capture_flips_turn(fresh_game):
    _setup_capture(fresh_game)
    fresh_game.select(4, 3)
    fresh_game.select(2, 1)
    assert fresh_game.turn == Config.WHITE

def test_winner_after_last_piece_removed(fresh_game):
    fresh_game.board.black_left = 1
    last = Soldier(5, 0, Config.BLACK)
    fresh_game.board.board[5][0] = last
    fresh_game.board.remove([last])
    assert fresh_game.board.winner() == Config.WHITE

def test_no_winner_while_both_have_pieces(fresh_game):
    assert fresh_game.board.winner() is None


# ── reset ──────────────────────────────────────────────────────────────────

def test_reset_restores_black_turn(fresh_game):
    fresh_game.change_turn()
    fresh_game.reset()
    assert fresh_game.turn == Config.BLACK

def test_reset_clears_selection(fresh_game):
    fresh_game.select(5, 0)
    fresh_game.reset()
    assert fresh_game.selected is None

def test_reset_restores_piece_counts(fresh_game):
    fresh_game.reset()
    assert fresh_game.board.white_left == 12
    assert fresh_game.board.black_left == 12
