# Zack Dragos & Sampath Reddy M.

from Daily_Schedule import *

class Weekly_Schedule:
    def __init__(self, planner=None, riders=None, horses=None):
        if planner:
            self._planner = planner # List of Daily Schedules
        else:
            self._planner = {"Monday": Daily_Schedule("Monday"), "Tuesday": Daily_Schedule("Tuesday"), "Wednesday": Daily_Schedule("Wednesday"),
                             "Thursday": Daily_Schedule("Thursday"), "Friday": Daily_Schedule("Friday"), "Saturday": Daily_Schedule("Saturday"),
                             "Sunday": Daily_Schedule("Sunday")}
        self._riders = riders if riders is not None else []
        self._horses = horses if horses is not None else []

    def add_rider(self, rider):
        self._riders.append(rider)

    def remove_rider(self, rider):
        for i, Rider in enumerate(self._riders):
            if Rider == rider:
                self._riders = self._riders[:i] + self._riders[i+1:]

    def get_riders(self):
        return self._riders

    def add_horse(self, horse):
        self._horses.append(horse)

    def remove_horse(self, horse):
        for i, Horse in enumerate(self._horses):
            if Horse == horse:
                self._horses = self._horses[:i] + self._horses[i+1:]

    def get_horses(self):
        return self._horses

    def update_schedule(self):
        self.reset_schedule()
        for rider in self._riders:
            for lesson in rider.get_weekly_schedule():
                self._planner[lesson[0]].add_rider(rider, None, lesson[1])

    def reset_schedule(self):
        self._planner = {"Monday": Daily_Schedule("Monday"), "Tuesday": Daily_Schedule("Tuesday"), "Wednesday": Daily_Schedule("Wednesday"),
                             "Thursday": Daily_Schedule("Thursday"), "Friday": Daily_Schedule("Friday"), "Saturday": Daily_Schedule("Saturday"),
                             "Sunday": Daily_Schedule("Sunday")}


