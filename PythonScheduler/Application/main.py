import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
from PIL import Image, ImageTk  # Ensure Pillow is installed

# Add these lines as per your current working directory setup to import classes
import sys
import os

print(os.getcwd()[:-11])  # prints the current working directory path
sys.path.append(os.path.abspath(os.getcwd()[:-11]))
from Classes.Horse import *
from Classes.Rider import *
from Classes.Weekly_Schedule import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome")
        self.geometry("600x400")
        self.resizable(True, True)

        self.bg_label = tk.Label(self)
        self.bg_label.place(relwidth=1, relheight=1)

        self.background_image = None
        self.after(1, self.initialize_background_image)
        self.bind("<Configure>", self.resize_background)

        self.schedule = Weekly_Schedule()
        self.horse_data = None
        self.rider_data = None
        self.welcome_screen()

    def initialize_background_image(self):
        try:
            self.image_path = "temp-bg.jpg"  # Ensure this image file is present in the directory
            self.original_image = Image.open(self.image_path)
            self.resize_background()
        except Exception as e:
            print(f"Error loading background image: {e}")

    def resize_background(self, event=None):
        if not hasattr(self, 'original_image'):
            return
        resized_image = self.original_image.resize((self.winfo_width(), self.winfo_height()), Image.Resampling.LANCZOS)
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.bg_label.config(image=self.background_image)

    def welcome_screen(self):
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)

        welcome_label = tk.Label(self, text="Welcome to the Horse Lesson Scheduler", font=("Arial", 16), bg="white")
        welcome_label.pack(pady=50)

        enter_button = tk.Button(self, text="Enter", command=self.file_upload_screen, font=("Arial", 14), bg="white",
                                 fg="black")
        enter_button.pack(pady=20)

    def file_upload_screen(self):
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)

        instruction_label = tk.Label(self, text="Please upload Horse and Rider data files:", font=("Arial", 14),
                                     bg="white")
        instruction_label.pack(pady=20)

        upload_button = tk.Button(self, text="Upload Horse Data", command=self.upload_horse_data, font=("Arial", 14),
                                  bg="white", fg="black")
        upload_button.pack(pady=10)

        upload_rider_button = tk.Button(self, text="Upload Rider Data", command=self.upload_rider_data,
                                        font=("Arial", 14), bg="white", fg="black")
        upload_rider_button.pack(pady=10)

        add_horse_button = tk.Button(self, text="Add Horse", command=self.add_horse, font=("Arial", 14), bg="white",
                                     fg="black")
        add_horse_button.pack(pady=10)

        remove_horse_button = tk.Button(self, text="Remove Horse", command=self.remove_horse, font=("Arial", 14),
                                        bg="white", fg="black")
        remove_horse_button.pack(pady=10)

        add_rider_button = tk.Button(self, text="Add Rider", command=self.add_rider, font=("Arial", 14), bg="white",
                                     fg="black")
        add_rider_button.pack(pady=10)

        back_button = tk.Button(self, text="Back", command=self.welcome_screen, font=("Arial", 12), bg="white",
                                fg="black")
        back_button.pack(pady=10)

    def upload_horse_data(self):
        file_path = filedialog.askopenfilename(
            title="Select Horse Data File",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            try:
                self.horse_data = pd.read_excel(file_path) if file_path.endswith(('.xlsx', '.xls')) else pd.read_csv(
                    file_path)
                messagebox.showinfo("Horse Data Selected",
                                    f"Horse data successfully uploaded.\n\nData Preview:\n{self.horse_data.head()}")
            except Exception as e:
                messagebox.showerror("Error", f"Error reading horse data file: {e}")
        else:
            messagebox.showwarning("No File Selected", "Please select a valid horse data file.")

    def upload_rider_data(self):
        file_path = filedialog.askopenfilename(
            title="Select Rider Data File",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            try:
                self.rider_data = pd.read_excel(file_path) if file_path.endswith(('.xlsx', '.xls')) else pd.read_csv(
                    file_path)
                messagebox.showinfo("Rider Data Selected",
                                    f"Rider data successfully uploaded.\n\nData Preview:\n{self.rider_data.head()}")
                self.process_schedule(self.horse_data, self.rider_data)
            except Exception as e:
                messagebox.showerror("Error", f"Error reading rider data file: {e}")
        else:
            messagebox.showwarning("No File Selected", "Please select a valid rider data file.")

    def add_horse(self):
        add_horse_window = tk.Toplevel(self)
        add_horse_window.title("Add Horse")
        add_horse_window.geometry("400x450")

        tk.Label(add_horse_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(add_horse_window)
        name_entry.pack(pady=5)

        tk.Label(add_horse_window, text="Max Weight:").pack(pady=5)
        max_weight_entry = tk.Entry(add_horse_window)
        max_weight_entry.pack(pady=5)

        tk.Label(add_horse_window, text="Skill Level:").pack(pady=5)
        skill_level_entry = tk.Entry(add_horse_window)
        skill_level_entry.pack(pady=5)

        tk.Label(add_horse_window, text="Is Jumper (yes/no):").pack(pady=5)
        is_jumper_entry = tk.Entry(add_horse_window)
        is_jumper_entry.pack(pady=5)

        tk.Label(add_horse_window, text="Max Rides per Day:").pack(pady=5)
        max_rides_entry = tk.Entry(add_horse_window)
        max_rides_entry.pack(pady=5)

        tk.Label(add_horse_window, text="Leaser (optional):").pack(pady=5)
        leaser_entry = tk.Entry(add_horse_window)
        leaser_entry.pack(pady=5)

        def submit_horse():
            try:
                name = name_entry.get()
                max_weight = int(max_weight_entry.get())
                skill_level = skill_level_entry.get()
                is_jumper = is_jumper_entry.get().strip().lower() == "yes"
                max_rides = int(max_rides_entry.get())
                leaser = leaser_entry.get() or ""

                new_horse = Horse(name, is_jumping_horse=is_jumper, max_weight=max_weight, skill_level=skill_level,
                                  max_daily_jumps=max_rides, leaser=leaser)
                self.schedule.add_horse(new_horse)
                messagebox.showinfo("Success", f"Horse '{name}' added successfully.")
                add_horse_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add horse: {e}")

        tk.Button(add_horse_window, text="Add Horse", command=submit_horse).pack(pady=20)

    def add_rider(self):
        add_rider_window = tk.Toplevel(self)
        add_rider_window.title("Add Rider")
        add_rider_window.geometry("400x400")

        tk.Label(add_rider_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(add_rider_window)
        name_entry.pack(pady=5)

        tk.Label(add_rider_window, text="Weight:").pack(pady=5)
        weight_entry = tk.Entry(add_rider_window)
        weight_entry.pack(pady=5)

        tk.Label(add_rider_window, text="Skill Level:").pack(pady=5)
        skill_level_entry = tk.Entry(add_rider_window)
        skill_level_entry.pack(pady=5)

        def submit_rider():
            try:
                name = name_entry.get()
                weight = int(weight_entry.get())
                skill_level = skill_level_entry.get()

                new_rider = Rider(name, weight=weight, skill_level=skill_level, weekly_schedule=[])
                self.schedule.add_rider(new_rider)
                messagebox.showinfo("Success", f"Rider '{name}' added successfully.")
                add_rider_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add rider: {e}")

        tk.Button(add_rider_window, text="Add Rider", command=submit_rider).pack(pady=20)

    def remove_horse(self):
        # Placeholder for remove horse functionality
        pass

    def remove_rider(self):
        try:
            name = simpledialog.askstring("Remove Rider", "Enter Rider Name to Remove:")
            removed = self.schedule.remove_rider(name)
            if removed:
                messagebox.showinfo("Rider Removed", f"{name} successfully removed from the schedule.")
            else:
                messagebox.showwarning("Not Found", f"Rider named {name} not found in the schedule.")
        except Exception as e:
            messagebox.showerror("Error", f"Error removing rider: {e}")

    def process_schedule(self, horse_data, rider_data):
        try:
            schedule = Weekly_Schedule()

            self.upload_horses(horse_data, schedule)
            self.upload_riders(rider_data, schedule)

            attempts = 0
            while attempts < 1000:
                try:
                    attempts += 1
                    print(f"Attempt {attempts} - Generating schedule...")
                    schedule.make_schedule()
                    print(schedule)
                    break
                except Exception as e:
                    print(f"Error during schedule generation (Attempt {attempts}): {e}")

            if attempts == 1000:
                raise Exception("Failed to generate a working schedule.")

            self.show_schedule(schedule)
        except Exception as e:
            messagebox.showerror("Error", f"Error generating schedule: {e}")

    def show_schedule(self, schedule):
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)

        schedule_label = tk.Label(self, text="Generated Schedule", font=("Arial", 16), bg="white")
        schedule_label.pack(pady=20)

        for horse in schedule.get_horses():
            horse_label = tk.Label(self, text=f"Horse: {horse.get_name()}", font=("Arial", 12), bg="white")
            horse_label.pack(pady=5)

        for rider in schedule.get_riders():
            rider_label = tk.Label(self, text=f"Rider: {rider.get_name()}", font=("Arial", 12), bg="white")
            rider_label.pack(pady=5)

        back_button = tk.Button(self, text="Back", command=self.welcome_screen, font=("Arial", 12), bg="#f44336",
                                fg="black")
        back_button.pack(pady=20)

    def upload_horses(self, horse_data, schedule):
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

    def upload_riders(self, rider_data, schedule):
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


# Application entry
if __name__ == "__main__":
    app = App()
    app.mainloop()
