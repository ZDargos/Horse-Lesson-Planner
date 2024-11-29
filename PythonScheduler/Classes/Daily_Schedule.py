# Zack Dragos & Sampath Reddy M.


class Daily_Schedule:
    def __init__(self, day, planner=None, riders=None, horses=None):
        self._day = day # Day of the week
        self._planner = planner if planner is not None else {}  # List of Hourly Schedules
        self._riders = riders if riders is not None else []
        self._horses = horses if horses is not None else []
        self._jumped_today = []
        self._walker_times_today = {}

    def get_day(self):
        return self._day
    def set_day(self, day):
        self._day = day

    def get_planner(self):
        return self._planner

    def add_rider(self, rider, horse, hour):
        self._riders.append(rider)
        if hour in self._planner:
            self._planner[hour].append([rider.get_name(),None if not horse else horse.get_name()])
        else:
            self._planner[hour] = [[rider.get_name(), None if not horse else horse.get_name()]]
        if horse:
            self._horses.append(horse.get_name())


    def set_horse(self, rider, horse, hour, jumper):
        for i, (Rider, Horse) in enumerate(self._planner[hour]):
            if Rider == rider:
                self._planner[hour][i][1] = horse.get_name()
                if jumper:
                    horse.add_jumper_times()
                    self._jumped_today.append(horse.get_name())
                else:
                    horse.add_non_jumper_times()
                    if horse.get_name() in self._walker_times_today:
                        self._walker_times_today[horse.get_name()] += 1
                    else:
                        self._walker_times_today[horse.get_name()] = 1
                self._horses.append(horse.get_name())

    def jumped_today(self, Horse):
        return Horse in self._jumped_today

    def num_walks_today(self, Horse):
        if Horse in self._walker_times_today:
            return self._walker_times_today[Horse]
        else:
            return 0
    def get_horses(self):
        return self._horses

    def __str__(self):
        string = ""
        for key, value in sorted(self._planner.items()):
            string += f'{key}: {value}\n'
        return string


