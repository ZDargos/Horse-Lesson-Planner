# Zack Dragos & Sampath Reddy M.


from PythonScheduler.Classes.Horse import *
from PythonScheduler.Classes.Rider import *
from PythonScheduler.Classes.Daily_Schedule import *
from PythonScheduler.Classes.Weekly_Schedule import *


def main():
    Schedule = Weekly_Schedule()
    Schedule.add_horse(Horse("Kitty"))
    Schedule.add_horse(Horse("Spotty"))
    Schedule.add_rider(Rider("Sammy", None, 60, 150, 0, None, 0))


if __name__ == "__main__":
    main()


