# Zack Dragos & Sampath Reddy M.

from Daily_Schedule import *
import random

MAX_JUMPER_TIMES = 3

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
        leasers = []
        #Assign all leased horses to their leasers
        for horse in self._horses:
            for leaser in horse.get_leaser().split(";"): #Account for horses with multiple leasers
                if self.get_rider(leaser) in self._riders:

                    for (day, hour, jumper) in self.get_rider(leaser).get_weekly_schedule():
                        self._planner[day].set_horse(leaser, horse, hour, jumper)
                        leasers.append(leaser)


        '''
        Now that all the riders who lease a horse are taken care of, we can assign horses to the rest
        '''

        # Create a list of horses who are currently available
        available_horses = []
        for horse in self._horses:
            if horse.is_available() and horse.get_jumper_times() < MAX_JUMPER_TIMES:
                available_horses.append(horse.get_name())


        # Go through each rider and their weekly schedules to then assign them horses
        used_horses = []
        for rider in self._riders:
            if rider.get_name() in leasers:
                pass
            else:
                for (day, hour, jumper) in rider.get_weekly_schedule():
                    if not available_horses:
                        available_horses = used_horses
                        used_horses = []
                    #Randomly select a horse from the pool of available horses
                    Horse = available_horses[random.randint(0, len(available_horses) - 1)]
                    counter = 0
                    while self.is_horse_unavailable_today(day, Horse, rider, jumper): # Make sure Horse is not been recently used by the rider
                        Horse = available_horses[random.randint(0, len(available_horses) - 1)]
                        counter+=1
                        if counter == 1000: #In case you are only left with one horse that the final few riders have already used, reset the available horses list
                            available_horses.extend(used_horses)
                            used_horses = []
                            continue
                        elif counter > 2000: #In case of impossible scheduling conflict, raise an error and restart the schedule making process
                            raise "Impossible Schedule. No horse left that the rider has not recently ridden"

                    # Remove horse from availability until all horses have been used
                    available_horses.remove(Horse)
                    used_horses.append(Horse)
                    self._planner[day].set_horse(rider.get_name(), self.get_horse(Horse), hour, jumper)
                    rider.add_recent_horse(Horse)


    def is_horse_unavailable_today(self, day, horse_name, rider, jumper):
        '''
        Boolean function that returns true if the horse is not available to the rider on the given day and lesson
        :param day: string of day of week
        :param horse_name: name of horse
        :param rider: rider object
        :param jumper: true false
        :return: true false
        '''
        horse = self.get_horse(horse_name)
        is_unavail = horse in rider.get_recent_horses() or self._planner[day].jumped_today(horse)
        is_unavail = is_unavail or self._planner[day].num_walks_today(horse) > 3 or (jumper and not horse.is_jumping_horse())
        is_unavail = is_unavail or rider.get_weight() > horse.get_max_weight()
        skill = False
        for level in rider.get_skill_level().split("-"):
            skill = skill or level in horse.get_skill_level()
        is_unavail = is_unavail and not skill
        return is_unavail


    def __str__(self):
        string = ""
        for planner in self._planner:
            string += f'{planner}:\n{str(self._planner[planner])}\n'
        return string

