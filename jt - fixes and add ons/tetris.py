import pygame, math
from pygame.locals import *
from tetris_pieces import *

pygame.init()
# NEW
pygame.font.init()

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
colors = [black, cyan, blue, orange, yellow, green, purple, red]

# Variables for window and tiles
clock = pygame.time.Clock()
FPS = 60
WIDTH = 640
HEIGHT = 480
TILE_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
# NEW: creates formatting for pygame font, 1st param is font style, second is font size
font_format = pygame.font.SysFont('comicsansms', 60)


def draw_board(board, board_surface):
    for row in range(ROWS):
        for col in range(COLS):
            currentTile = board[row][col]
            tile_x = col * TILE_SIZE
            tile_y = row * TILE_SIZE
            draw_tile(tile_x, tile_y, currentTile, board_surface)


def draw_tile(posX, posY, tile, surface):
    tile_color = colors[tile]
    rect = Rect((posX,posY), (TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(surface, tile_color, rect)
    pygame.draw.rect(surface, gray, rect.inflate(1,1),1)


def draw_play_area(screen_position, screen_surface, board_surface):
    rows_toShow = 20.5
    topY = board_surface.get_height() - rows_toShow * TILE_SIZE
    screen_surface.blit(board_surface,screen_position, Rect((0, topY), (board_surface.get_width(), rows_toShow * TILE_SIZE)))

def draw_tetrimino(posX,posY, tetrimino, board_surface):
    topX = posX
    topY = posY
    rows = len(tetrimino)
    cols = len(tetrimino[0])

    for row in range(rows):
        for col in range(cols):
            tile = tetrimino[row][col]
            if tile != 0: # tile is not black
                tileX = (topX + col) * TILE_SIZE
                tileY = (topY + row) * TILE_SIZE
                draw_tile(tileX, tileY, tile, board_surface)


def calculate_drop_time(level):
    return math.floor(math.pow((0.8 - ((level - 1) * 0.007)), level-1) * 60)

# NEW: taken from Jon code, will be used to create a faster drop speed for tetris piece when holding down key
def soft_drop_time(baseDropTime):
    return baseDropTime // 20

# Basically the same scanning method as collision check, but instead of checking collisions, we'll copy the tetrimino values over.
def lock(posX, posY, grid, tetrimino):
    top_x, top_y = posX, posY
    tetrimino_height = len(tetrimino)
    tetrimino_width = len(tetrimino[0])
    for y in range(tetrimino_height):
        for x in range(tetrimino_width):
            # No need to check blank spaces of the tetrimino.
            # Should never be out of bounds since we only try to lock after a collision check.
            tile = tetrimino[y][x]
            if tile != 0:
                grid[top_y + y][top_x + x] = tile

# Add method for checking if we need to clear a line after the piece is locked into place
def check_and_clear_lines(grid):
    lines_cleared = 0

    # list to keep track of which lines we need to pull out
    full_lines = []
    for y, line in enumerate(grid):
        if 0 not in line:
            # if there's no 0 in the line, then it's cleared
            lines_cleared += 1
            # add to the list for later
            full_lines.append(y)

    if lines_cleared > 0:
        for y in full_lines:
            # remove the element at index y.
            grid.pop(y)
            # insert a new empty row at the top.
            grid.insert(0, [0 for _ in range(COLS)])

# NEW: from Jon's code, will use to clear board for a restart
def clear_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

level = 1
score = 0
new_level = 5 * level
drop_clock = 0
currentDropTime = baseDropTime = calculate_drop_time(level)


# Variables for board
ROWS = 40
COLS = 10
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
board_surface = pygame.Surface((COLS*TILE_SIZE, ROWS * TILE_SIZE))

# variables for locking pieces
locking = False
lock_clock = 0
lock_delay = 30

# Game States
RESTART = -1
PLAYING = 0
GAME_OVER = 1
game_state = PLAYING

# Create first tetrimino
active_tetrimino = Tetrimino()
active_tetrimino.grid_ref = board
active_tetrimino.reset()

#Game Loop
while True:
    while game_state == PLAYING:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    active_tetrimino.move(1,0)
                elif event.key == pygame.K_LEFT:
                    active_tetrimino.move(-1,0)
                # NEW: from Jon code, implementing down key, will make base drop time increase when down key pushed
                elif event.key == pygame.K_DOWN:
                    currentDropTime = soft_drop_time(baseDropTime)
                elif event.key == pygame.K_UP or event.key == pygame.K_x:
                    active_tetrimino.rotate(1)
                elif event.key == pygame.K_z or event.key == pygame.K_RCTRL:
                    active_tetrimino.rotate(-1)
            #NEW: from Jon code, will set current drop time back to base drop time once key is let go of
            elif event.type == KEYUP:
                if event.key == pygame.K_DOWN:
                    currentDropTime = baseDropTime


        # Increase the drop clock each frame, once we pass current_drop_time, it's time to fall.
        drop_clock += 1
        if drop_clock >= currentDropTime:
            move = active_tetrimino.move(0, 1)
            # determine if something moved and check to see if we need to lock the piece
            if not move:
                #we hit something!
                if not locking:
                    locking = True
                    lock_clock = 0
            else:
                # no longer locking
                locking = False
            drop_clock = 0

        #Check for locking
        if locking:
            lock_clock += 1
            if lock_clock >= lock_delay:
                lock(active_tetrimino.x, active_tetrimino.y, board, pieces[active_tetrimino.type][active_tetrimino.rotation])
                drop_clock = baseDropTime
                active_tetrimino.reset()

                # NEW: adjusted from what Jon had to account for our collision checker being inside our class
                # will check for game over if active_tetrimino has collided with edge or another piece after reset
                game_over = active_tetrimino.collision_check(active_tetrimino.x, active_tetrimino.y)
                if game_over:
                    game_state = GAME_OVER
                    pass

                lock_clock = 0
                locking = False
                check_and_clear_lines(board)

        screen.fill(gray)
        draw_board(board, board_surface)


        # drawing to the board
        draw_tetrimino(active_tetrimino.x, active_tetrimino.y, pieces[active_tetrimino.type][active_tetrimino.rotation],board_surface)
        draw_play_area((10,10), screen, board_surface)

        pygame.display.update()

    # NEW: loop that will run while game state is equal to a game over
    while game_state == GAME_OVER:
        clock.tick(FPS)

        # NEW: event handler that will restart game when enter/return hit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # NEW: resetting all values to create a new game, from Jon's code, just in different place
                    board = clear_board()
                    active_tetrimino = Tetrimino()
                    active_tetrimino.grid_ref = board
                    active_tetrimino.reset()
                    score = 0
                    level = 1
                    next_level = 5 * level
                    current_drop_time = base_drop_time = calculate_drop_time(level)
                    game_state = PLAYING

        screen.fill(black)

        # NEW: Rendering text, will essentially "create" text with given colors
        text_gameover = font_format.render("GAME OVER!", 75, red)
        text_restart = font_format.render("RESTART", 75, gray)

        # NEW: gets rectangles around text, will use this rectangle to place text
        gameover_rect = text_gameover.get_rect()
        restart_rect = text_restart.get_rect()

        # NEW: place text on screen: text, x (equation to get to center of screen), y
        screen.blit(text_gameover, (WIDTH / 2 - (gameover_rect[2] / 2), 150))
        screen.blit(text_restart, (WIDTH / 2 - (restart_rect[2] / 2), 350))

        pygame.display.update()