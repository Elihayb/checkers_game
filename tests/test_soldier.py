"""Soldier class unit tests: constructor, position, king, movement, direction helpers."""
import pytest
from config import Config
from src.soldier_cls import Soldier


# ── constructor ────────────────────────────────────────────────────────────

def test_valid_white_soldier():
    s = Soldier(0, 1, Config.WHITE)
    assert s.color == Config.WHITE
    assert s.is_king is False

def test_valid_black_soldier():
    s = Soldier(7, 0, Config.BLACK)
    assert s.color == Config.BLACK
    assert s.is_king is False

def test_invalid_color_raises_value_error():
    with pytest.raises(ValueError):
        Soldier(0, 0, "GREEN")

def test_invalid_color_error_message():
    with pytest.raises(ValueError, match="Invalid square color"):
        Soldier(0, 0, "RED")


# ── position calculation ───────────────────────────────────────────────────

def test_calc_pos_origin():
    s = Soldier(0, 0, Config.WHITE)
    assert s.x == Config.SQUARE_SIZE // 2
    assert s.y == Config.SQUARE_SIZE // 2

def test_calc_pos_non_zero():
    s = Soldier(2, 3, Config.WHITE)
    assert s.x == Config.SQUARE_SIZE * 3 + Config.SQUARE_SIZE // 2
    assert s.y == Config.SQUARE_SIZE * 2 + Config.SQUARE_SIZE // 2


# ── king ───────────────────────────────────────────────────────────────────

def test_make_king_sets_flag():
    s = Soldier(3, 2, Config.BLACK)
    assert s.is_king is False
    s.make_king()
    assert s.is_king is True

def test_make_king_idempotent():
    s = Soldier(3, 2, Config.BLACK)
    s.make_king()
    s.make_king()
    assert s.is_king is True


# ── move ───────────────────────────────────────────────────────────────────

def test_move_updates_row_col():
    s = Soldier(2, 1, Config.WHITE)
    s.move(3, 0)
    assert s.row == 3
    assert s.col == 0

def test_move_recalculates_xy():
    s = Soldier(2, 1, Config.WHITE)
    s.move(3, 2)
    assert s.x == Config.SQUARE_SIZE * 2 + Config.SQUARE_SIZE // 2
    assert s.y == Config.SQUARE_SIZE * 3 + Config.SQUARE_SIZE // 2


# ── get_location ───────────────────────────────────────────────────────────

def test_get_location_returns_tuple():
    s = Soldier(5, 3, Config.BLACK)
    assert s.get_location() == (5, 3)

def test_get_location_none_raises():
    s = Soldier(0, 0, Config.WHITE)
    s.row = None
    with pytest.raises(ValueError):
        s.get_location()


# ── get_next_row_index ─────────────────────────────────────────────────────

def test_white_next_row_increases():
    assert Soldier(3, 3, Config.WHITE).get_next_row_index() == 4

def test_black_next_row_decreases():
    assert Soldier(4, 3, Config.BLACK).get_next_row_index() == 3

def test_next_row_custom_index():
    assert Soldier(3, 3, Config.WHITE).get_next_row_index(2) == 5


# ── get_next_column_index ──────────────────────────────────────────────────

def test_white_left_decreases_col():
    assert Soldier(3, 4, Config.WHITE).get_next_column_index(Config.LEFT) == 3

def test_white_right_increases_col():
    assert Soldier(3, 4, Config.WHITE).get_next_column_index(Config.RIGHT) == 5

def test_black_left_mirrors():
    assert Soldier(4, 4, Config.BLACK).get_next_column_index(Config.LEFT) == 5

def test_black_right_mirrors():
    assert Soldier(4, 4, Config.BLACK).get_next_column_index(Config.RIGHT) == 3

def test_invalid_direction_raises():
    with pytest.raises(ValueError):
        Soldier(3, 3, Config.WHITE).get_next_column_index("DIAGONAL")
