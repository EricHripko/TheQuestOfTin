import pygame
import pygame.sprite
from tqot.sprites import *


class LevelReader:
    """
    Class that enables the game to read in and interpret
    the level definition file.
    """
    BACKGROUND = 0
    GROUND_LEVEL = 1
    PLATFORMS = 2
    LEVEL = 3
    EXIT = 4

    def __init__(self, name):
        """
        Create and initialise a new level reader.
        :param name: Asset name.
        :return: Initialised instance of the reader.
        """
        # Store the asset name
        self.name = name
        # Initialise the properties
        self.background = (0, 0, 0)
        self.ground_level = ""
        self.platforms = {}
        self.level = []
        # Setup the default state of the reader
        self.state = LevelReader.BACKGROUND
        # Read the level in
        self.read()

    def read(self):
        """
        Read the level in from the file.
        """
        with open(self.get_asset(), "r") as file:
            while True:
                line = file.readline().rstrip("\n")
                # Skip comments
                if line.startswith("$"):
                    continue
                # Background is a tuple with elements separated by spaces
                if self.state == LevelReader.BACKGROUND:
                    self.background = tuple([int(x) for x in line.split(" ")])
                    self.state += 1
                    continue
                # Ground level is the name of the asset
                if self.state == LevelReader.GROUND_LEVEL:
                    self.ground_level = line
                    self.state += 1
                    continue
                # Skip the ceiling of the level
                if line.startswith("##"):
                    self.state += 1
                    continue
                # Platforms definitions
                if self.state == LevelReader.PLATFORMS:
                    [symbol, name] = line.split(" ")
                    self.platforms[symbol] = name
                    continue
                # Read the level in
                if self.state == LevelReader.LEVEL:
                    # Get rid of side maps
                    line = line[1:-1]
                    level = []
                    platform = ""
                    size = 1
                    for x in range(len(line)):
                        if not(line[x] in self.platforms):
                            if platform != "":
                                level.append((x - size + 1, size, self.platforms[platform]))
                                platform = ""
                            continue
                        if platform != line[x]:
                            platform = line[x]
                            size = 1
                        else:
                            size += 1

                    if platform != "":
                        level.append((x - size + 1, size, self.platforms[platform]))
                        platform = ""
                    self.level.insert(0, level)
                    continue
                # Stop the reader loop
                if self.state == LevelReader.EXIT:
                    break

    def get_asset(self):
        """
        Identify the relative path to the assets of the map.
        :return: Path as a string.
        """
        return "../assets/" + self.name + ".level"


class EnvironmentSprite(pygame.sprite.Sprite):
    """
    Class that defines and facilitates the management of
    an asset-based environment sprite. Defines additional
    properties such as asset name.
    """

    def __init__(self, name):
        """
        Create and initialise a new asset-based sprite.
        :param name: Asset name.
        :return: Initialised instance of the sprite.
        """
        # Store the asset name
        self.name = name
        # Load the associated art asset
        self.image = pygame.image.load(self.get_asset()).convert_alpha()
        self.rect = self.image.get_rect()
        # Initialise the sprite
        super().__init__()

    def get_asset(self):
        """
        Identify the relative path to the assets of the sprite.
        :return: Path as a string.
        """
        return "../assets/" + self.name + ".png"


class GroundLevel(pygame.sprite.Group):
    """
    Class that defines and the ground level for the game
    world. Applies tiling on the given asset to span across
    the whole screen. GravitySprite defined in sprites will
    ensure that characters do not fall below this level.
    """

    def __init__(self, name):
        """
        Create a new ground level.
        :param name: Asset name.
        :return: Initialised instance of the sprite group.
        """
        # Initialise the sprite group
        super().__init__()
        # Identify the size of the screen
        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()
        # Create and tile the sprites
        offset = 0
        while offset < width:
            # Initialise an environment sprite
            sprite = EnvironmentSprite(name)
            sprite.rect.x = offset
            sprite.rect.y = height - sprite.rect.height
            offset = sprite.rect.right
            self.add(sprite)

    def get_vertical_rect(self):
        """
        Retrieve the vertical bounding rectangle of the group.
        :return: Bounding rectangle of the sprite in the group.
        """
        return self.sprites()[0].rect


class Platform(EnvironmentSprite):
    """
    Class that defines and the platforms that the character
    can step on. Crops the image left and right sides (4px)
    and applies tiling on middle bit to create the platform
    of the specified size.
    """
    # Width of the slot for the 1x1 platform to fit in
    slot_width = 32
    # Size of the border for the art asset
    border = 4

    def __init__(self, name, size):
        """
        Create a new platform.
        :param name: Asset name.
        :param size: Size of the platform.
        :return: Initialised instance of the sprite.
        """
        # Initialise the sprite
        super().__init__(name)
        # Determine the dimensions of the platform
        width = (self.rect.width - 2*self.border) * size + 2*self.border
        height = self.rect.height
        # Generate the tiled asset
        asset = pygame.Surface((width, height), pygame.SRCALPHA)
        asset.blit(self.image, (0, 0), (0, 0, self.border, self.rect.height))
        for i in range(size):
            offset_x = (self.rect.width - 2*self.border) * i + self.border
            crop = (self.border, 0, self.rect.width - 2*self.border, self.rect.height)
            asset.blit(self.image, (offset_x, 0), crop)
        crop = (self.rect.width - self.border, 0, self.border, self.rect.height)
        asset.blit(self.image, (width - self.border, 0), crop)
        # Set the generated asset as appearance for the sprite
        self.image = asset
        self.rect = asset.get_rect()


class Tower(EnvironmentSprite, Damageable):
    """
    Class that defines and the main tower that the character
    is supposed to protect. Aligns the sprite in the middle
    and tracks the damage levels to change the state accordingly.
    """
    ASSET_NAME = "Tower"
    STATE_INITIAL = "Initial"
    STATE_DAMAGED = "Damaged"
    STATE_RUINED = "Ruined"
    MAXIMUM_HEALTH = 100

    def __init__(self):
        """
        Create a new Tower.
        :return: Tower sprite.
        """
        # Initialise the tower
        self.state = ""
        self.set_state(Tower.STATE_INITIAL)
        # Identify the size of the screen
        surface = pygame.display.get_surface()
        width = surface.get_width()
        # Position the tower in the middle vertically
        self.rect.centerx = width / 2
        # Initialise the logic
        self.set_health(Tower.MAXIMUM_HEALTH, Tower.MAXIMUM_HEALTH)

    def set_state(self, state):
        """
        Update the tower state.
        :param state: New state.
        """
        # Set the state of the tower
        self.state = state
        # Reinitialise the sprite
        super().__init__(Tower.ASSET_NAME + '-' + self.state)

    def update(self):
        # Identify previous location
        x = self.rect.x
        y = self.rect.y

        # Update the state based on current tower health
        if self.current > self.maximum * 2/3:
            self.set_state(Tower.STATE_INITIAL)
        elif self.current > self.maximum * 1/3:
            self.set_state(Tower.STATE_DAMAGED)
        else:
            self.set_state(Tower.STATE_RUINED)

        # Restore previous position
        self.rect.x = x
        self.rect.y = y

        # Base update routine
        super().update()


class HealthIndicator(EnvironmentSprite):
    """
    Class that defines the health indicator for the damageable
    creature in the game. Tiles the red and black hearts to display
    the current and maximum health.
    """
    ASSET_NAME = "Life"
    ALT_ASSET_NAME = "Death"

    def __init__(self, parent):
        """
        Create a new health indicator.
        :param parent: Parent damageable creature.
        :return: Health indicator sprite.
        """
        self.parent = parent
        self.rect = pygame.Rect(0, 0, 0, 0)

    def set_health(self, current, maximum):
        """
        Update the indicator with new creature health.
        :param current: Current creature health.
        :param maximum: Maximum creature health.
        """
        # Initialise the sprite
        super().__init__(HealthIndicator.ALT_ASSET_NAME)

        # Identify the number of sprites to be displayed
        count = int(maximum / 10)
        # Determine the dimensions of the indicator
        width = self.rect.width * count
        height = self.rect.height
        asset = pygame.Surface((width, height), pygame.SRCALPHA)
        # Tile the death asset
        for x in range(count):
            asset.blit(self.image, (self.rect.width * x, 0), (0, 0, self.rect.width, self.rect.height))

        # Initialise the sprite
        super().__init__(HealthIndicator.ASSET_NAME)
        # Identify the number of sprites to be displayed
        count = int(current / 10)
        # Tile the whole life asset
        for x in range(count):
            asset.blit(self.image, (self.rect.width * x, 0), (0, 0, self.rect.width, self.rect.height))
        # Draw the partial life asset
        partial_offset = self.rect.width * count
        partial_width = self.rect.width * (current % 10) / 10
        asset.blit(self.image, (partial_offset, 0), (0, 0, partial_width, self.rect.height))

        # Set the generated asset as appearance for the sprite
        self.image = asset
        self.rect = asset.get_rect()

    def update(self):
        # Identify previous location
        x = self.rect.x
        y = self.rect.y

        # Update creature health
        self.set_health(self.parent.current, self.parent.maximum)

        # Restore previous position
        self.rect.x = x
        self.rect.y = y

        # Base update routine
        super().update()


class Level(pygame.sprite.LayeredUpdates):
    """
    Class that defines and manages a game level with all
    the environment objects, game characters and HUD elements
    included.
    """
    # Layer ID for all the environment objects
    ENVIRONMENT = 0
    # Layer ID for the player and all the NPCs
    CHARACTERS = 1
    # Layer ID for the HUD elements
    HUD = 2
    # Vertical distance between platforms
    platform_spacing = 64

    def __init__(self, name):
        """
        Create a new level from the definition file.
        :param name: Name of the level.
        :return: Level sprite group.
        """
        # Initialise the sprite group
        super().__init__()

        # Identify the size of the screen
        surface = pygame.display.get_surface()
        width = surface.get_width()

        # Read the level
        self.definition = LevelReader(name)

        # Create the ground level
        self.ground = GroundLevel(self.definition.ground_level)
        self.add(self.ground, layer=Level.ENVIRONMENT)
        # Create the tower in the middle
        self.tower = Tower()
        self.tower.rect.bottom = self.ground.get_vertical_rect().top
        # Create the player
        self.player = Tin()
        # Create the princess in the tower
        self.princess = LookerSprite(self.player, "Olivia", "StandingLeft")
        self.princess.rect.centerx = self.tower.rect.centerx - 5
        self.princess.rect.y = 168
        self.add(self.princess, layer=Level.CHARACTERS)
        self.add(self.tower, layer=Level.CHARACTERS)
        self.add(self.player, layer=Level.CHARACTERS)

        # Create player's health indicator in the top right corner
        self.player_health = HealthIndicator(self.player)
        self.player_health.update()
        self.player_health.rect.top = 10
        self.player_health.rect.right = width - 10
        self.add(self.player_health, layer=Level.HUD)
        # Create player's icon in the top right corner
        self.player_icon = EnvironmentSprite(Tin.ASSET_NAME + "-Icon")
        self.player_icon.rect.top = 10
        self.player_icon.rect.right = self.player_health.rect.left
        self.add(self.player_icon, layer=Level.HUD)

        # Create player's health indicator in the top right corner
        self.tower_health = HealthIndicator(self.tower)
        self.tower_health.update()
        self.tower_health.rect.top = 10
        self.tower_health.rect.right = self.player_icon.rect.left - 10
        self.add(self.tower_health, layer=Level.HUD)
        # Create tower's icon in the top right corner
        self.tower_icon = EnvironmentSprite(Tower.ASSET_NAME + "-Icon")
        self.tower_icon.rect.top = 10
        self.tower_icon.rect.right = self.tower_health.rect.left - 5
        self.add(self.tower_icon, layer=Level.HUD)

        self.monster = MonsterAimer(self.player)
        self.add(self.monster, layer=Level.CHARACTERS)

        # Create the platforms
        y = self.ground.get_vertical_rect().top
        for line in self.definition.level:
            y -= self.platform_spacing
            for platform in line:
                (x, size, name) = platform
                platform = Platform(name, size)
                platform.rect.x = (Platform.slot_width - 2*Platform.border) * x + Platform.border
                platform.rect.y = y
                self.add(platform, layer=Level.ENVIRONMENT)

    def update(self):
        # Determine environment collisions
        collision_list = pygame.sprite.spritecollide(self.player, self.get_sprites_from_layer(Level.ENVIRONMENT), False)
        if len(collision_list) > 0:
            platform = collision_list[0]
            self.player.environment_collision(platform)
        # Determine character collisions
        collision_list = pygame.sprite.spritecollide(self.player, self.get_sprites_from_layer(Level.CHARACTERS), False)
        if len(collision_list) > 0:
            for character in collision_list:
                if character != self.player:
                    self.player.character_collision(character)
        super().update()