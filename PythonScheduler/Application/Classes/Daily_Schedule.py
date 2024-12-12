# Author: Zack Dragos, Sampath Reddy M., Palak Sood
# Date: 12/13/24
# Description: File storing the Daily Schedule class and all of its functionality


class Daily_Schedule:
    def __init__(self, day, planner=None, riders=None, horses=None):
        '''
        Initializes the Daily_Schedule object with a specific day, planner, riders, and horses.
        :param day: string representing the day of the week
        :param planner: dictionary containing hourly schedules
        :param riders: list of rider objects
        :param horses: list of horse objects
        :return: None
        '''
        self._day = day
        self._planner = planner if planner is not None else {}
        self._riders = riders if riders is not None else []
        self._horses = horses if horses is not None else []
        self._jumped_today = []
        self._walker_times_today = {}
        self._jumper_times_today = {}

    def get_day(self):
        '''
        Gets the day of the week for the schedule.
        :return: string representing the day of the week
        '''
        return self._day

    def set_day(self, day):
        '''
        Sets the day of the week for the schedule.
        :param day: string representing the new day of the week
        :return: None
        '''
        self._day = day

    def get_planner(self):
        '''
        Gets the planner containing the hourly schedule.
        :return: dictionary of hourly schedules
        '''
        return self._planner

    def add_rider(self, rider, horse, hour):
        '''
        Adds a rider and their assigned horse to the schedule at a specific hour.
        :param rider: rider object to be added
        :param horse: horse object assigned to the rider
        :param hour: string representing the hour in HHMM format
        :return: None
        '''
        self._riders.append(rider)
        if hour in self._planner:
            self._planner[hour].append([rider.get_name(), None if not horse else horse.get_name()])
        else:
            self._planner[hour] = [[rider.get_name(), None if not horse else horse.get_name()]]
        if horse:
            self._horses.append(horse.get_name())

    def set_horse(self, rider, horse, hour, jumper):
        '''
        Assigns a horse to a rider for a specific hour and updates jumper/non-jumper times.
        :param rider: string representing the rider's name
        :param horse: horse object to be assigned
        :param hour: string representing the hour in HHMM format
        :param jumper: boolean indicating if the lesson is a jumping lesson
        :return: None
        '''
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
        '''
        Boolean function that returns true if the horse has reached its maximum jumps for the day.
        :param horse: horse object to check
        :return: true if maximum jumps are reached, false otherwise
        '''
        if horse.get_name() in self._jumper_times_today:
            if self._jumper_times_today[horse.get_name()] >= horse.get_max_daily_jumps():
                return True
            return False
        else:
            return False

    def num_walks_today(self, Horse):
        '''
        Gets the number of walking lessons a specific horse has completed today.
        :param Horse: string representing the horse's name
        :return: integer count of walking lessons
        '''
        if Horse in self._walker_times_today:
            return self._walker_times_today[Horse]
        else:
            return 0

    def get_horses(self):
        '''
        Gets the list of all horses involved in today's schedule.
        :return: list of horse names
        '''
        return self._horses

    def military_to_standard(self, military_time):
        '''
        Converts military time (HHMM) to standard time (12-hour format with AM/PM).
        :param military_time: string representing time in HHMM format
        :return: string of time in 12-hour format with AM/PM
        '''
        try:
            if military_time == "-1":
                return "Hack"

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
            standard_hours = hours % 12 or 12

            # Return formatted time
            return f"{standard_hours:02}:{minutes:02d} {period}"
        except Exception as e:
            return f"Error: {e}. Please provide time in HHMM format."

    def riding_this_time(self, horse, time):
        '''
        Boolean function that checks if a specific horse is scheduled to ride at a given time.
        :param horse: horse object to check
        :param time: string representing the hour in HHMM format
        :return: true if the horse is scheduled, false otherwise
        '''
        if time in self._planner:
            for _, Horse in self._planner[time]:
                if horse.get_name() == Horse:
                    return True
        return False

    def __str__(self):
        '''
        Converts the daily schedule to a string format for display.
        :return: string representation of the daily schedule
        '''
        string = ""
        for key, value in sorted(self._planner.items()):
            string += f'{self.military_to_standard(key) if key != "-1" else "Hack"}: {value}\n'
        return string
