import pygame
# NEW: import locals from pygame
from pygame.locals import *

pygame.init()

# Colors
black = (0,0,0)
cyan = (0,255,255)
blue = (0,0,255)
orange = (255,100,10)
red = (255,0,0)
yellow = (255,255,0)
green = (0,255,0)
purple = (160,32,240)
gray = (190, 190, 190)
# NEW: Store colors as a list
colors = [black, cyan, blue, orange, yellow, green, purple, red]

#Variables for window and tiles
clock = pygame.time.Clock()
FPS = 60
WIDTH = 640
HEIGHT = 480
TILE_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# NEW: Draw board function
def draw_board(board, board_surface):
    for row in range(ROWS):
        for col in range(COLS):
            currentTile = board[row][col]
            tile_x = col * TILE_SIZE
            tile_y = row * TILE_SIZE
            draw_tile((tile_x, tile_y), currentTile, board_surface)

# NEW: Draw tile function
def draw_tile(position, tile, surface):
    tile_color = colors[tile]
    rect = Rect(position, (TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(surface, tile_color, rect)
    pygame.draw.rect(surface, gray, rect.inflate(1,1),1)

# NEW: draw play area
def draw_play_area(screen_position, screen_surface, board_surface):
    rows_toShow = 20.5
    topY = board_surface.get_height() - rows_toShow * TILE_SIZE
    screen_surface.blit(board_surface,screen_position, Rect((0, topY), (board_surface.get_width(), rows_toShow * TILE_SIZE)))

# NEW: Variables for board
ROWS = 40
COLS = 10
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
board_surface = pygame.Surface((COLS*TILE_SIZE, ROWS * TILE_SIZE))

# Game States
RESTART = -1
PLAYING = 0
GAME_OVER = 1
game_state = PLAYING

#Game Loop
while True:
    while game_state == PLAYING:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # NEW: Fill screen with gray, draw backdrop board and play area
        screen.fill(gray)
        draw_board(board, board_surface)
        draw_play_area((10,10), screen, board_surface)
        # DELETE: pygame.draw.rect(screen, purple, (WIDTH/2, HEIGHT/2, TILE_SIZE,TILE_SIZE))
        pygame.display.update()