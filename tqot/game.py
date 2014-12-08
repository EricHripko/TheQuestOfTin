import pygame
import pygame.sprite
from tqot.sprites import *

# Initialise the pygame software and hardware layers
pygame.init()

# Configure the screen
size = (640, 480)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("The Quest of Tin")

# Paint temporary background on the display
background = pygame.Surface(size).convert()
background.fill((0xCC, 0xCC, 0xCC))
screen.blit(background, (0, 0))

# Characters to be drawn on the screen
chars = pygame.sprite.Group()

# Create the protagonist
tin = Tin()
olivia = LookerSprite(tin, "Olivia", "StandingRight")
olivia.rect.x = 300
chars.add(tin)
chars.add(olivia)

# Start the game loop with the maximum of 60 frames/sec
running = True
fps = 60
clock = pygame.time.Clock()
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update in-game objects
    chars.clear(screen, background)
    chars.update()
    chars.draw(screen)

    pygame.display.flip()
