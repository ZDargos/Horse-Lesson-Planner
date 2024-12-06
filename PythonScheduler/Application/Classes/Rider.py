# Zack Dragos & Sampath Reddy M.


class Rider:
    def __init__(self, name="", recent_horses=None, height=0, weight=0, skill_level="B", weekly_schedule=None, total_owed=0):
        self._name = name # Rider's name
        self._recent_horses = recent_horses if recent_horses is not None else [] # List of the 3 most recent horses
        self._height = height
        self._weight = weight
        self._skill_level = skill_level # String skill level; B for beginner, N for novice, I for intermediate, O for open. B-N beginner to novice and so on
        self._weekly_schedule = weekly_schedule if weekly_schedule is not None else [] # List of tuples (Day of week, hour of the day [from 0 for midnight to 23 for 11pm], jumper [true or false], skill level)
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

    def add_lesson_time(self, day, time, length, jumper):
        """Sets the rider's weekly riding schedule."""
        if length <= 30:
            self.add_half_hour_lesson(day,time, jumper)
        else:
            self.add_hour_lesson(day,time,jumper)

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
        '''
        Clears out weekly schedule
        '''
        self._weekly_schedule = []

    # Getter and setter for total_owed
    def get_total_owed(self):
        """Gets the total amount owed by the rider."""
        return self._total_owed

    def add_charge(self, amount):
        """Adds to the total amount owed by the rider."""
        self._total_owed += amount

    def remove_charge(self, amount):
        '''
        Removes money from total owed if bill is paid
        '''
        if self._total_owed < amount:
            return False
        self._total_owed -= amount
        return True

    def add_half_hour_lesson(self, day, hour, jumper=False):
        '''
        Adds a 30-minute-long lesson to their schedule, and accounts for the cost of it
        '''
        self._weekly_schedule.append((day,hour,jumper))
        self.add_charge(75.0)

    def remove_half_hour_lesson(self, day, hour, jumper=False):
        for i,lesson in enumerate(self._weekly_schedule):
            if lesson == (day, hour, jumper):
                self._weekly_schedule = self._weekly_schedule[:i] + self._weekly_schedule[i+1:]
                self.remove_charge(75.00)

    def add_hour_lesson(self, day, hour, prepaid=False, jumper=False):
        '''
        Adds an hour-long lesson to their schedule, and accounts for the cost of it
        '''
        self._weekly_schedule.append((day,hour,jumper))
        if prepaid:
            self.add_charge(85.00)
            return
        else:
            self.add_charge(90.00)

    def remove_hour_lesson(self, lesson, prepaid=False):
        for i,lessonn in enumerate(self._weekly_schedule):
            if lessonn == lesson:
                self._weekly_schedule = self._weekly_schedule[:i] + self._weekly_schedule[i+1:]
                if prepaid:
                    self.remove_charge(85.00)
                else:
                    self.remove_charge(90.00)

    def __str__(self):
        return str([self._name, self._recent_horses, self._height, self._weight, self._skill_level, self._weekly_schedule, self._total_owed])

