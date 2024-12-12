# Author: Zack Dragos, Sampath Reddy M., Palak Sood
# Date: 12/13/24
# Description: File storing the Horse class and all of its functionality

class Horse:
    def __init__(self, name="", leaser="", jumper_times=0, non_jumper_times=0, available=True, is_jumping_horse=True, max_weight=190, skill_level="B", max_daily_jumps=1):
        '''
        Initializes the Horse object with details about its name, leaser, times used, availability, and attributes.
        :param name: string representing the horse's name
        :param leaser: string representing the leaser's name
        :param jumper_times: integer representing the number of jumping lessons this week
        :param non_jumper_times: integer representing the number of non-jumping lessons this week
        :param available: boolean indicating if the horse is available
        :param is_jumping_horse: boolean indicating if the horse is a jumping horse
        :param max_weight: integer representing the maximum rider weight the horse can handle
        :param skill_level: string representing the horse's skill level
        :param max_daily_jumps: integer representing the maximum number of jumps the horse can perform daily
        :return: None
        '''
        self._name = name
        self._leaser = leaser
        self._jumper_times = jumper_times
        self._non_jumper_times = non_jumper_times
        self._available = available
        self._is_jumping_horse = is_jumping_horse
        self._max_weight = max_weight
        self._skill_level = skill_level
        self._max_daily_jumps = max_daily_jumps

    def get_max_daily_jumps(self):
        '''
        Gets the maximum number of daily jumps the horse can perform.
        :return: integer representing the maximum daily jumps
        '''
        return self._max_daily_jumps

    def get_skill_level(self):
        '''
        Gets the skill level of the horse.
        :return: string representing the horse's skill level
        '''
        return self._skill_level

    def set_skill_level(self, skill_level):
        '''
        Sets a new skill level for the horse.
        :param skill_level: string representing the new skill level
        :return: None
        '''
        self._skill_level = skill_level

    def get_leaser(self):
        '''
        Gets the name of the person currently leasing the horse.
        :return: string representing the leaser's name
        '''
        return self._leaser

    def set_leaser(self, leaser):
        '''
        Sets the name of the person leasing the horse.
        :param leaser: string representing the leaser's name
        :return: None
        '''
        self._leaser = leaser

    def get_jumper_times(self):
        '''
        Gets the number of times the horse has been scheduled for a jumping lesson this week.
        :return: integer representing the number of jumping lessons
        '''
        return self._jumper_times

    def add_jumper_times(self):
        '''
        Increments the number of times the horse has been scheduled for a jumping lesson this week.
        :return: None
        '''
        self._jumper_times += 1

    def get_non_jumper_times(self):
        '''
        Gets the number of times the horse has been scheduled for a non-jumping lesson this week.
        :return: integer representing the number of non-jumping lessons
        '''
        return self._non_jumper_times

    def add_non_jumper_times(self):
        '''
        Increments the number of times the horse has been scheduled for a non-jumping lesson this week.
        :return: None
        '''
        self._non_jumper_times += 1

    def is_available(self):
        '''
        Checks if the horse is available for lessons.
        :return: boolean indicating the availability of the horse
        '''
        return self._available

    def set_available(self, available):
        '''
        Sets the availability status of the horse.
        :param available: boolean representing the horse's availability
        :return: None
        '''
        self._available = available

    def is_jumping_horse(self):
        '''
        Checks if the horse is a jumping horse.
        :return: boolean indicating if the horse is a jumping horse
        '''
        return self._is_jumping_horse

    def set_is_jumping_horse(self, is_jumping_horse):
        '''
        Sets whether the horse is a jumping horse.
        :param is_jumping_horse: boolean representing if the horse is a jumping horse
        :return: None
        '''
        self._is_jumping_horse = is_jumping_horse

    def get_name(self):
        '''
        Gets the name of the horse.
        :return: string representing the horse's name
        '''
        return self._name

    def get_max_weight(self):
        '''
        Gets the maximum rider weight the horse can handle.
        :return: integer representing the maximum weight in pounds
        '''
        return self._max_weight

    def reset_horse(self):
        '''
        Resets the horse's jumper and non-jumper lesson counts for the week.
        :return: None
        '''
        self._jumper_times = 0
        self._non_jumper_times = 0

    def __str__(self):
        '''
        Converts the horse's details to a string representation.
        :return: string containing the horse's attributes
        '''
        return str([self._name, self._leaser, self._jumper_times, self._non_jumper_times, self._available, self._is_jumping_horse, self._max_weight, self._skill_level, self._max_daily_jumps])
