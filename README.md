# Horse Lesson Planner

Welcome to the Horse Lesson Planner application! This program helps you manage horses, riders, and lessons efficiently with an easy-to-use GUI.

## Features
- Upload and manage horse and rider data.
- Add and remove horses and riders.
- Schedule and manage lessons.
- Automatically generate weekly schedules based on availability and skill levels.
- View and interact with the schedule using a graphical interface.

## Getting Started

### 1. Starting the App
- Open the app by running the Python script (`main.py`).
- Once launched, the main screen will display a **Welcome Message** with an **"Enter"** button.

### 2. Uploading Data
Before generating a schedule, upload the necessary data files.

#### Upload Horse Data
1. Click on the **"Upload Horse Data"** button.
2. Select a file containing horse information. Supported formats: `.csv`, `.xlsx`, or `.xls`.
    - Example file: `HorseData.csv`
3. A confirmation message will appear, showing a preview of the uploaded data.
4. The app will automatically process the horse data.
    - Data processing details can also be viewed in the Python terminal.

#### Upload Rider Data
1. Click on the **"Upload Rider Data"** button.
2. Select a file containing rider information.
    - Example file: `RiderData.csv`
3. A confirmation message will appear, showing a preview of the uploaded data.
4. The app will automatically process the rider data.
    - Data processing details can also be viewed in the Python terminal.

### 3. Managing Horses and Riders
The app allows you to manage horse and rider information directly.

#### Add a New Horse
1. Click **"Add Horse"** to open the Add Horse window.
2. Fill in the details:
    - Name
    - Maximum Weight
    - Skill Level (e.g., `B`, `N`, `I`, `O`, or combinations like `B-N` or `N-I-O`)
    - Jumper status (yes/no)
    - Maximum Rides Per Day
    - Leaser (optional)
3. Click **"Add Horse"** to save the horse to the system.

#### Remove a Horse
1. Click **"Remove Horse"**.
2. Enter the name of the horse you want to remove.
**Warning**: Removing too many horses or key horses may lead to issues generating a valid schedule.

#### Add a New Rider
1. Click **"Add Rider"** to open the Add Rider window.
2. Fill in the details:
    - Name
    - Weight
    - Skill Level (e.g., `B`, `N`, `I`, `O`, or combinations like `B-N` or `N-I-O`)
3. Click **"Add Rider"** to save the rider to the system.

#### Remove a Rider
1. Click **"Remove Rider"** and input the name of the rider you wish to remove.
2. Confirm the action.

### 4. Adding Lessons
1. Click **"Add Lesson"** to schedule a lesson for a rider.
2. In the lesson form:
    - Select a rider’s name from the dropdown list.
    - Choose a day of the week for the lesson.
    - Select whether it’s a jumping or non-jumping lesson.
    - Specify the duration of the lesson (30 or 60 minutes).
    - Set the lesson start time (using the hour, minute, and AM/PM selectors).
3. Click **"Add Lesson"** to save the lesson.

### 5. Generating the Weekly Schedule
1. After uploading all necessary data and adding lessons, click **"Generate Schedule"**.
2. The app will process the information to assign horses to riders based on availability and skill levels.
3. If the schedule generation fails (e.g., due to conflicts), it will retry automatically or display an error.

### 6. Viewing the Weekly Schedule
1. Once the schedule is generated, the app will display it on the screen:
    - Each day of the week is listed.
    - Under each day, the scheduled times, riders, and assigned horses are displayed.
2. Use the scroll bar to view all days and entries.

### 7. Going Back
- Click the **"Back"** button to return to the main menu or the data upload screen.

### 8. Closing the App
- Simply close the application window when done.
