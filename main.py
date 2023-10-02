import pygame

from config import Config
from src.game_cls import Game

WIN = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // Config.SQUARE_SIZE
    col = x // Config.SQUARE_SIZE
    return row, col


if __name__ == '__main__':
    game = Game(WIN)
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(Config.FPS)
        if game.board.winner() is not None:
            print(game.board.winner())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
        game.update()
    pygame.quit()
