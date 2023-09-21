from src.board_cls import Board
import pygame

from config import Config

WIN = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // Config.SQUARE_SIZE
    col = x // Config.SQUARE_SIZE
    return row, col


if __name__ == '__main__':
    board = Board()
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(Config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                soldier = board.get_soldier(row, col)
                board.move(soldier=soldier, row=4, col=3)
        board.draw(WIN)
        pygame.display.update()
    pygame.quit()
