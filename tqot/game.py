import pygame
import pygame.sprite
from tqot.environment import *

# Initialise the pygame software and hardware layers
pygame.init()

# Configure the screen
size = (1000, 480)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("The Quest of Tin")

# Create the game level
level = Level("SkyLand")

# Paint temporary background on the display
background = pygame.Surface(size).convert()
background.fill(level.definition.background)
screen.blit(background, (0, 0))

# Start the game loop with the maximum of 60 frames/sec
running = True
fps = 60
clock = pygame.time.Clock()
while running:
    clock.tick(fps)
    # Exit if requested
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update in-game objects
    level.clear(screen, background)
    level.update()
    level.draw(screen)

    pygame.display.flip()
