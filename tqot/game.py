import pygame
import pygame.font
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

# Create the font to be used for
font = pygame.font.SysFont("Helvetica", 32)

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
    # Update in-game objects or draw the end-game screen
    if not level.is_over():
        level.clear(screen, background)
        level.update()
        level.draw(screen)
    else:
        screen.blit(background, (0, 0))
        message = "The tower has fallen! You score is " + level.get_pretty_time() +  "!"
        label = font.render(message, 1, (255, 255, 255))
        x = (size[0] - label.get_width()) / 2
        y = (size[1] - label.get_height()) / 2
        screen.blit(label, (x, y))

        message = "Press any button to retry"
        label = font.render(message, 1, (255, 255, 255))
        x = (size[0] - label.get_width()) / 2
        y = (size[1] - label.get_height()) / 2 + 100
        screen.blit(label, (x, y))

    pygame.display.flip()
