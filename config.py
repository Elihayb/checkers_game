import pygame.image


class Config:
    FPS = 30
    WIDTH = HEIGHT = 800
    ROWS = COLS = 8
    SQUARE_SIZE = WIDTH // COLS
    BLUE = "BLUE"
    WHITE = "WHITE"
    BLACK = "BLACK"
    RED = "RED"
    CROWN = pygame.transform.scale(pygame.image.load("assets/crown.png"), size=(35, 35))
    LEFT = "LEFT"
    RIGHT = "RIGHT"
