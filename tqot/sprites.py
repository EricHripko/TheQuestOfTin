import pygame.display
import pygame.image
import pygame.key
import pygame.sprite
from tqot.animation import *


class GravitySprite(pygame.sprite.Sprite):
    """
    Class that defines and facilitates the management of
    an gravity-affected sprites. Defines additional properties
    such as vertical speed and allows the gravity value to be
    changed. Also prevents the sprites from going out of the
    screen.
    """
    gravity = 3
    ground = 32

    def __init__(self):
        """
        Create and initialise a new gravity-affected sprite.
        :return: Initialised instance of the sprite.
        """
        # Initialise the sprite
        super().__init__()

    def check_bounds(self):
        """
        Check the sprite position and make sure it stays on
        the screen.
        """
        # Identify the size of the screen
        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()
        # Fix the sprite position
        if self.rect.right < 0:
            self.rect.x = width - self.rect.width
        if self.rect.top < 0:
            self.rect.y = 0
            self.reset()
        if self.rect.bottom > height - self.ground:
            self.rect.y = height - self.ground - self.rect.height
            self.reset()
        if self.rect.left > width:
            self.rect.x = 0

    def update(self):
        # Update the speed and position of the sprite
        self.rect.y += self.gravity
        # Fix position
        self.check_bounds()
        # Base update routine
        super().update()


class AssetSprite(GravitySprite):
    """
    Class that defines and facilitates the management of
    an asset-based sprite. Defines additional properties
    such as asset name, state and enables simple animations.
    """

    def __init__(self, name, initial_state="Default"):
        """
        Create and initialise a new asset-based sprite.
        :param name: Asset name.
        :param initial_state: Initial sprite state.
        :return: Initialised instance of the sprite.
        """
        # Initialise the sprite
        super().__init__()
        # Store its asset parameters
        self._name = name
        self._state = initial_state
        # Finish initialisation
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.reload_asset()

    def get_asset(self):
        """
        Identify the relative path to the assets of the sprite.
        :return: Path as a string.
        """
        return "../assets/" + self._name + "-" + self._state + ".png"

    def reload_asset(self):
        """
        Reload the associated art asset and update its bounding rectangle.
        """
        self.image = pygame.image.load(self.get_asset()).convert_alpha()
        # Preserve the position of the sprite when updating the bounding box
        (x, y) = (self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = (x, y)

    def get_state(self):
        """
        Retrieve the state of the sprite.
        :return: State as a string.
        """
        return self._state

    def set_state(self, state):
        """
        Update the state of the sprite.
        :param state: New state.
        """
        # If state was changed, we need to reload the art asset
        invalidated = self._state != state
        self._state = state
        if invalidated:
            self.reload_asset()


class LookerSprite(AssetSprite):
    """
    Class that defines and manages a looker sprite. This sprite
    will be tracking the position of the given parent and change
    its state to either turn right or left based on the situation.
    """
    # Parent sprite that this looker will look at
    parent = None

    def __init__(self, parent, name, initial_state="Default"):
        """
        Create and initialise a new asset-based looker sprite.
        :param parent: Parent sprite that the looker will be focused on.
        :param name: Asset name.
        :param initial_state: Initial sprite state.
        :return: Initialised instance of the sprite.
        """
        # Store the link to the parent sprite
        self.parent = parent
        # Initialise the asset sprite
        super().__init__(name, initial_state)

    def update(self):
        if self.parent.rect.x > self.rect.x:
            self.set_state("StandingRight")
        else:
            self.set_state("StandingLeft")
        # Do not do base update routine
        # super().update()


class Tin(AssetSprite):
    """
    Class that defines and facilitates the management of
    the game protagonist. Binds game input to the sprite states
    and its movement.
    """
    ASSET_NAME = "Tin"
    # How long the character has been jumping for
    jump = 0
    # Maximum jump actions in sequence
    jump_limit = 20

    def __init__(self):
        # Initialise the asset sprite
        super().__init__(Tin.ASSET_NAME, "StandingRight")
        # Setup the animations
        self.runRight = Animation(self)
        self.runRight.add_frame("StandingRight", 50)
        self.runRight.add_frame("MovingRight", 50)
        self.runRight.add_frame("MovingRight2", 50)
        self.runLeft = Animation(self)
        self.runLeft.add_frame("StandingLeft", 50)
        self.runLeft.add_frame("MovingLeft", 50)
        self.runLeft.add_frame("MovingLeft2", 50)

    def collision(self, sprite):
        """
        Method invoked when the character collides with environment.
        Prevents the character from falling through the platforms.
        :param sprite: Sprite that character collided with.
        """
        # If character is above the platform, prevent falling down
        if self.rect.bottom - 5 <= sprite.rect.y:
            if abs(self.rect.bottom - sprite.rect.top) > 2:
                self.rect.bottom = sprite.rect.top
            self.reset()

    def reset(self):
        # Reset the jump counter when we hit a surface
        self.jump = 0

    def update(self):
        # Identify all the keys being currently pressed
        pressed_keys = pygame.key.get_pressed()
        # Rotate the sprite based on character's direction
        if pressed_keys[pygame.K_LEFT]:
            # Move left on left key press
            self.runRight.stop()
            self.runLeft.play()
            self.rect.x -= 5
        if pressed_keys[pygame.K_RIGHT]:
            # Move right on right key press
            self.runLeft.stop()
            self.runRight.play()
            self.rect.x += 5
        if pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_UP]:
            # Process jump action on space
            if self.jump < self.jump_limit:
                self.rect.y -= 10
                self.jump += 1
        if not pressed_keys[pygame.K_LEFT] and not pressed_keys[pygame.K_RIGHT]:
            # Stop moving when nothing is pressed
            self.runLeft.stop()
            self.runRight.stop()
        # Base update routine
        super().update()