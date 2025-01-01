# Author: Zack Dragos, Sampath Reddy M., Palak Sood
# Date: 12/13/24
# Description: File storing the Rider class and all of its functionality

class Rider:
    def __init__(self, name="", recent_horses=None, height=0, weight=0, skill_level="B", weekly_schedule=None, total_owed=0):
        '''
        Initializes the Rider object with name, recent horses, height, weight, skill level, weekly schedule, and total owed.
        :param name: string representing the rider's name
        :param recent_horses: list of the 3 most recently ridden horses
        :param height: integer representing the rider's height in inches
        :param weight: integer representing the rider's weight in pounds
        :param skill_level: string representing the rider's skill level (e.g., B for beginner)
        :param weekly_schedule: list of tuples representing the rider's weekly schedule
        :param total_owed: float representing the total amount owed by the rider
        :return: None
        '''
        self._name = name
        self._recent_horses = recent_horses if recent_horses is not None else []
        self._height = height
        self._weight = weight
        self._skill_level = skill_level
        self._weekly_schedule = weekly_schedule if weekly_schedule is not None else []
        self._total_owed = total_owed


    def get_name(self):
        '''
        Gets the rider's name.
        :return: string representing the rider's name
        '''
        return self._name

    def set_name(self, name):
        '''
        Sets the rider's name.
        :param name: string representing the rider's new name
        :return: None
        '''
        self._name = name

    def get_recent_horses(self):
        '''
        Gets the list of recent horses ridden by the rider.
        :return: list of horse names
        '''
        return self._recent_horses

    def add_recent_horse(self, recent_horse):
        '''
        Adds a horse to the list of recent horses ridden by the rider.
        :param recent_horse: string representing the horse's name
        :return: None
        '''
        if len(self._recent_horses) == 3:
            self._recent_horses = self._recent_horses[1:]
        self._recent_horses.append(recent_horse)

    def reset_recent_horses(self):
        '''
        Resets the list of recent horses ridden by the rider.
        :return: None
        '''
        self._recent_horses = []

    def get_height(self):
        '''
        Gets the rider's height.
        :return: integer representing the rider's height in inches
        '''
        return self._height

    def set_height(self, height):
        '''
        Sets the rider's height.
        :param height: integer representing the rider's new height in inches
        :return: None
        '''
        self._height = height

    def get_weight(self):
        '''
        Gets the rider's weight.
        :return: integer representing the rider's weight in pounds
        '''
        return self._weight

    def set_weight(self, weight):
        '''
        Sets the rider's weight.
        :param weight: integer representing the rider's new weight in pounds
        :return: None
        '''
        self._weight = weight

    def get_skill_level(self):
        '''
        Gets the rider's skill level.
        :return: string representing the rider's skill level
        '''
        return self._skill_level

    def set_skill_level(self, skill_level):
        '''
        Sets the rider's skill level.
        :param skill_level: string representing the rider's new skill level
        :return: None
        '''
        self._skill_level = skill_level

    def get_weekly_schedule(self):
        '''
        Gets the rider's weekly riding schedule.
        :return: list of tuples representing the weekly schedule
        '''
        return self._weekly_schedule

    def add_lesson_time(self, day, time, length, jumper, prepaid=False):
        '''
        Adds a lesson time to the rider's weekly schedule.
        :param day: string representing the day of the lesson
        :param time: string representing the time of the lesson in HHMM format
        :param length: integer representing the duration of the lesson in minutes
        :param jumper: boolean indicating if the lesson is a jumping lesson
        :return: None
        '''
        if length <= 30:
            self.add_half_hour_lesson(day, time, jumper)
        else:
            self.add_hour_lesson(day, time, jumper=jumper, prepaid=prepaid)

    def remove_lesson_time(self, lesson_time):
        '''
        Removes a lesson time from the rider's weekly schedule.
        :param lesson_time: tuple representing the lesson to be removed
        :return: boolean indicating if the lesson was successfully removed
        '''
        for i, lesson in enumerate(self._weekly_schedule):
            if lesson == lesson_time or lesson[1] == lesson_time:
                self._weekly_schedule = self._weekly_schedule[:i] + self._weekly_schedule[i + 1:]
                return True
        raise LookupError

    def clear_lessons(self):
        '''
        Clears all lessons from the rider's weekly schedule.
        :return: None
        '''
        self._weekly_schedule = []

    def get_total_owed(self):
        '''
        Gets the total amount owed by the rider.
        :return: float representing the total amount owed
        '''
        return self._total_owed

    def add_charge(self, amount):
        '''
        Adds a charge to the total amount owed by the rider.
        :param amount: float representing the charge to be added
        :return: None
        '''
        self._total_owed += amount

    def remove_charge(self, amount):
        '''
        Removes a charge from the total amount owed if the bill is paid.
        :param amount: float representing the charge to be removed
        :return: boolean indicating if the charge was successfully removed
        '''
        if self._total_owed < amount:
            return False
        self._total_owed -= amount
        return True

    def add_half_hour_lesson(self, day, hour, jumper=False):
        '''
        Adds a 30-minute lesson to the rider's weekly schedule and charges $75 for it.
        :param day: string representing the day of the lesson
        :param hour: string representing the time of the lesson in HHMM format
        :param jumper: boolean indicating if the lesson is a jumping lesson
        :return: None
        '''
        self._weekly_schedule.append((day, hour, jumper, 30))
        #self.add_charge(75.0)

    def remove_half_hour_lesson(self, day, hour, jumper=False):
        '''
        Removes a 30-minute lesson from the rider's weekly schedule and deducts $75 from the total owed.
        :param day: string representing the day of the lesson
        :param hour: string representing the time of the lesson in HHMM format
        :param jumper: boolean indicating if the lesson is a jumping lesson
        :return: None
        '''
        for i, lesson in enumerate(self._weekly_schedule):
            if lesson == (day, hour, jumper, 30):
                self._weekly_schedule = self._weekly_schedule[:i] + self._weekly_schedule[i + 1:]
                #self.remove_charge(75.0)

    def add_hour_lesson(self, day, hour, jumper=False, prepaid=False, ):
        '''
        Adds a 1-hour lesson to the rider's weekly schedule and charges $85 if prepaid or $90 otherwise.
        :param day: string representing the day of the lesson
        :param hour: string representing the time of the lesson in HHMM format
        :param prepaid: boolean indicating if the lesson is prepaid
        :param jumper: boolean indicating if the lesson is a jumping lesson
        :return: None
        '''
        self._weekly_schedule.append((day, hour, jumper, 60, prepaid))
        # if prepaid:
        #     self.add_charge(85.0)
        # else:
        #     self.add_charge(90.0)

    def remove_hour_lesson(self, lesson):
        '''
        Removes a 1-hour lesson from the rider's weekly schedule and deducts the appropriate charge.
        :param lesson: tuple representing the lesson to be removed
        :param prepaid: boolean indicating if the lesson was prepaid
        :return: None
        '''
        for i,lessonn in enumerate(self._weekly_schedule):
            if lessonn == lesson:
                self._weekly_schedule = self._weekly_schedule[:i] + self._weekly_schedule[i+1:]
                # if prepaid:
                #     self.remove_charge(85.00)
                # else:
                #     self.remove_charge(90.00)

    def __str__(self):
        '''
        Converts the Rider object to a string format for display.
        :return: string representation of the Rider object
        '''
        return str([self._name, self._recent_horses, self._height, self._weight, self._skill_level, self._weekly_schedule, self._total_owed])

