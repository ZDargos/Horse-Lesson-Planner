# Author: Zack Dragos
# Date: 12/21/24
import os.path
import pickle
from tkinter import messagebox
import pandas as pd
import datetime
from Classes.Rider import *
from Classes.Weekly_Schedule import *
from Classes.Horse import *

class Data_Manipulation:
    def __init__(self, rider_file="", horse_file="", options_file=""):
        self.__rider_file = rider_file
        self.__horse_file = horse_file
        self.__options_file = options_file

    def set_rider_file(self, r_file):
        self.__rider_file = r_file

    def set_horse_file(self, h_file):
        self.__horse_file = h_file

    def save_riders_to_pickle(self, riders):
        try:
            # Open the file in binary write mode
            with open(self.__rider_file, "wb") as file:
                # Serialize the data using pickle
                pickle.dump(riders, file)
            print(f"Data saved successfully to {self.__rider_file}.")
            return 0
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")
            return 1

    def save_horses_to_pickle(self, horses):
        try:
            # Open the file in binary write mode
            with open(self.__horse_file, "wb") as file:
                # Serialize the data using pickle
                pickle.dump(horses, file)
            print(f"Data saved successfully to {self.__horse_file}.")
            return 0
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")
            return 1

    def save_schedule_to_pickle(self, schedule):
        try:
            # Open the file in binary write mode
            with open(".data//schedules//schedule_" + self.get_time_stamp() + ".pkl", "wb") as file:
                # Serialize the data using pickle
                pickle.dump(schedule, file)
            print(f"Data saved successfully to {'.data//schedules//schedule_' + self.get_time_stamp() + '.pkl'}.")
            return 0
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")
            return 1

    def load_riders_from_pickle(self, schedule):
        try:
            with open(self.__rider_file, "rb") as file:
                schedule.set_riders(pickle.load(file))
            print("Data loaded successfully.")
            return 0
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")
            return 1

    def load_horses_from_pickle(self, schedule):
        try:
            with open(self.__horse_file, "rb") as file:
                schedule.set_horses(pickle.load(file))
            print("Data loaded successfully.")
            return 0
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")
            return 1

    def load_riders_from_excel(self, file_path, schedule):
        if file_path:
            try:
                rider_data = pd.read_excel(file_path) if file_path.endswith(('.xlsx', '.xls')) else pd.read_csv(
                    file_path)
                messagebox.showinfo("Rider Data Selected",
                                    f"Rider data successfully uploaded.\n\nData Preview:\n{rider_data.head()}")
                schedule.set_riders([])
                for _, row in rider_data.iterrows():
                    weekly_schedule = row['Weekly Schedule']

                    if isinstance(weekly_schedule, str) and pd.notnull(weekly_schedule):
                        weekly_schedule = weekly_schedule.split("|")
                        for i, lesson in enumerate(weekly_schedule):
                            lesson = lesson.split(';')
                            lesson[-1] = eval(lesson[-1])
                            weekly_schedule[i] = lesson

                    else:
                        weekly_schedule = []

                    if not weekly_schedule:
                        print(f"Rider {row['Name']} has no schedule.")

                    schedule.add_rider(Rider(
                        row['Name'],
                        weight=int(row['Weight']),
                        skill_level=row['Skill Level'],
                        weekly_schedule=weekly_schedule
                    ))
                for rider in schedule.get_riders():
                    print(rider)
                return 0
            except Exception as e:
                messagebox.showerror("Error", f"Error reading rider data file: {e}")
        else:
            messagebox.showwarning("No File Selected", "Please select a valid rider data file.")

    def load_horses_from_excel(self, file_path, schedule):
        if file_path:
            try:
                horse_data = pd.read_excel(file_path) if file_path.endswith(('.xlsx', '.xls')) else pd.read_csv(
                    file_path)
                messagebox.showinfo("Horse Data Selected",
                                    f"Horse data successfully uploaded.\n\nData Preview:\n{horse_data.head()}")
                schedule.set_horses([])
                for i, row in horse_data.iterrows():
                    leaser = row['Leaser'] if pd.notnull(row['Leaser']) else ''
                    schedule.add_horse(Horse(
                        row['Name'],
                        is_jumping_horse=True if row['Jumper?'] == 1 else False,
                        max_weight=int(row['Max Weight']),
                        leaser=leaser,
                        skill_level=row['Difficulty'],
                        max_daily_jumps=int(row['Max Rides per Day'])
                    ))
                for horse in schedule.get_horses():
                    print(horse)
                return 0
            except Exception as e:
                messagebox.showerror("Error", f"Error reading horse data file: {e}")
        else:
            messagebox.showwarning("No File Selected", "Please select a valid horse data file.")

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

    def get_time_stamp(self):
        today = datetime.date.today()  # Find the most recent Sunday
        start_of_week = today - datetime.timedelta(days=today.weekday() + 1)
        return str(start_of_week)  # Get the start of the current week

    def load_options(self, app):
        if os.path.exists(self.__options_file):
            options = open(self.__options_file, "r")
            line = "t"
            while line:
                line = options.readline()
                option = line.strip()
                option = option.split(",")
                if option[0] == "display_font_size":
                    app.display_font_size = int(option[1])
            options.close()
    def save_options(self, app):
        options = open(self.__options_file, 'w')
        options.write("display_font_size," + str(app.display_font_size))