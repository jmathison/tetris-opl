import pygame, sys

pygame.init()

#Colors
black = (0,0,0)
cyan = (0,255,255)
blue = (0,0,255)
orange = (255,100,10)
red = (255,0,0)
yellow = (255,255,0)
green = (0,255,0)
purple = (160,32,240)
gray = (190, 190, 190)

#Variables for window and tiles
clock = pygame.time.Clock()
FPS = 60
WIDTH = 640
HEIGHT = 480
TILE_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Game States
RESTART = -1
PLAYING = 0
GAME_OVER = 1
game_state = PLAYING

# Game Loop
while True:

    # Loop when player is playing the game
    while game_state == PLAYING:
        #60 Frames per second yeeee
        clock.tick(FPS)

        # Handle user input / events
        for event in pygame.event.get():
            # When user clicks on the X button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill screen with black, draw a rectangle, and update display
        screen.fill((0,0,0))
        pygame.draw.rect(screen, purple, (WIDTH/2, HEIGHT/2, TILE_SIZE,TILE_SIZE))
        pygame.display.update()