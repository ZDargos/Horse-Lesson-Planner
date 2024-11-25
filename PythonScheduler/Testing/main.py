# Zack Dragos & Sampath Reddy M.
import random
import sys
import os
sys.path.append(os.path.abspath("C:\\Users\\zrdra\\gitRepositories\\Horse-Lesson-Planner\\PythonScheduler\\"))
sys.path.append(os.path.abspath("C:\\Users\\zrdra\\gitRepositories\\Horse-Lesson-Planner\\PythonScheduler\\Classes"))
sys.path.append(os.path.abspath("C:\\Users\\zrdra\\gitRepositories\\Horse-Lesson-Planner\\PythonScheduler\\Testing"))

from Classes.Horse import *
from Classes.Rider import *
from Classes.Weekly_Schedule import *

def get_random_day():
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return random.choice(days_of_week)


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

def main():
    Schedule = Weekly_Schedule()
    for horse in ALL_HORSES:
        Schedule.add_horse(Horse(horse, is_jumping_horse = random.choice([True,False])))
    for i in range(10):
        Schedule.add_rider(Rider("Rider#" + str(i), None, random.randint(50,70), random.randint(100,190), 0, None, 0))
    Schedule.add_rider(Rider("Sammy", None, 60, 150, 0, None, 0))
    Schedule.add_rider(Rider("Ryan", None, 60, 150, 0, None, 0))
    Schedule.add_rider(Rider("Patrick", None, 60, 150, 0, None, 0))
    for i in range(3):
        for rider in Schedule.get_riders():
            Schedule.add_lesson(rider.get_name(), get_random_day(), random.randint(8, 16), random.choice([30,60]), random.choice([True, False]))

    Schedule.make_schedule()
    for horse in Schedule.get_horses():
        print(horse)
    for rider in Schedule.get_riders():
        print(rider)
    print("\n\n")
    print(Schedule)

if __name__ == "__main__":
    main()


