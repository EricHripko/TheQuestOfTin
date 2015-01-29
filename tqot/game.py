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

# Load the scores
scores = load_scores()

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
        # Store the high score
        if not level.multiplayer and (len(scores) == 0 or not level.get_time() in scores):
            scores.append(level.get_time())
            scores = list(reversed(sorted(scores)))
            save_scores(scores)

        if not level.multiplayer:
            # Display end-game message
            screen.blit(background, (0, 0))
            message = "The tower has fallen! Your score is " + level.get_pretty_time() + "!"
            label = font.render(message, 1, (255, 255, 255))
            x = (size[0] - label.get_width()) / 2
            y = (size[1] - label.get_height()) / 2 - 200
            screen.blit(label, (x, y))
        else:
            # Display end-game message
            screen.blit(background, (0, 0))
            message = "Sin has won! The darkness grows!" if level.player.is_dead()\
                                                        else "Tin has won! Nothing escapes the light!"
            label = font.render(message, 1, (255, 255, 255))
            x = (size[0] - label.get_width()) / 2
            y = (size[1] - label.get_height()) / 2 - 200
            screen.blit(label, (x, y))
        # Display progress message
        message = "Press R to retry or M for multi-player :)"
        label = font.render(message, 1, (255, 255, 255))
        x = (size[0] - label.get_width()) / 2
        y = (size[1] - label.get_height()) / 2 - 100
        screen.blit(label, (x, y))
        # Display the high scores
        message = "High scores:"
        label = font.render(message, 1, (255, 255, 255))
        x = (size[0] - label.get_width()) / 2
        y = (size[1] - label.get_height()) / 2
        screen.blit(label, (x, y))
        for i in range(0, min(3, len(scores))):
            message = "%d. %02d:%02d" % (i + 1,  (scores[i] // 60), (scores[i] % 60))
            label = font.render(message, 1, (255, 255, 255))
            x = (size[0] - label.get_width()) / 2
            y = (size[1] - label.get_height()) / 2 + 50 * (i + 1)
            screen.blit(label, (x, y))

        # Restart the level once finished
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_r]:
            screen.blit(background, (0, 0))
            level = Level("SkyLand")
        if pressed_keys[pygame.K_m]:
            screen.blit(background, (0, 0))
            level = Level("SkyLand", True)

    pygame.display.flip()
