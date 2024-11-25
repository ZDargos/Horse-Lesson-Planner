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

    def get_rider(self, rider):
        for r in self._riders:
            if r.get_name() == rider:
                return r

    def add_horse(self, horse):
        self._horses.append(horse)


    def remove_horse(self, horse):
        for i, Horse in enumerate(self._horses):
            if Horse == horse:
                self._horses = self._horses[:i] + self._horses[i+1:]

    def get_horses(self):
        return self._horses

    def get_horse(self, horse):
        for h in self._horses:
            if h.get_name() == horse:
                return h
    def update_schedule(self):
        self.reset_schedule()
        for rider in self._riders:
            for lesson in rider.get_weekly_schedule():
                self._planner[lesson[0]].add_rider(rider, None, lesson[1])

    def reset_schedule(self):
        self._planner = {"Monday": Daily_Schedule("Monday"), "Tuesday": Daily_Schedule("Tuesday"), "Wednesday": Daily_Schedule("Wednesday"),
                             "Thursday": Daily_Schedule("Thursday"), "Friday": Daily_Schedule("Friday"), "Saturday": Daily_Schedule("Saturday"),
                             "Sunday": Daily_Schedule("Sunday")}


    def add_lesson(self, rider, day, time, duration, jumper=False):
        r = self.get_rider(rider)
        r.add_lesson_time(day, time, duration, jumper)

    def make_schedule(self):
        '''
        Main logical functionality of sorting which horse goes to what rider and when
        :return: None
        '''

        #Update scheudle to make sure all riders and times are in
        self.update_schedule()

        #Assign all leased horses to their leasers
        for horse in self._horses:
            if self.get_rider(horse.get_leaser()) in self._riders:
                for (day, hour, jumper) in self.get_rider(horse.get_leaser()).get_weekly_schedule():
                    self._planner[day].set_horse(horse.get_leaser(), horse, hour, jumper)

        #Now that all the riders who lease a horse are taken care of, we can assign horses to the rest



    def __str__(self):
        string = ""
        for planner in self._planner:
            string += f'{planner}:  {str(self._planner[planner])}\n'
        return string

