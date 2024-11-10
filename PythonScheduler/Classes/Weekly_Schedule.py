# Zack Dragos & Sampath Reddy M.


class Weekly_Schedule:
    def __init__(self, planner=None, riders=None, horses=None):
        self._planner = planner if planner is not None else [] # List of Daily Schedules
        self._riders = riders if riders is not None else []
        self._horses = horses if horses is not None else []


