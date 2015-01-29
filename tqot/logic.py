import json
import pygame.display
import random


class Damageable:
    """
    Class that defines a logic for damageable and,
    as a result, kill-able creature.
    """
    def __init__(self):
        """
        Create a new damageable creature.
        :return: Damageable creature.
        """
        self.current = 0
        self.maximum = 0

    def set_health(self, current, maximum):
        """
        Set the new values for the creature health.
        :param current: Current creature health.
        :param maximum: Maximum creature health.
        """
        self.current = current
        self.maximum = maximum

    def character_attacked(self):
        """
        Callback for when the character is attacked.
        """
        pass

    def is_dead(self):
        return self.current <= 0


class SpawnerManager:
    """
    Class that defines the spawner manager and
    is able to position the sprites for the game.
    """
    def __init__(self, heights):
        # Identify and save the size of the screen
        surface = pygame.display.get_surface()
        width = surface.get_width()
        self.screen_width = width
        # Store the heights at which the monsters can be spawned
        self.heights = heights

    def set_location(self, sprite):
        """
        Randomise the position for the sprite.
        :param sprite: Sprite position.
        """
        # Identify y coordinate
        sprite.rect.y = random.choice(self.heights)
        x = random.getrandbits(1) or self.screen_width
        if x > 1:
            sprite.rect.left = x
        else:
            sprite.rect.right = x


def load_scores():
    """
    Load the high scores from the file.
    :return: High scores.
    """
    try:
        with open("scores.json", "r") as file:
            return json.load(file)
    except:
        return []


def save_scores(scores):
    """
    Save the high scores to the file.
    :param scores: Maximum scores.
    """
    with open("scores.json", "w") as file:
        json.dump(scores, file)