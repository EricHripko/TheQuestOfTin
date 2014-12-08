import pygame.time


class Animation:
    """
    Class that defines simple looped frame-by-frame animations
    on art-assets and plays them when prompted to.
    """

    def __init__(self, sprite):
        """
        Create a new animation.
        :param sprite: Asset sprite that will play the animation.
        :return: An empty animation instance.
        """
        # Store the associated sprite
        self.sprite = sprite
        # Initialise the animation as empty by default
        self.frames = []
        # Current frame index
        self.current = 0
        # Ticks when the frame got shown
        self.duration = 0

    def add_frame(self, state, duration):
        """
        Add a new frame to the animation.
        :param state: State the the art asset should be in.
        :param duration: Duration of the frame in milliseconds.
        """
        self.frames.append((state, duration))

    def is_playing(self):
        """
        Identify whether the animation is currently playing.
        :return: True if animation is active, false otherwise.
        """
        return self.duration != 0

    def play(self):
        """
        Play the animation. Takes care of setting the animation off,
        measuring all the timings, changing states and looping. Similar
        to update() method of a sprite.
        """
        # Just started playing the animation
        if self.duration == 0:
            self.duration = pygame.time.get_ticks()

        # Retrieve the current frame information
        (state, duration) = self.frames[self.current]
        self.sprite.set_state(state)
        # Check whether the state needs changing
        elapsed = pygame.time.get_ticks() - self.duration
        if elapsed > duration:
            self.current += 1
            self.duration = pygame.time.get_ticks()
        # Check whether the loop is needed
        if self.current == len(self.frames):
            self.current = 0

    def invalidate(self):
        """
        Update the current frame displayed by the animation.
        Internal routine necessary to be carried out after the
        animation flow was manually altered.
        """
        (state, duration) = self.frames[self.current]
        self.sprite.set_state(state)

    def stop(self):
        """
        Stop playing the animation and reset its state.
        """
        # Do not trigger reset if animation was not being played
        if not self.is_playing():
            return
        # Reset the animation state
        self.current = 0
        self.duration = 0
        self.invalidate()