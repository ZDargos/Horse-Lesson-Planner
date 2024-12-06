# Zack Dragos & Sampath Reddy M.
from fontTools.varLib.instancer import setMacOverlapFlags


class Horse:
    def __init__(self, name="", leaser="", jumper_times=0, non_jumper_times=0, available=True, is_jumping_horse=True, max_weight=190, skill_level="B", max_daily_jumps=1):
        self._name = name
        self._leaser = leaser #The person who currently leases the horse, is empty string if nobody is leasing
        self._jumper_times = jumper_times #Number of times this week the horse has been scheduled to do a jumping lesson
        self._non_jumper_times = non_jumper_times #Number of times this week the horse has been scheduled to do a non-jumping lesson
        self._available = available #Is the horse available this week
        self._is_jumping_horse = is_jumping_horse #Is the horse a jumping horse this week
        self._max_weight = max_weight
        self._skill_level = skill_level
        self._max_daily_jumps = max_daily_jumps


    def get_max_daily_jumps(self):
        return self._max_daily_jumps

    def get_skill_level(self):
        """Gets the skill level of the horse"""
        return self._skill_level

    def set_skill_level(self, skill_level):
        """Sets a new skill level for the horse"""
        self._skill_level = skill_level
    # Getter and setter for leaser
    def get_leaser(self):
        """Gets the name of the person currently leasing the horse."""
        return self._leaser

    def set_leaser(self, leaser):
        """Sets the name of the person leasing the horse."""
        self._leaser = leaser

    # Getter and setter for jumper_times
    def get_jumper_times(self):
        """Gets the number of times the horse has been scheduled for a jumping lesson."""
        return self._jumper_times

    def add_jumper_times(self):
        """Sets the number of times the horse has been scheduled for a jumping lesson."""
        self._jumper_times += 1

    # Getter and setter for non_jumper_times
    def get_non_jumper_times(self):
        """Gets the number of times the horse has been scheduled for a non-jumping lesson."""
        return self._non_jumper_times

    def add_non_jumper_times(self):
        """Sets the number of times the horse has been scheduled for a non-jumping lesson."""
        self._non_jumper_times += 1

    # Getter and setter for available
    def is_available(self):
        """Gets the availability status of the horse."""
        return self._available

    def set_available(self, available):
        """Sets the availability status of the horse."""
        self._available = available

    # Getter and setter for is_jumping_horse
    def is_jumping_horse(self):
        """Checks if the horse is a jumping horse."""
        return self._is_jumping_horse

    def set_is_jumping_horse(self, is_jumping_horse):
        """Sets whether the horse is a jumping horse."""
        self._is_jumping_horse = is_jumping_horse

    def get_name(self):
        return self._name

    def get_max_weight(self):
        return self._max_weight

    def __str__(self):
        return str([self._name, self._leaser, self._jumper_times, self._non_jumper_times, self._available, self._is_jumping_horse, self._max_weight, self._skill_level, self._max_daily_jumps])