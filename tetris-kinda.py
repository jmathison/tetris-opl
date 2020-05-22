# Allows use of pygame functions
import pygame, sys, random, math
from pygame.locals import *

ROWS = 40
COLS = 10
TILE_SIZE = 20


# Create an empty board.
def clear_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]


board = clear_board()

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


def draw_ghost(pos, tetrimino, board_surface):

    top_x, top_y = pos
    rows = len(tetrimino)
    cols = len(tetrimino[0])

    for y in range(rows):
        for x in range(cols):
            tile_type = tetrimino[y][x]
            if tile_type != 0:
                tile_x = (top_x + x) * TILE_SIZE
                tile_y = (top_y + y) * TILE_SIZE
                draw_tile_ghost((tile_x, tile_y), tile_type, board_surface)



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

def draw_tile_ghost(pos, tile_type, surface):
    tile_color = pygame.Color(colors[tile_type])
    rect = Rect(pos, (TILE_SIZE, TILE_SIZE))

    # Draw the filled rect
    #pygame.draw.rect(surface, tile_color, rect)
    # Draw the grid border
    pygame.draw.rect(surface, tile_color, rect.inflate(1, 1), 3)


def collision_check(position, grid, tetrimino):
    top_x, top_y = position
    tetrimino_height = len(tetrimino)
    tetrimino_width = len(tetrimino[0])

    for y in range(tetrimino_height):
        for x in range(tetrimino_width):
            # No need to check blank spaces of the tetrimino for collision.
            if tetrimino[y][x] != 0:
                # out of bounds (walls or floor)
                if top_x + x < 0 or top_x + x >= COLS or top_y + y < 0 or top_y + y >= ROWS:
                    return True
                # Check vs grid
                if grid is not None and grid[top_y + y][top_x + x] != 0:
                    return True
    # If you make it out of this loop without returning True, you're in the clear.
    return False

# Basically the same scanning method as collision check, but instead of checking collisions, we'll copy the tetrimino values over.
def lock(position, grid, tetrimino):
    top_x, top_y = position
    tetrimino_height = len(tetrimino)
    tetrimino_width = len(tetrimino[0])

    for y in range(tetrimino_height):
        for x in range(tetrimino_width):
            # No need to check blank spaces of the tetrimino.
            # Should never be out of bounds since we only try to lock after a collision check.
            tile = tetrimino[y][x]
            if tile != 0:
                # print(tile)
                # print("setting " + str(top_x + x) + " " + str(top_y + y) + " to " + str(tile))
                # print(grid[top_y + y][top_x + x])
                grid[top_y + y][top_x + x] = tile


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

    return lines_cleared


def score_lines(lines_cleared):
    if 1 < lines_cleared < 4:
        lines_cleared += 2
    elif lines_cleared == 4:
        lines_cleared += 4
    return lines_cleared

def check_lock_out(position, grid, tetrimino):
    top_x, top_y = position
    tetrimino_height = len(tetrimino)
    tetrimino_width = len(tetrimino[0])

    out_of_bounds_y = 19
    max_y = 0

    for y in range(tetrimino_height):
        if not all(tetrimino[y]):
            # find the lowest row this block locked into
            max_y = top_y + y

    # if the lowest block was above our out of bounds cutoff, game over.
    return max_y <= out_of_bounds_y


# locations to check for wall kick rotations. Indexes 0-3 represent each possible rotation. List of tuples is the offsets to check for a valid rotation.
KICK_VALUES = [
    [
        (0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)
    ],
    [
        (0, 0), (1, 0), (1, -1), (0, 2), (1, 2)
    ],
    [
        (0, 0), (1, 0), (1, 1), (0, -2), (1, -2)
    ],
    [
        (0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)
    ]
]

KICK_VALUES_I = [
    [
        (0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)
    ],
    [
        (0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)
    ],
    [
        (0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)
    ],
    [
        (0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)
    ]
]


class Tetrimino:

    def __init__(self):
        self.type = "I"
        self.rotation = 0
        self.x, self.y = tetrimino_start

        # Set grid_ref manually - if left as none, blocks will fall and ignore the grid.
        self.grid_ref = None

    def reset(self):
        # TODO: Bag shuffle instead of random choice
        self.type = random.choice(types)
        self.rotation = 0
        self.x, self.y = tetrimino_start

    def move(self, dx, dy):
        destination_x = self.x + dx
        destination_y = self.y + dy
        if not collision_check((destination_x, destination_y), self.grid_ref, self.get_piece()):
            self.x = destination_x
            self.y = destination_y
            # move succeeded
            return True
        # move failed
        return False

    def rotate(self, dr):
        new_rotation = (self.rotation + dr) % len(pieces[self.type])
        # TODO: Wall kicks - currently rotation just fails if impossible.

        # If the block is an "I" we need to use the special kick values for I blocks
        kick_values = KICK_VALUES_I if self.type == "I" else KICK_VALUES

        # get the kick values for the current rotation
        kick_values_for_rotation = kick_values[self.rotation]
        for value in kick_values_for_rotation:
            # go through each kick value checking if any are a valid rotation destination.
            kick_x, kick_y = value
            kick_x *= dr
            kick_y *= dr
            pos = (self.x + kick_x, self.y + kick_y)
            if not collision_check(pos, self.grid_ref, pieces[self.type][new_rotation]):
                self.rotation = new_rotation
                self.x += kick_x
                self.y += kick_y
                # rotate succeeded
                return True

        # rotate failed
        return False

    # get position as a tuple
    def get_pos(self):
        return self.x, self.y

    # get the 2d array for the current tetrimino type and rotation.
    def get_piece(self):
        return pieces[self.type][self.rotation]


pygame.init()
clock = pygame.time.Clock()
FPS = 60

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Tetris, kinda")


# create a surface to draw the board on.
board_surface = pygame.Surface((COLS * TILE_SIZE, ROWS * TILE_SIZE))

tetrimino_start = (3, 18)

active_tetrimino = Tetrimino()
active_tetrimino.grid_ref = board
active_tetrimino.reset()

# spooky
ghost = Tetrimino()
ghost.grid_ref = board

# Delayed automatic scrolling - das_clock will track how many frames the move keys are held before scrolling starts.
# Change das_time to control how many frames before automatic scrolling starts.
das_clock = 0
das_time = 9
new_keypress = False

# Lock delay - how many frames before locking
lock_clock = 0
lock_delay = 30

# Infinite lock delay or Classic:
# Infinite (infinite_lock = True) - any successful move resets the lock counter.
# Classic (infinite_lock = False) - only a successful drop resets the counter.
infinite_lock = True

# Are we counting down to a lock?
locking = False

score = 0
level = 1
next_level = 5 * level

drop_clock = 0

# Calculations for drop time by level and soft drop speed taken from guidelines. We can simplify this if we want.
def calculate_drop_time(level):
    return math.floor(math.pow((0.8 - ((level - 1) * 0.007)), level-1) * 60)

def soft_drop_time(base_drop_time):
    return base_drop_time // 20

current_drop_time = base_drop_time = calculate_drop_time(level)

# Load a font to display score
font = pygame.font.Font(None, 24)

# game states
RESTART = -1
PLAYING = 0
GAME_OVER = 1

game_state = PLAYING

while True:
    while game_state == RESTART:
        board = clear_board()
        active_tetrimino = Tetrimino()
        active_tetrimino.grid_ref = board
        active_tetrimino.reset()
        score = 0
        level = 1
        next_level = 5 * level
        current_drop_time = base_drop_time = calculate_drop_time(level)
        game_state = PLAYING

    while game_state == PLAYING:
        # tick based on max fps
        clock.tick(FPS)

        moved = False
        rotated = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    new_keypress = True
                    das_clock = 0
                elif event.key == pygame.K_DOWN:
                    current_drop_time = soft_drop_time(base_drop_time)
                    # manual locking
                    if locking:
                        lock_clock = lock_delay
                elif event.key == pygame.K_UP or event.key == pygame.K_x:
                    rotated = active_tetrimino.rotate(1)
                elif event.key == pygame.K_z or event.key == pygame.K_RCTRL:
                    rotated = active_tetrimino.rotate(-1)
                elif event.key == pygame.K_SPACE:
                    # Hard drop. Move the block down instantly
                    while active_tetrimino.move(0,1):
                        pass
                    # Max out drop clock and lock clock to prepare to lock the block instantly.
                    drop_clock = current_drop_time
                    locking = True
                    lock_clock = lock_delay
                elif event.key == pygame.K_TAB:
                    active_tetrimino.reset()
            elif event.type == KEYUP:
                if event.key == pygame.K_DOWN:
                    current_drop_time = base_drop_time

        # Increase the drop clock each frame, once we pass current_drop_time, it's time to fall.
        drop_clock += 1
        if drop_clock >= current_drop_time:
            successful_fall = active_tetrimino.move(0, 1)
            if not successful_fall:
                # hit something while falling!
                # start the locking process
                if not locking:
                    locking = True
                    lock_clock = 0
            else:
                # If fall was successful, we're no longer locking.
                locking = False
            drop_clock = 0

        # if locking, increase the lock counter. when counter expires, lock it.
        if locking:
            lock_clock += 1
            print(lock_clock)
            if lock_clock >= lock_delay:

                lock(active_tetrimino.get_pos(), board, active_tetrimino.get_piece())
                lines_cleared = check_and_clear_lines(board)
                if lines_cleared > 0:
                    # Increase score based on lines cleared.
                    score += score_lines(lines_cleared)
                    if score >= next_level:
                        level += 1
                        next_level = 5 * level
                        base_drop_time = calculate_drop_time(level)

                # after lines cleared, check for a game over by first checking if the last locked piece was completely above the top line.
                game_over = check_lock_out(active_tetrimino.get_pos(), board, active_tetrimino.get_piece())

                # First drop after reset is instant, don't wait for drop clock.
                drop_clock = base_drop_time
                active_tetrimino.reset()
                # After resetting the piece, also check for game over if the spawned piece collided with anything.
                game_over = collision_check(active_tetrimino.get_pos(), board, active_tetrimino.get_piece())
                if game_over:
                    game_state = GAME_OVER
                    pass
                lock_clock = 0
                locking = False

        # Get all keys that are currently down
        keys_down = pygame.key.get_pressed()

        # DAS included to improve tapping vs. holding input feel.
        if keys_down[pygame.K_RIGHT]:
            das_clock += 1
            if das_clock >= das_time or new_keypress:
                moved = active_tetrimino.move(1, 0)
                new_keypress = False
        elif keys_down[pygame.K_LEFT]:
            das_clock += 1
            if das_clock >= das_time or new_keypress:
                moved = active_tetrimino.move(-1, 0)
                new_keypress = False

        # reset drop clock on successful move / rotate
        if infinite_lock and (moved or rotated):
            lock_clock = 0

        ghost.x = active_tetrimino.x
        ghost.y = active_tetrimino.y
        ghost.rotation = active_tetrimino.rotation
        ghost.type = active_tetrimino.type
        while ghost.move(0, 1):
            pass

        screen.fill(Color("gray"))

        draw_board(board, board_surface)
        draw_ghost(ghost.get_pos(), ghost.get_piece(), board_surface)
        draw_tetrimino(active_tetrimino.get_pos(), active_tetrimino.get_piece(), board_surface)

        draw_play_area((10, 10), screen, board_surface)

        score_surface = font.render("Lines: " + str(score), False, pygame.Color("black"))
        level_surface = font.render("Level: " + str(level), False, pygame.Color("black"))
        next_level_surface = font.render("Next Level: " + str(next_level), False, pygame.Color("black"))
        screen.blit(score_surface, (10 + board_surface.get_width() + 10, 10))
        screen.blit(level_surface, (10 + board_surface.get_width() + 10, 10 + font.get_linesize()))
        screen.blit(next_level_surface, (10 + board_surface.get_width() + 10, 10 + 2* font.get_linesize()))

        pygame.display.update()

    while game_state == GAME_OVER:
        # tick based on max fps
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = RESTART


        screen.fill(Color("red"))

        draw_board(board, board_surface)
        draw_tetrimino((active_tetrimino.x, active_tetrimino.y),
                       pieces[active_tetrimino.type][active_tetrimino.rotation], board_surface)

        draw_play_area((10, 10), screen, board_surface)

        score_surface = font.render("Lines: " + str(score), False, pygame.Color("white"))
        level_surface = font.render("Level: " + str(level), False, pygame.Color("white"))
        next_level_surface = font.render("Next Level: " + str(next_level), False, pygame.Color("white"))
        game_over_surface = font.render("Game over! Press Space to restart.", False, pygame.Color("white"))
        screen.blit(score_surface, (10 + board_surface.get_width() + 10, 10))
        screen.blit(level_surface, (10 + board_surface.get_width() + 10, 10 + font.get_linesize()))
        screen.blit(next_level_surface, (10 + board_surface.get_width() + 10, 10 + 2 * font.get_linesize()))
        screen.blit(game_over_surface, (10 + board_surface.get_width() + 10, 10 + 3 * font.get_linesize()))

        pygame.display.update()
