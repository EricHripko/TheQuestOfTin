import pygame.display
import pygame.image
import pygame.key
import pygame.sprite


class GravitySprite(pygame.sprite.Sprite):
    """
    Class that defines and facilitates the management of
    an gravity-affected sprites. Defines additional properties
    such as vertical speed and allows the gravity value to be
    changed. Also prevents the sprites from going out of the
    screen.
    """
    gravity = 0.25
    vy = 0

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
        if self.rect.left < 0:
            self.rect.x = 0
        if self.rect.top < 0:
            self.rect.y = 0
            self.reset()
        if self.rect.bottom > height:
            self.rect.y = height - self.rect.height
            self.reset()
        if self.rect.right > width:
            self.rect.x = width - self.rect.width

    def reset(self):
        """
        Reset the build-up of vertical velocity. Occurs when
        the sprite hits the ground and/or other obstacle that
        would make it stop in a real world.
        """
        self.vy = 0

    def update(self):
        # Update the speed and position of the sprite
        self.vy += self.gravity
        self.rect.y += self.vy
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

class Tin(AssetSprite):
    """
    Class that defines and facilitates the management of
    the game protagonist. Binds game input to the sprite states
    and its movement.
    """
    # How long the character has been jumping ofr
    jump = 0
    # Maximum jump actions in sequence
    jump_limit = 20

    def __init__(self):
        # Initialise the asset sprite
        super().__init__("Tin", "StandingRight")

    def reset(self):
        # Reset the jump counter when we hit a surface
        self.jump = 0
        # Base reset routine
        super().reset()

    def update(self):
        # Identify all the keys being currently pressed
        pressed_keys = pygame.key.get_pressed()
        # Rotate the sprite based on character's direction
        if pressed_keys[pygame.K_LEFT]:
            # Move left on left key press
            self.set_state("StandingLeft")
            self.rect.x -= 5
        if pressed_keys[pygame.K_RIGHT]:
            # Move right on right key press
            self.set_state("StandingRight")
            self.rect.x += 5
        if pressed_keys[pygame.K_SPACE]:
            # Process jump action on space
            if self.jump < self.jump_limit:
                self.rect.y -= 10
                self.jump += 1
        # Base update routine
        super().update()