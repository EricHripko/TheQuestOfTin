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

    def is_dead(self):
        return self.current <= 0