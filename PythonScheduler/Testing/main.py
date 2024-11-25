# Zack Dragos & Sampath Reddy M.

import sys
import os
sys.path.append(os.path.abspath("C:\\Users\\zrdra\\gitRepositories\\Horse-Lesson-Planner\\PythonScheduler\\"))
sys.path.append(os.path.abspath("C:\\Users\\zrdra\\gitRepositories\\Horse-Lesson-Planner\\PythonScheduler\\Classes"))
sys.path.append(os.path.abspath("C:\\Users\\zrdra\\gitRepositories\\Horse-Lesson-Planner\\PythonScheduler\\Testing"))

from Classes.Horse import *
from Classes.Rider import *
from Classes.Weekly_Schedule import *


def main():
    Schedule = Weekly_Schedule()
    Schedule.add_horse(Horse("Kitty"))
    Schedule.add_horse(Horse("Spotty",leaser="Sammy"))
    Schedule.add_rider(Rider("Sammy", None, 60, 150, 0, None, 0))
    Schedule.add_rider(Rider("Ryan", None, 60, 150, 0, None, 0))
    Schedule.add_lesson("Sammy", "Monday", 8, 30, True)
    Schedule.add_lesson("Ryan", "Tuesday", 10, 60, False)
    Schedule.add_lesson("Ryan", "Monday", 10, 60, False)
    Schedule.add_lesson("Ryan", "Monday", 8, 60, True)
    Schedule.add_lesson("Sammy", "Monday", 18, 30, True)
    Schedule.add_lesson("Sammy", "Wednesday", 8, 30, True)
    Schedule.make_schedule()
    for horse in Schedule.get_horses():
        print(horse)
    for rider in Schedule.get_riders():
        print(rider)
    print("\n\n")
    print(Schedule)
    print(Schedule.get_horse("Spotty"))
    print(Schedule.get_horse("Kitty"))

if __name__ == "__main__":
    main()


