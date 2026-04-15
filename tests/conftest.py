import os
import sys
import pytest

# Set headless drivers BEFORE pygame is imported anywhere.
# config.py calls pygame.image.load() at class-definition time, so pygame
# must already be in headless mode when any project module is first imported.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

# Ensure project root is on sys.path so bare imports like
# "from config import Config" work when pytest is invoked from any directory.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture(scope="session", autouse=True)
def pygame_session():
    """Initialize pygame once for the entire test session, headlessly."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def screen(pygame_session):
    """In-memory surface the size of the real game window."""
    return pygame.display.set_mode((800, 600))


@pytest.fixture
def clock(pygame_session):
    return pygame.time.Clock()


@pytest.fixture
def fresh_board(pygame_session):
    from src.board_cls import Board
    return Board()


@pytest.fixture
def fresh_game(screen, pygame_session):
    from src.game_cls import Game
    return Game(screen)
