# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Game

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requierments.txt  # note: filename has a typo

# Run the game
python main.py
```

> Note: `Config.CROWN` loads a pygame image at module import time (`config.py:13`), so `pygame.display` must be initialized before any import of `config`. The `main.py` entry point handles this correctly via `pygame.display.set_mode(...)` before creating the `Game`.

## Architecture

The game follows a 3-layer design:

```
main.py          — pygame event loop; translates mouse clicks to (row, col) and calls game.select()
src/game_cls.py  — Game: selection state, turn management, delegates drawing and move logic to Board
src/board_cls.py — Board: 8×8 grid (list of lists), valid-move calculation, king promotion, winner detection
src/soldier_cls.py — Soldier: piece position, color, king state, pixel coordinate calculation
config.py        — Single source of all constants (dimensions, colors, FPS, CROWN image)
```

### Key data conventions

- **Colors are strings**, not RGB tuples: `Config.BLACK = "BLACK"`, `Config.WHITE = "WHITE"`. Pygame accepts CSS color strings directly.
- **Empty squares are `0`** (integer), not `None`. All board iteration guards against `0` explicitly.
- **`get_valid_moves` returns** `{(row, col): [list_of_skipped_Soldier_objects]}`. An empty list means a plain (non-capture) move; a non-empty list means the pieces to remove after the move.
- `_traverse_left` / `_traverse_right` use a mutable default argument `skipped=[]` — be aware of this Python gotcha when modifying those methods.

### Move flow

1. `main.py` → `game.select(row, col)`
2. `Game.select` → `Board.get_valid_moves(soldier)` populates `self.valid_moves`
3. On a valid destination click → `Game._move` → `Board.move` (updates grid + promotes king) + `Board.remove` (removes captured pieces) + `Game.change_turn`

## Dependencies

`requierments.txt` (note typo) contains only `pygame==2.5.2`.

## Behavioral Instructions

- **Treat CLAUDE.md as a living document**: After completing any non-trivial task, suggest the user add lessons learned to this file. This includes: anti-patterns discovered, library/pattern preferences that emerged, directional choices ("we chose X over Y"), and "don't do this" rules to prevent future rework. Add them under the `## Lessons Learned / Do & Don't` section below.
- **Flag direction changes**: When the user redirects an implementation mid-task, after completing the task suggest: "Consider adding this preference to CLAUDE.md so future sessions and teammates follow the same direction."

## Lessons Learned / Do & Don't
<!-- Grow this section from real session experience. Add entries as: "DO: ...", "DON'T: ...", or "CHOSE X OVER Y BECAUSE: ..." -->