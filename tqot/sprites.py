import pygame.image
import pygame.sprite


class AssetSprite(pygame.sprite.Sprite):
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
        # Load the associated art asset and setup the bounding rectangle
        self.image = pygame.image.load(self.get_asset()).convert_alpha()
        self.rect = self.image.get_rect()

    def get_asset(self):
        """
        Identify the relative path to the assets of the sprite.
        :return: Path as string.
        """
        return "../assets/" + self._name + "-" + self._state + ".png"