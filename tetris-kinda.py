# Allows use of pygame functions
import pygame, sys, random
from pygame.locals import *

ROWS = 40
COLS = 10
TILE_SIZE = 20

board = [[0] * COLS] * ROWS

types = ["I", "J", "L", "O", "S", "T", "Z"]

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


def draw_board(grid, board_surface):

    # Draw the board
    for y in range(ROWS):
        for x in range(COLS):
            tile_type = grid[y][x]
            tile_x = x * TILE_SIZE
            tile_y = y * TILE_SIZE
            draw_tile((tile_x, tile_y), tile_type, board_surface)


def draw_tetrimino(pos, tetrimino, board_surface):

    top_x, top_y = pos
    rows = len(tetrimino)
    cols = len(tetrimino[0])

    for y in range(rows):
        for x in range(cols):
            tile_type = tetrimino[y][x]
            if tile_type != 0:
                tile_x = (top_x + x) * TILE_SIZE
                tile_y = (top_y + y) * TILE_SIZE
                draw_tile((tile_x, tile_y), tile_type, board_surface)



def draw_play_area(screen_pos, screen_surface, board_surface):
    # how many rows show of the play area. 20.5 shows half of 21 so players can see new blocks fall into play.
    rows_shown = 20.5

    top_y = board_surface.get_height() - rows_shown * TILE_SIZE
    screen_surface.blit(board_surface, screen_pos, Rect((0, top_y), (board_surface.get_width(), rows_shown * TILE_SIZE)))


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

tetrimino_start = (3, 18)
tetrimino_x, tetrimino_y = tetrimino_start

tetrimino_type = "J"
tetrimino_rotation = 0

tetrimino = pieces["J"][0]


drop_clock = 0
drop_time = 30

das_clock = 0
das_time = 9
new_keypress = False

while True:
    # tick based on max fps, save time since last frame.
    delta_time = clock.tick(MAX_FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                new_keypress = True
                das_clock = 0
            elif event.key == pygame.K_SPACE:
                #rotation
                tetrimino_rotation += 1
                tetrimino_rotation %= len(pieces[tetrimino_type])
                tetrimino = pieces[tetrimino_type][tetrimino_rotation]
            elif event.key == pygame.K_LSHIFT:
                tetrimino_rotation -= 1
                tetrimino_rotation %= len(pieces[tetrimino_type])
                tetrimino = pieces[tetrimino_type][tetrimino_rotation]
            elif event.key == pygame.K_TAB:
                tetrimino_type = random.choice(types)
                tetrimino_rotation = 0
                tetrimino_x, tetrimino_y = tetrimino_start
                tetrimino = pieces[tetrimino_type][tetrimino_rotation]

    drop_clock += 1
    if drop_clock >= drop_time:
        tetrimino_y += 1
        drop_clock = 0

    # Get all keys that are currently down
    keys_down = pygame.key.get_pressed()

    # DAS included to improve tapping vs. holding input feel.
    if keys_down[pygame.K_RIGHT]:
        das_clock += 1
        if das_clock >= das_time or new_keypress:
            tetrimino_x += 1
            new_keypress = False
    elif keys_down[pygame.K_LEFT]:
        das_clock += 1
        if das_clock >= das_time or new_keypress:
            tetrimino_x -= 1
            new_keypress = False


    screen.fill(Color("gray"))

    draw_board(board, board_surface)
    draw_tetrimino((tetrimino_x, tetrimino_y), tetrimino, board_surface)

    draw_play_area((10, 10), screen, board_surface)

    pygame.display.update()

