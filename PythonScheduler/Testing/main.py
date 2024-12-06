# Zack Dragos & Sampath Reddy M.
import random
import sys
import os

from PythonScheduler.Application.Classes.Rider import Rider

sys.path.append(os.path.abspath("C:\\Users\\zrdra\\gitRepositories\\Horse-Lesson-Planner\\PythonScheduler\\"))
sys.path.append(os.path.abspath("C:\\Users\\zrdra\\gitRepositories\\Horse-Lesson-Planner\\PythonScheduler\\Classes"))
sys.path.append(os.path.abspath("C:\\Users\\zrdra\\gitRepositories\\Horse-Lesson-Planner\\PythonScheduler\\Testing"))

from PythonScheduler.Application.Classes.Horse import *
from PythonScheduler.Application.Classes.Rider import *
from PythonScheduler.Application.Classes.Weekly_Schedule import *

import random

def get_random_day():
    return random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])


def load_horses(fileName):
    Horses = []
    file = open(fileName, 'r')
    line = file.readline()
    while line:
        line = file.readline()
        line = line.strip()
        data = line.split(",")
        if data == [""]:
            continue
        Horses.append(data)
    return Horses

def upload_horses(HorseData, Schedule):
    for horse in HorseData:
        Schedule.add_horse(Horse(horse[0], is_jumping_horse = True if horse[1] == '1' else False, max_weight= int(horse[2]), leaser=horse[3] if horse[3] != 'null' else "", skill_level=horse[4], max_daily_jumps=int(horse[5])))

def load_riders(fileName):
    Riders = []
    file = open(fileName, 'r')
    line = file.readline()
    while line:
        line = file.readline()
        line = line.strip()
        data = line.split(",")
        if len(data) > 3:
            data[3] = data[3].split("|")
            if data[3] == ['null']:
                data[3] = None
            else:
                for i, d in enumerate(data[3]):
                    data[3][i] = data[3][i].split(";")
                    data[3][i][-1] = eval(data[3][i][-1])
            Riders.append(data)
    return Riders

def upload_riders(RiderData, Schedule):
    for rider in RiderData:
        Schedule.add_rider(Rider(rider[0], weight=int(rider[1]), skill_level=rider[2], weekly_schedule=rider[3]))
ALL_HORSES = [
    "Carmel",
    "Chico",
    "Papa",
    "Spotty",
    "Heidi",
    "Moose",
    "Sir",
    "Charlie",
    "Elido",
    "IKON",
    "Okie",
    "Diesel",
    "SAM",
    "Tucker",
    "Power",
    "Ella",
    "Winnie",
    "Kitty",
    "Theo",
    "Miss Patty",
    "Squirrel",
    "ACORN"
]

def randomize_data(Schedule):
    for horse in ALL_HORSES:
        Schedule.add_horse(Horse(horse, is_jumping_horse = random.choice([True,False]), max_weight=random.randint(150,230)))
    for i in range(15):
        Schedule.add_rider(Rider("Rider#" + str(i), None, random.randint(50,70), random.randint(100,190), 0, None, 0))
    for i in range(4):
        for rider in Schedule.get_riders():
            Schedule.add_lesson(rider.get_name(), get_random_day(), random.randint(8, 16), random.choice([30,60]), random.choice([True, False]))

def main():
    Schedule = Weekly_Schedule()
    Horses = load_horses("HorseData.csv")
    upload_horses(Horses, Schedule)
    Riders = load_riders("RiderData.csv")
    upload_riders(Riders,Schedule)
    #Schedule.make_schedule()

    attempts = 0
    while attempts < 1000:
        try:
            attempts+=1
            Schedule.make_schedule()
            break
        except:
            pass
    if attempts == 1000:
        raise "Failed to find a working schedule."
    for horse in Schedule.get_horses():
        print(horse)
    for rider in Schedule.get_riders():
        print(rider)
    print("\n\n")
    print(Schedule)

if __name__ == "__main__":
    main()