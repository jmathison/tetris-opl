# Allows use of pygame functions
import pygame, sys, random
from pygame.locals import *

ROWS = 40
COLS = 10
TILE_SIZE = 20

board = [[0] * COLS] * ROWS

types = ["", "I", "J", "L", "O", "S", "T", "Z"]

# Can be color strings or hex colors
colors = ["black", "cyan", "blue", "orange", "yellow", "green", "purple", "red"]

# dict of pieces and their rotations. Key is tile type.
pieces = {
    "I": [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]
         ]
    ],
    "J": [
        [[2, 0, 0],
         [2, 2, 2],
         [0, 0, 0]],
        [[0, 2, 2],
         [0, 2, 0],
         [0, 2, 0]],
        [[0, 0, 0],
         [2, 2, 2],
         [0, 0, 2]],
        [[0, 2, 0],
         [0, 2, 0],
         [2, 2, 0]]
    ],
    "L": [
        [[0, 0, 3],
         [3, 3, 3],
         [0, 0, 0]],
        [[0, 3, 0],
         [0, 3, 0],
         [0, 3, 3]],
        [[0, 0, 0],
         [3, 3, 3],
         [3, 0, 0]],
        [[3, 3, 0],
         [0, 3, 0],
         [0, 3, 0]]
    ],
    "O": [
        [[0, 4, 4, 0],
         [0, 4, 4, 0],
         [0, 0, 0, 0]]
    ],
    "S": [
        [[0, 5, 5],
         [5, 5, 0],
         [0, 0, 0]],
        [[0, 5, 0],
         [0, 5, 5],
         [0, 0, 5]],
        [[0, 0, 0],
         [0, 5, 5],
         [5, 5, 0]],
        [[5, 0, 0],
         [5, 5, 0],
         [0, 5, 0]]
    ],
    "T": [
        [[0, 6, 0],
         [6, 6, 6],
         [0, 0, 0]],
        [[0, 6, 0],
         [0, 6, 6],
         [0, 6, 0]],
        [[0, 0, 0],
         [6, 6, 6],
         [0, 6, 0]],
        [[0, 6, 0],
         [6, 6, 0],
         [0, 6, 0]]
    ],
    "Z": [
        [[7, 7, 0],
         [0, 7, 7],
         [0, 0, 0]],
        [[0, 0, 7],
         [0, 7, 7],
         [0, 7, 0]],
        [[0, 0, 0],
         [7, 7, 0],
         [0, 7, 7]],
        [[0, 7, 0],
         [7, 7, 0],
         [7, 0, 0]]
    ]
}


def draw_grid(screen_pos, grid, screen_surface, board_surface):

    for y in range(ROWS):
        for x in range(COLS):
            tile_type = grid[y][x]
            tile_x = x * TILE_SIZE
            tile_y = y * TILE_SIZE
            draw_tile((tile_x, tile_y), tile_type, board_surface)

    rows_shown = 20.5

    top_y = board_surface.get_height() - rows_shown * TILE_SIZE
    screen.blit(board_surface, screen_pos, Rect((0, top_y), (board_surface.get_width(), rows_shown * TILE_SIZE)))


def draw_tile(pos, tile_type, surface):
    tile_color = pygame.Color(colors[tile_type])
    rect = Rect(pos, (TILE_SIZE, TILE_SIZE))

    # Draw the filled rect
    pygame.draw.rect(surface, tile_color,rect)
    # Draw the grid border
    pygame.draw.rect(surface, Color("gray"), rect.inflate(1, 1), 1)


pygame.init()
clock = pygame.time.Clock()
MAX_FPS = 60

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Tetris, kinda")


# create a surface to draw the board on.
board_surface = pygame.Surface((COLS * TILE_SIZE, ROWS * TILE_SIZE))


while True:
    # tick based on max fps, save time since last frame.
    delta_time = clock.tick(MAX_FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(Color("gray"))
    draw_grid((10, 10), board, screen, board_surface)

    pygame.display.update()

