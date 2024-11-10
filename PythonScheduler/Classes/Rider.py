# Zack Dragos & Sampath Reddy M.


class Rider:
    def __init__(self, name="", recent_horses=None, height=0, weight=0, skill_level=0, weekly_schedule=None, total_owed=0):
        self._name = name # Rider's name
        self._recent_horses = recent_horses if recent_horses is not None else [] # List of the 3 most recent horses
        self._height = height
        self._weight = weight
        self._skill_level = skill_level # Integer skill level; 0 for beginner, 1 for jumper
        self._weekly_schedule = weekly_schedule if weekly_schedule is not None else [] # List of tuples (Day of week, hour of the day [from 0 for midnight to 23 for 11pm])
        self._total_owed = total_owed # Float representing the total amount of money owed by this rider

    # Getter and setter for name
    def get_name(self):
        """Gets the rider's name."""
        return self._name

    def set_name(self, name):
        """Sets the rider's name."""
        self._name = name

    # Getter and setter for recent_horses
    def get_recent_horses(self):
        """Gets the list of recent horses ridden by the rider."""
        return self._recent_horses

    def add_recent_horse(self, recent_horse):
        """Adds a horse to list of recent horses ridden by the rider."""
        if len(self._recent_horses) == 3:
            self._recent_horses = self._recent_horses[1:]
        self._recent_horses.append(recent_horse)

    # Getter and setter for height
    def get_height(self):
        """Gets the rider's height."""
        return self._height

    def set_height(self, height):
        """Sets the rider's height."""
        self._height = height

    # Getter and setter for weight
    def get_weight(self):
        """Gets the rider's weight."""
        return self._weight

    def set_weight(self, weight):
        """Sets the rider's weight."""
        self._weight = weight

    # Getter and setter for skill_level
    def get_skill_level(self):
        """Gets the rider's skill level."""
        return self._skill_level

    def set_skill_level(self, skill_level):
        """Sets the rider's skill level."""
        self._skill_level = skill_level

    # Getter and setter for weekly_schedule
    def get_weekly_schedule(self):
        """Gets the rider's weekly riding schedule."""
        return self._weekly_schedule

    def add_lesson_time(self, lesson_time):
        """Sets the rider's weekly riding schedule."""
        self._weekly_schedule.append(lesson_time)

    def remove_lesson_time(self, lesson_time):
        '''
        Removes a lesson time from the weekly schedule, returns True if it exists, False if it didn't
        '''
        for i, lesson in enumerate(self._weekly_schedule):
            if lesson == lesson_time:
                self._weekly_schedule = self._weekly_schedule[:i] + self._weekly_schedule[i+1:]
                return True
        return False

    def clear_lessons(self):
        self._weekly_schedule = []

    # Getter and setter for total_owed
    def get_total_owed(self):
        """Gets the total amount owed by the rider."""
        return self._total_owed

    def set_total_owed(self, total_owed):
        """Sets the total amount owed by the rider."""
        self._total_owed = total_owed

