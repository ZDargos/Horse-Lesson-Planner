# Zack Dragos & Sampath Reddy M.


class Daily_Schedule:
    def __init__(self, day, planner=None, riders=None, horses=None):
        self._day = day # Day of the week
        self._planner = planner if planner is not None else {}  # List of Hourly Schedules
        self._riders = riders if riders is not None else []
        self._horses = horses if horses is not None else []
        self._jumped_today = []
        self._walker_times_today = {}
        self._jumper_times_today = {}

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
                    if horse.get_name() in self._jumper_times_today:
                        self._jumper_times_today[horse.get_name()] += 1
                    else:
                        self._jumper_times_today[horse.get_name()] = 1
                else:
                    horse.add_non_jumper_times()
                    if horse.get_name() in self._walker_times_today:
                        self._walker_times_today[horse.get_name()] += 1
                    else:
                        self._walker_times_today[horse.get_name()] = 1
                self._horses.append(horse.get_name())

    def max_jumped_today(self, horse):
        if horse.get_name() in self._jumper_times_today:
            if self._jumper_times_today[horse.get_name()] >= horse.get_max_daily_jumps():
                return True
            return False
        else:
            return False

    def num_walks_today(self, Horse):
        if Horse in self._walker_times_today:
            return self._walker_times_today[Horse]
        else:
            return 0
    def get_horses(self):
        return self._horses

    def military_to_standard(self,military_time):
        """
        Convert military time (HHMM) to standard time (12-hour format with AM/PM).
        Parameters: military_time (str): Time in HHMM format (e.g., "1400").
        Returns: Time in 12-hour format with AM/PM (e.g., "02:00 PM").
        """
        try:
            # Ensure the input is exactly 4 characters and is numeric
            if len(military_time) != 4 or not military_time.isdigit():
                raise ValueError("Invalid time format. Use HHMM format (e.g., 1400).")

            # Parse hours and minutes
            hours = int(military_time[:2])
            minutes = int(military_time[2:])

            # Validate time
            if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                raise ValueError("Invalid time. Hours must be 00-23 and minutes 00-59.")

            # Determine AM/PM and adjust hours for 12-hour format
            period = "AM" if hours < 12 else "PM"
            standard_hours = hours % 12 or 12  # Convert 0 or 12 to 12

            # Return formatted time
            return f"{standard_hours:02}:{minutes:02d} {period}"
        except Exception as e:
            return f"Error: {e}. Please provide time in HHMM format."

    def riding_this_time(self, horse, time):
        if time in self._planner:
            for _,Horse in self._planner[time]:
                if horse.get_name() == Horse:
                    return True
        return False


    def __str__(self):
        string = ""
        for key, value in sorted(self._planner.items()):
            string += f'{self.military_to_standard(key) if key != "-1" else "Hack"}: {value}\n'
        return string


