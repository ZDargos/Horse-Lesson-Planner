# Author: Zack Dragos, Sampath Reddy M., Palak Sood
# Date: 12/13/24
# Description: File storing the Weekly Schedule class and all of its functionality

from Classes.Daily_Schedule import *
from Classes.Rider import *
import random


MAX_JUMPER_TIMES = 3

class Weekly_Schedule:
    def __init__(self, planner=None, riders=None, horses=None):
        '''
        Initializes the Weekly_Schedule object with daily schedules, riders, and horses.
        :param planner: dictionary containing daily schedules
        :param riders: list of rider objects
        :param horses: list of horse objects
        :return: None
        '''
        if planner:
            self._planner = planner
        else:
            self._planner = {"Monday": Daily_Schedule("Monday"), "Tuesday": Daily_Schedule("Tuesday"), "Wednesday": Daily_Schedule("Wednesday"),
                             "Thursday": Daily_Schedule("Thursday"), "Friday": Daily_Schedule("Friday"), "Saturday": Daily_Schedule("Saturday"),
                             "Sunday": Daily_Schedule("Sunday")}
        self._riders = riders if riders is not None else []
        self._horses = horses if horses is not None else []

    def add_rider(self, rider):
        '''
        Adds a rider to the weekly schedule.
        :param rider: rider object to be added
        :return: None
        '''
        self._riders.append(rider)

    def remove_rider(self, rider):
        '''
        Removes a rider from the weekly schedule.
        :param rider: name of the rider to be removed
        :return: boolean indicating if the rider was successfully removed
        '''
        for i, Rider in enumerate(self._riders):
            if Rider.get_name() == rider:
                self._riders = self._riders[:i] + self._riders[i+1:]
                return True
        return False

    def get_riders(self):
        '''
        Gets the list of all riders in the schedule.
        :return: list of rider objects
        '''
        return self._riders

    def get_rider(self, rider):
        '''
        Gets a rider object by name.
        :param rider: name of the rider to retrieve
        :return: rider object
        '''
        for r in self._riders:
            if r.get_name() == rider:
                return r

    def add_horse(self, horse):
        '''
        Adds a horse to the weekly schedule.
        :param horse: horse object to be added
        :return: None
        '''
        self._horses.append(horse)

    def remove_horse(self, horse):
        '''
        Removes a horse from the weekly schedule.
        :param horse: name of the horse to be removed
        :return: boolean indicating if the horse was successfully removed
        '''
        for i, Horse in enumerate(self._horses):
            if Horse.get_name() == horse:
                self._horses = self._horses[:i] + self._horses[i+1:]
                return True
        return False

    def get_horses(self):
        '''
        Gets the list of all horses in the schedule.
        :return: list of horse objects
        '''
        return self._horses

    def get_horse(self, horse):
        '''
        Gets a horse object by name.
        :param horse: name of the horse to retrieve
        :return: horse object
        '''
        for h in self._horses:
            if h.get_name() == horse:
                return h

    def update_schedule(self):
        '''
        Updates the schedule by resetting and assigning lessons based on the riders' weekly schedules.
        :return: None
        '''
        self.reset_schedule()
        for rider in self._riders:
            rider.reset_recent_horses()
            for lesson in rider.get_weekly_schedule():
                self._planner[lesson[0]].add_rider(rider, None, lesson[1])

    def reset_schedule(self):
        '''
        Resets the schedule by clearing all daily schedules and resetting horse data.
        :return: None
        '''
        self._planner = {"Monday": Daily_Schedule("Monday"), "Tuesday": Daily_Schedule("Tuesday"), "Wednesday": Daily_Schedule("Wednesday"),
                             "Thursday": Daily_Schedule("Thursday"), "Friday": Daily_Schedule("Friday"), "Saturday": Daily_Schedule("Saturday"),
                             "Sunday": Daily_Schedule("Sunday")}
        for horse in self._horses:
            horse.reset_horse()

    def add_lesson(self, rider, day, time, duration, jumper=False):
        '''
        Adds a lesson to a rider's weekly schedule.
        :param rider: name or object of the rider
        :param day: string of the day of the lesson
        :param time: time of the lesson in HHMM format
        :param duration: duration of the lesson in minutes
        :param jumper: boolean indicating if the lesson is a jumping lesson
        :return: None
        '''
        if isinstance(rider, Rider):
            r = rider
        else:
            r = self.get_rider(rider)
        r.add_lesson_time(day, time, duration, jumper)

    def make_schedule(self):
        '''
        Main functionality for assigning horses to riders and generating the weekly schedule.
        :return: None
        '''
        self.update_schedule()
        leasers = []
        for horse in self._horses:
            for leaser in horse.get_leaser().split(";"):
                if self.get_rider(leaser) in self._riders:
                    for (day, hour, jumper) in self.get_rider(leaser).get_weekly_schedule():
                        self._planner[day].set_horse(leaser, horse, hour, jumper)
                        leasers.append(leaser)

        available_horses = []
        for horse in self._horses:
            if horse.is_available() and horse.get_jumper_times() < MAX_JUMPER_TIMES:
                available_horses.append(horse.get_name())

        used_horses = []
        for rider in self._riders:
            if rider.get_name() in leasers:
                pass
            else:
                for (day, hour, jumper) in rider.get_weekly_schedule():
                    if not available_horses:
                        available_horses = used_horses
                        used_horses = []
                    Horse = available_horses[random.randint(0, len(available_horses) - 1)]
                    counter = 0
                    while self.is_horse_unavailable_today(day, Horse, rider, jumper, hour):
                        Horse = available_horses[random.randint(0, len(available_horses) - 1)]
                        counter += 1
                        if counter == 1000:
                            available_horses.extend(used_horses)
                            used_horses = []
                            continue
                        elif counter > 2000:
                            raise "Impossible Schedule. No horse left that the rider has not recently ridden"

                    available_horses.remove(Horse)
                    used_horses.append(Horse)
                    self._planner[day].set_horse(rider.get_name(), self.get_horse(Horse), hour, jumper)
                    if self.get_horse(Horse).get_jumper_times() >= MAX_JUMPER_TIMES:
                        used_horses.remove(Horse)
                    rider.add_recent_horse(Horse)

    def is_horse_unavailable_today(self, day, horse_name, rider, jumper, hour):
        '''
        Boolean function that returns true if the horse is not available to the rider on the given day and lesson.
        :param day: string of day of week
        :param horse_name: name of horse
        :param rider: rider object
        :param jumper: true false
        :param hour: time of the lesson in HHMM format
        :return: true false
        '''
        horse = self.get_horse(horse_name)
        return (self._planner[day].max_jumped_today(horse) or self._planner[day].max_jumped_today(horse) or
                self._planner[day].num_walks_today(horse) > 3 or (jumper and not horse.is_jumping_horse()) or
                rider.get_weight() > horse.get_max_weight() or self._planner[day].riding_this_time(horse, hour) or
                self.match_skill_level(rider, horse) == False)

    def match_skill_level(self, rider, horse):
        '''
        Boolean function that returns true if the rider and horse have matching skill levels
        :param rider: rider object
        :param horse: horse object
        :return: true if their skill levels match, false if not
        '''

        for level in rider.get_skill_level().split("-"):
            if level in horse.get_skill_level():
                return True
        return False

    def find_rider_available_horses(self, available_horses, rider, day, jumper, hour):
        '''
        Function to find and return a list of all available horses to a rider on a given day and time
        :param available_horses: list of horses
        :param rider: rider object
        :param day: string representing day
        :param jumper: boolean is a jumper or not
        :param hour: string representing time of day
        :return: list of horse names
        '''
        horses_available_to_rider = []
        for horse in available_horses:
            if self.is_horse_unavailable_today(day, horse, rider, jumper, hour):
                pass
            else:
                horses_available_to_rider.append(horse)
        return horses_available_to_rider

    def save_schedule(self):
        pass

    def __str__(self):
        '''
        Converts the weekly schedule to a string format for display.
        :return: string representation of the weekly schedule
        '''
        string = ""
        for planner in self._planner:
            string += f'{planner}:\n{str(self._planner[planner])}\n'
        return string

