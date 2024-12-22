# Author: Zack Dragos, Sampath Reddy M., Palak Sood
# Date: 12/13/24
# Description: File storing all of the functionality of the application. The usage of tkinter and culmination of the app

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import pandas as pd
from PIL import Image, ImageTk  # Ensure Pillow is installed
from tkinter import StringVar
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Add these lines as per your current working directory setup to import classes
import sys
import os

print(os.getcwd()[:-11])  # prints the current working directory path
sys.path.append(os.path.abspath(os.getcwd()[:-11]))
from Classes.Horse import *
from Classes.Rider import *
from Classes.Weekly_Schedule import *
from Classes.Data_Manipulation import *

class App(tk.Tk):
    def __init__(self):
        '''
        Initializes the App class, setting up the main application window with its title, dimensions, background image, and default states for data and schedule.
        :return: None
        '''
        super().__init__()
        self.title("Welcome")
        self.geometry("600x800")
        self.resizable(True, True)

        self.bg_label = tk.Label(self)
        self.bg_label.place(relwidth=1, relheight=1)

        self.background_image = None
        self.after(1, self.initialize_background_image)
        self.bind("<Configure>", self.resize_background)

        self.schedule = Weekly_Schedule()
        self.data_manipulator = Data_Manipulation(".data/rider_data.pkl", ".data/horse_data.pkl")
        self.load_saves()

        self.welcome_screen()

        self.active_window = self

        self.schedule_displayed = False

    def initialize_background_image(self):
        '''
        Loads and sets the background image for the application window, resizing it to fit the window dimensions.
        :return: None
        '''
        try:
            self.image_path = "bg.jpg"  # Ensure this image file is present in the directory
            self.original_image = Image.open(self.image_path)
            self.resize_background()
        except Exception as e:
            print(f"Error loading background image: {e}")

    def resize_background(self, event=None):
        '''
        Adjusts the background image dimensions dynamically when the application window is resized.
        :return: None
        '''
        if not hasattr(self, 'original_image'):
            return
        resized_image = self.original_image.resize((self.winfo_width(), self.winfo_height()), Image.Resampling.LANCZOS) #ensure background fits frame size
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.bg_label.config(image=self.background_image)

    def welcome_screen(self):
        '''
        Displays the welcome screen of the application, with a title and an "Enter" button to navigate to the file upload screen.
        :return: None
        '''
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
        '''
        Displays the file upload screen, allowing the user to upload horse and rider data, and navigate to other functionalities such as adding or removing entities.
        :return: None
        '''
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.active_window = self

        self.bg_label.config(image=self.background_image)

        instruction_label = tk.Label(self, text="Please upload Horse and Rider data files:", font=("Arial", 14),
                                     bg="white")
        instruction_label.pack(pady=20)

        upload_button = tk.Button(self, text="Upload Horse Data", command=self.upload_horse_data, font=("Arial", 14),
                                  bg="white", fg="black")
        upload_button.pack(pady=10)

        upload_rider_button = tk.Button(self, text="Upload Rider Data", command=self.upload_rider_data_from_excel,
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
        
        remove_rider_button = tk.Button(self, text="Remove Rider", command=self.remove_rider, font=("Arial", 14), bg="white",
                                     fg="black")
        remove_rider_button.pack(pady=10)

        add_lesson_button = tk.Button(self, text="Add Lesson", command=self.add_lesson, font=("Arial", 14), bg="white",
                                     fg="black")
        add_lesson_button.pack(pady=10)

        generate_schedule_button = tk.Button(self, text="Generate Schedule", command=self.process_schedule, font=("Arial", 14), bg="white",
                                fg="black")
        generate_schedule_button.pack(pady=10)

        show_schedule_button = tk.Button(self, text="Show Schedule", command=lambda: self.show_schedule(self.schedule),font=("Arial", 14), bg="white",
                                         fg="black")
        show_schedule_button.pack(pady=10)

        back_button = tk.Button(self, text="Back", command=self.welcome_screen, font=("Arial", 12), bg="white",
                                fg="black")
        back_button.pack(pady=10)

    def load_saves(self):
        self.data_manipulator.load_riders_from_pickle(self.schedule)
        self.data_manipulator.load_horses_from_pickle(self.schedule)
    def upload_horse_data(self):
        '''
        Prompts the user to select and upload a file containing horse data in CSV or Excel format, and processes the file for use within the application.
        :return: None
        '''
        file_path = filedialog.askopenfilename(
            title="Select Horse Data File",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls")]
        )
        self.data_manipulator.load_horses_from_excel(file_path, self.schedule)


    def upload_rider_data_from_excel(self):
        '''
        Prompts the user to select and upload a file containing rider data in CSV or Excel format, and processes the file for use within the application.
        :return: None
        '''
        file_path = filedialog.askopenfilename(
            title="Select Rider Data File",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls")]
        )
        self.data_manipulator.load_riders_from_excel(file_path, self.schedule)


    def save_rider_data(self):
        self.data_manipulator.save_riders_to_pickle(self.schedule.get_riders())

    def save_horse_data(self):
        self.schedule.reset_horses()
        self.data_manipulator.save_horses_to_pickle(self.schedule.get_horses())

    def add_horse(self):
        '''
        Opens a new window to add a new horse to the schedule, with fields for the horse's name, attributes, and optional leaser.
        :return: None
        '''
        add_horse_window = tk.Toplevel(self)
        add_horse_window.title("Add Horse")
        add_horse_window.geometry("400x450")

        self.active_window = add_horse_window

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
        '''
        Opens a new window to add a new rider to the schedule, with fields for the rider's name, weight, and skill level.
        :return: None
        '''
        add_rider_window = tk.Toplevel(self)
        add_rider_window.title("Add Rider")
        add_rider_window.geometry("400x400")

        self.active_window = add_rider_window

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

    def add_lesson(self):
        '''
        Opens a new window to add a new lesson to the schedule, with options to select the rider, day, time, type of lesson, and duration.
        :return: None
        '''
        add_lesson_window = tk.Toplevel(self)
        add_lesson_window.title("Add Lesson")
        add_lesson_window.geometry("400x400")

        self.active_window = add_lesson_window

        rider_name_option = StringVar()
        riders = [r.get_name() for r in self.schedule.get_riders()]

        if len(riders) == 0:
            riders = ["No Riders"]
        rider_name_option.set(riders[0])

        tk.Label(add_lesson_window, text="Name Of Rider:").pack(pady=2)
        rider_options = tk.OptionMenu(add_lesson_window, rider_name_option, *riders)
        rider_options.pack(pady=10)

        days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        day_option = StringVar()

        day_option.set(days_of_week[0])
        tk.Label(add_lesson_window, text="Day of week:").pack(pady=2)
        day_options = tk.OptionMenu(add_lesson_window, day_option, *days_of_week)
        day_options.pack(pady=10)

        tk.Label(add_lesson_window, text="Type of lesson:").pack(pady=2)
        jump_var = StringVar()
        jump_var.set("Jumping")
        jumping_lesson_dropdown = ttk.Combobox(add_lesson_window, textvariable=jump_var, values=["Jumping", "Not Jumping"], width=10,
                                     font=("Arial", 12),
                                     state="readonly")
        jumping_lesson_dropdown.pack(pady=10)

        tk.Label(add_lesson_window, text="Duration of Lesson (in minutes):").pack(pady=2)
        duration_var = StringVar()
        duration_var.set("30")
        duration_dropdown = ttk.Combobox(add_lesson_window, textvariable=duration_var,
                                               values=["30", "60"], width=5,
                                               font=("Arial", 12),
                                               state="readonly")
        duration_dropdown.pack(pady=10)

        def get_time():
            if ampm_var.get() == "AM":
              if int(hour_var.get()) < 10:
                  return f"0{hour_var.get()}{minute_var.get()}"
              return f"{hour_var.get()}{minute_var.get()}"
            return f"{int(hour_var.get())+12}{minute_var.get()}"

        # Variables for hours, minutes, and AM/PM
        hour_var = tk.StringVar(value="12")
        minute_var = tk.StringVar(value="00")
        ampm_var = tk.StringVar(value="AM")

        # Hour Spinbox (1 to 12)
        hour_spinbox = ttk.Spinbox(add_lesson_window, from_=1, to=12, wrap=True, textvariable=hour_var, width=5, font=("Arial", 12))
        hour_spinbox.pack(side=tk.LEFT, padx=10,pady=10)

        # Minute Spinbox (0 to 59)
        minute_spinbox = ttk.Spinbox(add_lesson_window, from_=0, to=59, wrap=True, textvariable=minute_var, format="%02.0f", width=5,
                                     font=("Arial", 12))
        minute_spinbox.pack(side=tk.LEFT, padx=5, pady=10)

        # AM/PM Dropdown
        ampm_dropdown = ttk.Combobox(add_lesson_window, textvariable=ampm_var, values=["AM", "PM"], width=5, font=("Arial", 12),
                                     state="readonly")
        ampm_dropdown.pack(side=tk.LEFT, padx=5, pady=10)


        def submit_lesson():
            try:
                rider = rider_name_option.get()
                time = get_time()
                day = day_option.get()
                duration = int(duration_var.get())
                jumper = True if jump_var.get() == "Jumping" else False

                self.schedule.add_lesson(rider,day,time,duration,jumper)
                messagebox.showinfo("Success", f"Lesson added successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add rider: {e}")

        tk.Button(add_lesson_window, text="Add Lesson", command=submit_lesson).pack(pady=20)
    def remove_horse(self):
        '''
        Prompts the user to enter the name of a horse to remove from the schedule and processes the removal.
        :return: None
        '''
        try:
            name = simpledialog.askstring("Remove Horse", "Enter Horse to Remove:")
            removed = self.schedule.remove_horse(name)
            if removed:
                messagebox.showinfo("Horse Removed", f"{name} successfully removed from the schedule.")
            else:
                messagebox.showwarning("Not Found", f"Horse named {name} not found in the schedule.")
        except Exception as e:
            messagebox.showerror("Error", f"Error removing horse: {e}")

    def remove_rider(self):
        '''
        Prompts the user to enter the name of a rider to remove from the schedule and processes the removal.
        :return: None
        '''
        try:
            name = simpledialog.askstring("Remove Rider", "Enter Rider Name to Remove:")
            removed = self.schedule.remove_rider(name)
            if removed:
                messagebox.showinfo("Rider Removed", f"{name} successfully removed from the schedule.")
            else:
                messagebox.showwarning("Not Found", f"Rider named {name} not found in the schedule.")
        except Exception as e:
            messagebox.showerror("Error", f"Error removing rider: {e}")

    def process_schedule(self):
        '''
        Attempts to generate a weekly schedule for lessons based on the input data, retrying multiple times in case of conflicts.
        :return: None
        '''

        try:
            attempts = 0
            while attempts < 50:
                try:
                    attempts += 1
                    print(f"Attempt {attempts} - Generating schedule...")
                    self.schedule.make_schedule()
                    print(self.schedule)
                    break
                except Exception as e:
                    print(f"Error during schedule generation (Attempt {attempts}): {e}")
            if self.schedule_displayed:
                self.show_schedule(self.schedule)
            else:
                messagebox.showinfo("Success", "Successfully created schedule!")
            if attempts == 1000:
                raise Exception("Failed to generate a working schedule.")



        except Exception as e:
            messagebox.showerror("Error", f"Error generating schedule: {e}")

    def show_schedule(self, schedule):
        '''
        Displays the generated weekly schedule, adjusting layout dynamically based on window state (maximized or normal).
        :param schedule: an instance of the Weekly_Schedule class containing the schedule data
        :return: None
        '''
        self.schedule_displayed = True
        self.schedule_data = schedule  # Save the schedule data for re-rendering
        self.current_state = self.state()  # Track the current window state

        # Bind the window's configure event to update layout dynamically
        self.bind("<Configure>", self.on_window_resize)

        # Render the initial layout
        self.render_schedule_layout()

    def on_window_resize(self, event):
        '''
        Handles window resize events and updates the schedule layout if the window state changes.
        :param event: The event triggered by resizing the window.
        :return: None
        '''
        # Check if the current screen is the schedule screen before updating
        if hasattr(self, "schedule_data"):
            new_state = self.state()
            if new_state != self.current_state:  # Only update if the state (e.g., maximized) changes
                self.current_state = new_state
                self.render_schedule_layout()

    def render_schedule_layout(self):
        '''
        Renders the schedule layout dynamically based on the current window state.
        :return: None
        '''
        # Clear all widgets except the background label
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)

        # Header and control buttons
        generate_schedule_button = tk.Button(self, text="Re-Generate Schedule", command=self.process_schedule,
                                             font=("Arial", 14), bg="white", fg="black")
        generate_schedule_button.pack(pady=10)

        schedule_label = tk.Label(self, text="Weekly Schedule", font=("Arial", 16), bg="white")
        schedule_label.pack(pady=20)

        export_button = ttk.Button(self, text="Save to PDF", command=self.export_schedule_as_pdf)
        export_button.pack(pady=10)

        is_maximized = self.state() == 'zoomed'

        if is_maximized:
            # Multi-column layout with horizontal scrolling
            outer_canvas = tk.Canvas(self, bg="white")
            x_scrollbar = tk.Scrollbar(self, orient="horizontal", command=outer_canvas.xview)
            outer_frame = tk.Frame(outer_canvas, bg="white")
            self.resize_background()

            outer_frame.bind(
                "<Configure>",
                lambda e: outer_canvas.configure(scrollregion=outer_canvas.bbox("all"))
            )
            outer_canvas.create_window((0, 0), window=outer_frame, anchor="nw")
            outer_canvas.configure(xscrollcommand=x_scrollbar.set)

            outer_canvas.pack(side="top", fill="both", expand=True)
            x_scrollbar.pack(side="bottom", fill="x")

            for col, (day, daily_schedule) in enumerate(self.schedule_data._planner.items()):
                day_frame = tk.Frame(outer_frame, bg="white", borderwidth=2, relief="groove")
                day_frame.grid(row=0, column=col, padx=10, pady=10, sticky="n")

                day_label = tk.Label(day_frame, text=f"{day}:", font=("Arial", 14, "bold"), bg="white")
                day_label.pack(anchor="w", padx=10, pady=5)

                planner = daily_schedule.get_planner()
                if planner:
                    for time, lessons in sorted(planner.items()):
                        time_label = tk.Label(day_frame, text=f"  {daily_schedule.military_to_standard(time)}",
                                              font=("Arial", 12), bg="white")
                        time_label.pack(anchor="w", padx=20)

                        for rider, horse in lessons:
                            lesson_label = tk.Label(day_frame,
                                                    text=f"    Rider: {rider} | Horse: {horse if horse else 'TBD'}",
                                                    font=("Arial", 10), bg="white")
                            lesson_label.pack(anchor="w", padx=40)
                else:
                    no_schedule_label = tk.Label(day_frame, text="  No lessons scheduled.",
                                                 font=("Arial", 10, "italic"), bg="white")
                    no_schedule_label.pack(anchor="w", padx=20)
        else:
            # Single-column scrollable layout for normal state
            canvas = tk.Canvas(self, bg="white")
            scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for day, daily_schedule in self.schedule_data._planner.items():
                day_label = tk.Label(scrollable_frame, text=f"{day}:", font=("Arial", 14, "bold"), bg="white")
                day_label.pack(anchor="w", padx=10, pady=5)

                planner = daily_schedule.get_planner()
                if planner:
                    for time, lessons in sorted(planner.items()):
                        time_label = tk.Label(scrollable_frame, text=f"  {daily_schedule.military_to_standard(time)}",
                                              font=("Arial", 12), bg="white")
                        time_label.pack(anchor="w", padx=20)

                        for rider, horse in lessons:
                            lesson_label = tk.Label(scrollable_frame,
                                                    text=f"    Rider: {rider} | Horse: {horse if horse else 'TBD'}",
                                                    font=("Arial", 10), bg="white")
                            lesson_label.pack(anchor="w", padx=40)
                else:
                    no_schedule_label = tk.Label(scrollable_frame, text="  No lessons scheduled.",
                                                 font=("Arial", 10, "italic"), bg="white")
                    no_schedule_label.pack(anchor="w", padx=20)

        back_button = tk.Button(self, text="Back", command=self.leave_schedule_screen, font=("Arial", 12), bg="#f44336",
                                fg="black")
        back_button.pack(pady=20)

    def leave_schedule_screen(self):
        '''
        Unbinds the resize event and navigates away from the schedule screen.
        :return: None
        '''
        self.unbind("<Configure>")  # Unbind resize event
        self.file_upload_screen()  # Navigate to the file upload screen
        self.schedule_displayed = False

    def upload_riders(self, rider_data):
        '''
        Processes uploaded rider data and integrates it into the application, adding horses to the schedule as needed.
        :param rider_data: DataFrame containing the uploaded rider data
        :return: None
        '''
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

            self.schedule.add_rider(Rider(
                row['Name'],
                weight=int(row['Weight']),
                skill_level=row['Skill Level'],
                weekly_schedule=weekly_schedule
            ))
        for rider in self.schedule.get_riders():
            print(rider)

    def export_schedule_as_pdf(self):
        response = messagebox.askokcancel("Are you sure", "Rider and horse data will be updated. Are you sure you want to go with this schedule?")
        if not response:
            return 1
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            pdf = canvas.Canvas(file_path, pagesize=letter)
            pdf.setFont("Helvetica", 14)
            left_margin = 50
            right_margin = 300
            column_gap = 20
            y_position = 750
            current_column = left_margin

            # Title
            pdf.drawString(250, y_position, "Weekly Schedule")
            y_position -= 30

            for day, daily_schedule in self.schedule._planner.items():
                # Estimate height needed for the day's content
                planner = daily_schedule.get_planner()
                lines_needed = 1  # For the day header
                if planner:
                    for time, details in sorted(planner.items()):
                        lines_needed += 1  # Time header
                        lines_needed += len(details)  # Each lesson
                else:
                    lines_needed += 1  # "No lessons scheduled" message

                # Estimate required space (15 units per line)
                space_needed = lines_needed * 15 + 10  # Add padding between days

                # Check if there's enough space in the current column
                if y_position - space_needed < 50:
                    if current_column == left_margin:
                        # Switch to the right column
                        current_column = right_margin
                        y_position = 720
                    else:
                        # Move to a new page
                        pdf.showPage()
                        pdf.setFont("Helvetica", 14)
                        current_column = left_margin
                        y_position = 720

                # Add day header
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(current_column, y_position, f"{day}:")
                y_position -= 20

                if planner:
                    for time, details in sorted(planner.items()):
                        # Add time
                        pdf.setFont("Helvetica", 12)
                        pdf.drawString(current_column + 20, y_position, f"{daily_schedule.military_to_standard(time)}:")
                        y_position -= 15

                        for rider, horse in details:
                            # Add rider and horse details
                            horse_name = horse if horse else "TBD"
                            pdf.setFont("Helvetica", 10)
                            pdf.drawString(current_column + 40, y_position, f"Rider: {rider} | Horse: {horse_name}")
                            y_position -= 15
                else:
                    # Add "No lessons scheduled" message
                    pdf.setFont("Helvetica-Oblique", 10)
                    pdf.drawString(current_column + 20, y_position, "No lessons scheduled.")
                    y_position -= 15

                # Add spacing between days
                y_position -= 10

            pdf.save()
            messagebox.showinfo("Success", f"Schedule exported as PDF to {file_path}")
            self.save_rider_data()
            self.save_horse_data()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export schedule: {e}")


# Application entry
if __name__ == "__main__":
    app = App()
    app.mainloop()
