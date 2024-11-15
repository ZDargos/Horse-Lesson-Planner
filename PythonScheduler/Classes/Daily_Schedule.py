# Zack Dragos & Sampath Reddy M.


class Daily_Schedule:
    def __init__(self, day, planner=None, riders=None, horses=None):
        self._day = day # Day of the week
        self._planner = planner if planner is not None else {}  # List of Daily Schedules
        self._riders = riders if riders is not None else []
        self._horses = horses if horses is not None else []

    def get_day(self):
        return self._day
    def set_day(self, day):
        self._day = day

    def get_planner(self):
        return self._planner
    def add_rider(self, rider, horse, hour):
        self._riders.append(rider)
        if hour in self._planner:
            self._planner[hour].append((rider,horse))
        else:
            self._planner[hour] = (rider,horse)


