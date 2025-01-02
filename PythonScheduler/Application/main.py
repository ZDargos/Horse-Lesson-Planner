# Author: Zack Dragos, Sampath Reddy M., Palak Sood
# Date: 12/13/24
# Description: File storing all of the functionality of the application. The usage of tkinter and culmination of the app

import importlib.util
import subprocess
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk, StringVar

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk, StringVar
from PIL import Image, ImageTk  # Ensure Pillow is installed
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Add these lines as per your current working directory setup to import classes
import sys
import os
# def check_and_install(package_name, import_name=None):
#     """
#     Checks if a package is installed and installs it if missing.
#     :param package_name: The name of the package for pip installation.
#     :param import_name: The name used to import the package (if different from package_name).
#     """
#     if import_name is None:
#         import_name = package_name
#
#     if importlib.util.find_spec(import_name) is None:
#         print(f"{import_name} not found. Installing {package_name}...")
#         subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
#     else:
#         print(f"{import_name} is already installed.")
#
# # Check and install required libraries
# libraries = [
#     ("tkinter", "tkinter"),  # Built-in, no pip installation needed
#     ("Pillow", "PIL"),       # Pillow for Image, ImageTk
#     ("reportlab", "reportlab"),  # ReportLab for PDF generation
#     ("pandas", "pandas")
# ]
#
# for package, import_name in libraries:
#     if package == "tkinter":
#         # Tkinter is built-in for most Python distributions; verify installation
#         try:
#             import tkinter
#             print("tkinter is installed.")
#         except ImportError:
#             print("tkinter is missing. Please install a Python distribution with tkinter included.")
#     else:
#         check_and_install(package, import_name)
from PIL import Image, ImageTk
# Check for additional imports
# additional_imports = ["StringVar"]
# for additional in additional_imports:
#     try:
#         exec(f"from tkinter import {additional}")
#         print(f"{additional} is available in tkinter.")
#     except ImportError:
#         print(f"{additional} could not be imported from tkinter.")



print(os.getcwd()[:-11])  # prints the current working directory path
sys.path.append(os.path.abspath(os.getcwd()[:-11]))
from Classes.Horse import *
from Classes.Rider import *
from Classes.Weekly_Schedule import *
from Classes.Data_Manipulation import *

app_font = "Times New Roman"
accept_color = "#1d9bf0"
back_color = "#71767b"
m_frame_color = "#000000"
text_color = "#e7e9ea"


class App(tk.Tk):
    def __init__(self):
        '''
        Initializes the App class, setting up the main application window with its title, dimensions, background image, and default states for data and schedule.
        :return: None
        '''
        super().__init__()
        self.title("Welcome")
        self.geometry("710x800")
        self.resizable(True, True)

        self.bg_label = tk.Label(self)
        self.bg_label.place(relwidth=1, relheight=1)

        self.background_image = None
        self.after(1, self.initialize_background_image)
        self.bind("<Configure>", self.resize_background)


        self.schedule = Weekly_Schedule()
        self.data_manipulator = Data_Manipulation(".data/rider_data.pkl", ".data/horse_data.pkl", ".data/options.txt")
        self.display_font_size = 13
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
            self.image_path = "bg6.jpg"  # Ensure this image file is present in the directory
            self.original_image = Image.open(self.image_path)
            self.resize_background()
        except Exception as e:
            print(f"Error loading background image: {e}")

    def resize_background(self, event=None):
        '''
        Adjusts the background image dimensions dynamically when the application window is resized.
        :return: None
        '''
        if not hasattr(self, 'original_image') or not hasattr(self, 'bg_label') or not self.bg_label.winfo_exists():
            return
        resized_image = self.original_image.resize((self.winfo_width(), self.winfo_height()), Image.Resampling.LANCZOS)
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
        self.resize_background()



        welcome_label = tk.Label(self, text="Welcome to the Horse Lesson Scheduler", font=(app_font, self.display_font_size+3), bg=m_frame_color, borderwidth=-10, fg=text_color)
        welcome_label.pack(pady=50)

        enter_button = tk.Button(self, text="Enter", command=self.pseudo_solve_speed, font=(app_font, self.display_font_size+1), bg="white",
                                 fg="black")
        enter_button.pack(pady=20)



    def file_upload_screen(self):
        '''
        Displays the file upload screen, allowing the user to upload horse and rider data, and navigate to other functionalities such as adding or removing entities.
        :return: None
        '''
        button_color = ""
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.active_window = self

        self.bg_label.config(image=self.background_image)
        self.resize_background()

        instruction_label = tk.Label(self, text="Main Operation", font=(app_font, 14, "bold"),
                                     bg=m_frame_color, fg=text_color)
        instruction_label.pack(pady=20)

        ''' Testing buttons, uncomment for quick upload of rider data
        
        upload_button = tk.Button(self, text="Upload Horse Data", command=self.upload_horse_data, font=(app_font, self.display_font_size+1),
                                  bg="white", fg="black")
        upload_button.pack(pady=10)

        upload_rider_button = tk.Button(self, text="Upload Rider Data", command=self.upload_rider_data_from_excel,
                                        font=(app_font, self.display_font_size+1), bg="white", fg="black")
        upload_rider_button.pack(pady=10)
                
        '''

        tk.Button(self, text="Riders", command=self.display_all_riders, font=(app_font, self.display_font_size+1), bg="white", fg="black").pack(pady=10)

        tk.Button(self, text="Horses", command=self.display_all_horses, font=(app_font, self.display_font_size+1), bg="white",
                  fg="black").pack(pady=10)

        view_all_lessons_button = tk.Button(self, text="Lessons", command=self.display_lessons_by_day,
                                            font=(app_font, self.display_font_size+1), bg="white",
                                            fg="black")
        view_all_lessons_button.pack(pady=10)

        add_lesson_button = tk.Button(self, text="Add Lesson", command=self.add_lesson, font=(app_font, self.display_font_size+1), bg="white",
                                      fg="black")
        add_lesson_button.pack(pady=10)


        generate_schedule_button = tk.Button(self, text="Generate Schedule", command=self.process_schedule,
                                             font=(app_font, self.display_font_size+1), bg="white",
                                             fg="black")
        generate_schedule_button.pack(pady=10)

        show_schedule_button = tk.Button(self, text="Show Schedule", command=lambda: self.show_schedule(self.schedule),
                                         font=(app_font, self.display_font_size+1), bg="white",
                                         fg="black")
        show_schedule_button.pack(pady=10)

        options_button = tk.Button(self, text="Options", command=self.options_menu,
                                         font=(app_font, self.display_font_size+1), bg="white",
                                         fg="black")
        options_button.pack(pady=10)

        save_changes_button = tk.Button(self, text="Save Changes", command=self.save_data, font=(app_font, self.display_font_size+1), bg=accept_color, fg="black")
        save_changes_button.pack(pady=10)

        back_button = tk.Button(self, text="Back", command=self.welcome_screen, font=(app_font, self.display_font_size+1), bg=back_color,
                                fg="black")
        back_button.pack(pady=10)

    def save_data(self):
        self.save_horse_data()
        self.save_rider_data()

    def display_all_horses(self):
        """
        Displays all horses using a Treeview for faster rendering with a fixed-size box.
        :return: None
        """
        # Clear all widgets except the background label
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)
        self.resize_background()
        header_label = tk.Label(self, text=f"All Horses: {len(self.schedule.get_horses())}\nDouble Click To See Details", font=(app_font, self.display_font_size+3),
                                bg=m_frame_color, fg=text_color)
        header_label.pack(pady=10)

        style = ttk.Style()
        style.configure("Treeview", font=(app_font, 14))  # Row font
        style.configure("Treeview.Heading", font=(app_font, 14, "bold"))  # Header font

        # Treeview setup with fixed width and height
        tree_frame = tk.Frame(self, width=250, height=400)  # Fixed frame size
        tree_frame.pack(pady=20)
        tree_frame.pack_propagate(False)  # Prevent the frame from resizing to its content

        tree = ttk.Treeview(tree_frame, columns=("Name"), show="headings", height=20)
        tree.heading("Name", text="Horses")
        tree.column("Name", anchor="w", width=200)  # Adjust column width

        # Add riders to the Treeview
        horses = self.schedule.get_horses()
        horses = [i.get_name() for i in horses]
        horses.sort()
        for horse in horses:
            tree.insert("", "end", values=(horse,))

        def on_double_click(event):
            selected_item = tree.selection()
            if selected_item:
                horse_name = tree.item(selected_item, "values")[0]
                horse = next((r for r in horses if r == horse_name), None)
                if horse:
                    self.display_horse_information(self.schedule.get_horse(horse))

        tree.bind("<Double-1>", on_double_click)
        tree.pack(fill="both", expand=True)  # Fill within the fixed-size frame

        add_horse_button = tk.Button(self, text="Add Horse", command=self.add_horse, font=(app_font, self.display_font_size+1), bg=accept_color,
                                     fg="black")
        add_horse_button.pack(pady=10)

        back_button = tk.Button(self, text="Back", command=self.file_upload_screen, font=(app_font, self.display_font_size-1), bg=back_color,
                                fg="black")
        back_button.pack(pady=20)

    def options_menu(self):
        # Clear all widgets except the background label
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)
        self.resize_background()

        main_frame = tk.Frame(self, bg=m_frame_color)
        main_frame.pack(pady=10)

        tk.Label(main_frame, text="Display Font Size:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(
            row=0, column=0, padx=10, pady=5,
            sticky="e")
        font_entry = tk.Entry(main_frame, font=(app_font, self.display_font_size))
        font_entry.insert(0, self.display_font_size)
        font_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        def save_changes():
            try:
                new_font_size = int(font_entry.get())
                self.display_font_size = new_font_size
                self.data_manipulator.save_options(self)
                self.options_menu()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update settings: {e}")

        save_button = tk.Button(self, text="Save", command=save_changes, font=(app_font, self.display_font_size-1), bg=accept_color,
                                fg="black")
        save_button.pack(pady=10)

        back_button = tk.Button(self, text="Back", command=self.file_upload_screen,
                                font=(app_font, self.display_font_size-1), bg=back_color, fg="black")
        back_button.pack(pady=10)

    def display_horse_information(self, horse):
        """
        Displays detailed information about a specific horse in the current window.
        :param horse: Horse object whose information is to be displayed.
        :return: None
        """
        # Reinitialize the background label if it's missing
        if not hasattr(self, "bg_label") or not self.bg_label.winfo_exists():
            self.bg_label = tk.Label(self)
            self.bg_label.place(relwidth=1, relheight=1)
            self.resize_background()

        # Clear all widgets except the background label
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)
        self.resize_background()

        main_frame = tk.Frame(self, bg=m_frame_color)
        main_frame.pack(pady=10)

        tk.Label(main_frame, text="Name:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=0, column=0, padx=10, pady=5,
                                                                                 sticky="e")
        tk.Label(main_frame, text=horse.get_name(), font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=0, column=1, padx=10,
                                                                                          pady=5, sticky="w")

        tk.Label(main_frame, text="Leaser:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=1, column=0, padx=10, pady=5,
                                                                                   sticky="e")

        if horse.get_leaser():
            tk.Label(main_frame, text=horse.get_leaser(), font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=1, column=1, padx=10,
                                                                                            pady=5, sticky="w")
        else:
            tk.Label(main_frame, text="No leasers", font=(app_font, self.display_font_size, "italic"), bg=m_frame_color, fg=text_color).grid(
                row=1, column=1, padx=10,
                pady=5, sticky="w")

        tk.Label(main_frame, text="Max Weight:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=2, column=0, padx=10, pady=5,
                                                                                       sticky="e")
        tk.Label(main_frame, text=f"{horse.get_max_weight()} lbs", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=2,
                                                                                                         column=1,
                                                                                                         padx=10,
                                                                                                         pady=5,
                                                                                                         sticky="w")

        tk.Label(main_frame, text="Skill Level:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=3, column=0, padx=10,
                                                                                        pady=5, sticky="e")
        tk.Label(main_frame, text=horse.get_skill_level(), font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=3, column=1,
                                                                                                 padx=10, pady=5,
                                                                                                 sticky="w")

        tk.Label(main_frame, text="Jumper:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=4, column=0, padx=10, pady=5,
                                                                                   sticky="e")
        tk.Label(main_frame, text="Yes" if horse.is_jumping_horse() else "No", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(
            row=4, column=1, padx=10, pady=5, sticky="w")

        tk.Label(main_frame, text="Max Daily Jumps:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=5, column=0, padx=10,
                                                                                            pady=5, sticky="e")
        tk.Label(main_frame, text=horse.get_max_daily_jumps(), font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=5, column=1,
                                                                                                     padx=10, pady=5,
                                                                                                     sticky="w")

        ''' Relic code
        jumper_times = horse.get_jumper_times()
        tk.Label(main_frame, text="Jumper Times This Week:", font=(app_font, self.display_font_size-1), bg=m_frame_color, fg=text_color).grid(row=6, column=0,
                                                                                                   padx=10, pady=5,
                                                                                                   sticky="e")
        tk.Label(main_frame, text=jumper_times, font=(app_font, self.display_font_size-1), bg=m_frame_color, fg=text_color).grid(row=6, column=1, padx=10, pady=5,
                                                                                      sticky="w")

        non_jumper_times = horse.get_non_jumper_times()
        tk.Label(main_frame, text="Non-Jumper Times This Week:", font=(app_font, self.display_font_size-1), bg=m_frame_color, fg=text_color).grid(row=7, column=0,
                                                                                                       padx=10, pady=5,
                                                                                                       sticky="e")
        tk.Label(main_frame, text=non_jumper_times, font=(app_font, self.display_font_size-1), bg=m_frame_color, fg=text_color).grid(row=7, column=1, padx=10,
                                                                                          pady=5, sticky="w")
        '''
        def edit_horse():
            self.edit_horse_information(horse)

        edit_button = tk.Button(self, text="Edit", command=edit_horse, font=(app_font, self.display_font_size), bg=accept_color, fg="black")
        edit_button.pack(pady=10)

        def delete_horse():
            self.schedule.remove_horse(horse.get_name())
            self.display_all_horses()

        delete_horse_button = tk.Button(self, text="Delete Horse", command=delete_horse, font=(app_font, self.display_font_size),
                                        bg="#f44336", fg="black")
        delete_horse_button.pack(pady=10)

        back_button = tk.Button(self, text="Back", command=self.display_all_horses, font=(app_font, self.display_font_size), bg=back_color,
                                fg="black")
        back_button.pack(pady=10)

    def edit_horse_information(self, horse):
        """
        Opens a form in the current window to edit a horse's information, including leaser information.
        :param horse: Horse object to edit.
        :return: None
        """
        # Clear all widgets from the current window
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)
        self.resize_background()

        tk.Label(self, text="Edit Horse Information", font=(app_font, self.display_font_size + 2), bg=m_frame_color,
                 fg=text_color).pack(pady=10)

        main_frame = tk.Frame(self, bg=m_frame_color)
        main_frame.pack(pady=10)

        # Name
        tk.Label(main_frame, text="Name:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(
            row=0, column=0, padx=10, pady=5,
            sticky="e")
        name_entry = tk.Entry(main_frame, font=(app_font, self.display_font_size))
        name_entry.insert(0, horse.get_name())
        name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Max Weight
        tk.Label(main_frame, text="Max Weight (lbs):", font=(app_font, self.display_font_size), bg=m_frame_color,
                 fg=text_color).grid(row=1, column=0, padx=10,
                                     pady=5, sticky="e")
        max_weight_entry = tk.Entry(main_frame, font=(app_font, self.display_font_size), width=4)
        max_weight_entry.insert(0, str(horse.get_max_weight()))
        max_weight_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Skill Level
        tk.Label(main_frame, text="Skill Level:", font=(app_font, self.display_font_size), bg=m_frame_color,
                 fg=text_color).grid(row=2, column=0, padx=10,
                                     pady=5, sticky="e")
        skill_frame = tk.Frame(main_frame, bg=m_frame_color)
        skill_frame.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        skill_levels = {
            "Beginner": tk.IntVar(value=0 if "B" not in horse.get_skill_level() else 1),
            "Novice": tk.IntVar(value=0 if "N" not in horse.get_skill_level() else 1),
            "Intermediate": tk.IntVar(value=0 if "I" not in horse.get_skill_level() else 1),
            "Open": tk.IntVar(value=0 if "O" not in horse.get_skill_level() else 1),
        }
        for level, var in skill_levels.items():
            check_box = tk.Checkbutton(skill_frame, text=level, variable=var, bg=m_frame_color, fg=text_color,
                                       selectcolor=m_frame_color)
            check_box.pack(side="left", padx=5)

        # Jumper
        tk.Label(main_frame, text="Jumper (Yes/No):", font=(app_font, self.display_font_size), bg=m_frame_color,
                 fg=text_color).grid(row=3, column=0, padx=10,
                                     pady=5, sticky="e")
        jumper_var = tk.StringVar(value="Yes" if horse.is_jumping_horse() else "No")
        jumper_entry = tk.Entry(main_frame, textvariable=jumper_var, font=(app_font, self.display_font_size), width=3)
        jumper_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Max Daily Jumps
        tk.Label(main_frame, text="Max Daily Jumps:", font=(app_font, self.display_font_size), bg=m_frame_color,
                 fg=text_color).grid(row=4, column=0, padx=10,
                                     pady=5, sticky="e")
        max_jumps_entry = tk.Entry(main_frame, font=(app_font, self.display_font_size), width=3)
        max_jumps_entry.insert(0, str(horse.get_max_daily_jumps()))
        max_jumps_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Leasers
        tk.Label(main_frame, text="Leasers (optional):", font=(app_font, self.display_font_size), bg=m_frame_color,
                 fg=text_color).grid(row=5, column=0, padx=10,
                                     pady=5, sticky="ne")
        leaser_frame = tk.Frame(main_frame, bg=m_frame_color)
        leaser_frame.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        leaser_menus = []

        riders = [r.get_name() for r in self.schedule.get_riders()]
        riders.sort()
        if len(riders) == 0:
            riders = ["No Riders"]

        def add_leaser_menu():
            leaser_var = tk.StringVar()
            leaser_var.set(riders[0])  # Default to the first rider in the list
            menu = tk.OptionMenu(leaser_frame, leaser_var, *riders)
            menu.config(font=(app_font, self.display_font_size - 2))
            menu.pack(pady=2, anchor="w")
            leaser_menus.append((leaser_var, menu))

        def remove_leaser_menu():
            if leaser_menus:
                _, last_menu = leaser_menus.pop()
                last_menu.destroy()

        tk.Button(leaser_frame, text="Add Leaser", command=add_leaser_menu,
                  font=(app_font, self.display_font_size - 2)).pack(side="left", padx=0, anchor='nw')
        tk.Button(leaser_frame, text="Remove Leaser", command=remove_leaser_menu,
                  font=(app_font, self.display_font_size - 2)).pack(side="left", padx=10, anchor='nw')

        for leaser in horse.get_leaser().split(";"):
            if leaser.strip():
                leaser_var = tk.StringVar(value=leaser)
                menu = tk.OptionMenu(leaser_frame, leaser_var, *riders)
                menu.config(font=(app_font, self.display_font_size - 2))
                if leaser != horse.get_leaser().split(";")[0]:
                    menu.pack(pady=2, anchor="w")
                else:
                    menu.pack(pady=0, anchor='w')
                leaser_menus.append((leaser_var, menu))



        def save_changes():
            try:
                new_name = name_entry.get()
                new_max_weight = int(max_weight_entry.get())
                selected_skills = [level for level, var in skill_levels.items() if var.get() == 1]
                if not selected_skills:
                    messagebox.showerror("Skill Issue!", "At least one skill level must be selected!")
                    return
                skills = [skill[0] for skill in selected_skills]
                new_skill = "-".join(skills)

                new_jumper = jumper_var.get().strip().lower() == "yes"
                new_max_jumps = int(max_jumps_entry.get())

                leasers = [leaser_var.get() for leaser_var, _ in leaser_menus if leaser_var.get() != "No Riders"]
                leasers = ";".join(leasers)

                horse.set_name(new_name)
                horse.set_max_weight(new_max_weight)
                horse.set_skill_level(new_skill)
                horse.set_is_jumping_horse(new_jumper)
                horse._max_daily_jumps = new_max_jumps  # Assuming there's no setter for max_daily_jumps
                horse.set_leaser(leasers)

                messagebox.showinfo("Success", "Horse information updated successfully.")
                self.display_horse_information(horse)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update horse: {e}")

        save_button = tk.Button(self, text="Save", command=save_changes, font=(app_font, self.display_font_size-1), bg=accept_color,
                                fg="black")
        save_button.pack(pady=10)

        back_button = tk.Button(self, text="Cancel", command=lambda: self.display_horse_information(horse),
                                font=(app_font, self.display_font_size-1), bg=back_color, fg="black")
        back_button.pack(pady=10)

    def display_all_riders(self):
        """
        Displays all riders using a Treeview for faster rendering with a fixed-size box.
        :return: None
        """
        # Clear all widgets except the background label
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)
        self.resize_background()

        header_label = tk.Label(self, text=f"All Riders: {len(self.schedule.get_riders())}\nDouble Click To See Details", font=(app_font, self.display_font_size+3),
                                bg=m_frame_color, fg=text_color)
        header_label.pack(pady=10)

        style = ttk.Style()
        style.configure("Treeview", font=(app_font, 14))  # Row font
        style.configure("Treeview.Heading", font=(app_font, 14, "bold"))  # Header font

        # Treeview setup with fixed width and height
        tree_frame = tk.Frame(self, width=250, height=475)  # Fixed frame size
        tree_frame.pack(pady=20)
        tree_frame.pack_propagate(False)  # Prevent the frame from resizing to its content

        tree = ttk.Treeview(tree_frame, columns=("Name"), show="headings", height=20)
        tree.heading("Name", text="Riders")
        tree.column("Name", anchor="w", width=200)  # Adjust column width

        # Add riders to the Treeview
        riders = self.schedule.get_riders()
        riders = [i.get_name() for i in riders]
        riders.sort()
        for rider in riders:
            tree.insert("", "end", values=(rider,))

        def on_double_click(event):
            selected_item = tree.selection()
            if selected_item:
                rider_name = tree.item(selected_item, "values")[0]
                rider = next((r for r in riders if r == rider_name), None)
                if rider:
                    self.display_rider_information(self.schedule.get_rider(rider))

        tree.bind("<Double-1>", on_double_click)
        tree.pack(fill="both", expand=True)  # Fill within the fixed-size frame

        add_rider_button = tk.Button(self, text="Add Rider", command=self.add_rider, font=(app_font, self.display_font_size+1), bg=accept_color,
                                     fg="black")
        add_rider_button.pack(pady=10)

        back_button = tk.Button(self, text="Back", command=self.file_upload_screen, font=(app_font, self.display_font_size-1), bg=back_color,
                                fg="black")
        back_button.pack(pady=20)

    def display_rider_information(self, rider):
        """
        Displays detailed information about a specific rider in the current window.
        :param rider: Rider object whose information is to be displayed.
        :return: None
        """
        # Reinitialize the background label if it's missing
        if not hasattr(self, "bg_label") or not self.bg_label.winfo_exists():
            self.bg_label = tk.Label(self)
            self.bg_label.place(relwidth=1, relheight=1)
            self.resize_background()

        # Clear all widgets except the background label
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)
        self.resize_background()

        main_frame = tk.Frame(self, bg=m_frame_color)
        main_frame.pack(pady=10)

        tk.Label(main_frame, text="Name:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=0, column=0, padx=10, pady=5,
                                                                                 sticky="e")
        tk.Label(main_frame, text=rider.get_name(), font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=0, column=1, padx=10,
                                                                                          pady=5, sticky="w")

        tk.Label(main_frame, text="Weight:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=1, column=0, padx=10, pady=5,
                                                                                   sticky="e")
        tk.Label(main_frame, text=f"{rider.get_weight()} lbs", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=1, column=1,
                                                                                                     padx=10, pady=5,
                                                                                                     sticky="w")

        tk.Label(main_frame, text="Skill Level:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=2, column=0, padx=10,
                                                                                        pady=5, sticky="e")
        tk.Label(main_frame, text=rider.get_skill_level(), font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=2, column=1,
                                                                                                 padx=10, pady=5,
                                                                                                 sticky="w")

        recent_horses = rider.get_recent_horses()
        tk.Label(main_frame, text="Recent Horses:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=3, column=0, padx=10,
                                                                                          pady=5, sticky="e")
        if recent_horses:
            horses = ", ".join(recent_horses)
            tk.Label(main_frame, text=horses, font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=3, column=1, padx=10, pady=5,
                                                                                    sticky="w")
        else:
            tk.Label(main_frame, text="No recent horses.", font=(app_font, self.display_font_size, "italic"), bg=m_frame_color, fg=text_color).grid(row=3,
                                                                                                           column=1,
                                                                                                           padx=10,
                                                                                                           pady=5,
                                                                                                           sticky="w")

        tk.Label(main_frame, text="Total Owed:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=4, column=0, padx=10, pady=5,
                                                                                       sticky="e")
        tk.Label(main_frame, text=f"${rider.get_total_owed():.2f}", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=4,
                                                                                                          column=1,
                                                                                                          padx=10,
                                                                                                          pady=5,
                                                                                                          sticky="w")

        tk.Label(main_frame, text="Current Lessons:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=5, column=0, padx=10,
                                                                                            pady=5, sticky="e")
        lessons = rider.get_weekly_schedule()
        if lessons:
            all_lessons = "\n".join([
                                        f"{self.data_manipulator.military_to_standard(lesson[1])} on {lesson[0]} and {'jumping' if lesson[2] else 'not jumping'}"
                                        for lesson in lessons])
            tk.Label(main_frame, text=all_lessons, font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=5, column=1, padx=10,
                                                                                         pady=5, sticky="w")
        else:
            tk.Label(main_frame, text="No lessons planned", font=(app_font, self.display_font_size, "italic"), bg=m_frame_color, fg=text_color).grid(row=5,
                                                                                                            column=1,
                                                                                                            padx=10,
                                                                                                            pady=5,
                                                                                                            sticky="w")

        def edit_rider():
            self.edit_rider_information(rider)

        edit_button = tk.Button(self, text="Edit", command=edit_rider, font=(app_font, self.display_font_size), bg=accept_color, fg="black")
        edit_button.pack(pady=10)

        def delete_rider():
            self.schedule.remove_rider(rider.get_name())
            self.display_all_riders()

        delete_rider_button = tk.Button(self, text="Delete Rider", command=delete_rider, font=(app_font, self.display_font_size),
                                        bg="#f44336", fg="black")
        delete_rider_button.pack(pady=10)

        back_button = tk.Button(self, text="Back", command=self.display_all_riders, font=(app_font, self.display_font_size), bg="gray",
                                fg="black")
        back_button.pack(pady=10)

    def edit_rider_information(self, rider):
        """
        Opens a form in the current window to edit a rider's information.
        :param rider: Rider object to edit.
        :return: None
        """
        # Clear all widgets from the current window
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)
        self.resize_background()

        tk.Label(self, text="Edit Rider Information", font=(app_font, self.display_font_size + 2), bg=m_frame_color,
                 fg=text_color).pack(
            pady=10)

        main_frame = tk.Frame(self, bg=m_frame_color)
        main_frame.pack(pady=10)

        # Name
        tk.Label(main_frame, text="Name:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(
            row=0, column=0,
            padx=10, pady=5,
            sticky="e")
        name_entry = tk.Entry(main_frame, font=(app_font, self.display_font_size))
        name_entry.insert(0, rider.get_name())
        name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Weight
        tk.Label(main_frame, text="Weight (lbs):", font=(app_font, self.display_font_size), bg=m_frame_color,
                 fg=text_color).grid(row=1,
                                     column=0,
                                     padx=10,
                                     pady=5,
                                     sticky="e")
        weight_entry = tk.Entry(main_frame, font=(app_font, self.display_font_size), width=4)
        weight_entry.insert(0, str(rider.get_weight()))
        weight_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Skill Level
        tk.Label(main_frame, text="Skill Level:", font=(app_font, self.display_font_size), bg=m_frame_color,
                 fg=text_color).grid(row=2,
                                     column=0,
                                     padx=10,
                                     pady=5,
                                     sticky="e")
        skill_frame = tk.Frame(main_frame, bg=m_frame_color)
        skill_frame.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        skill_levels = {
            "Beginner": tk.IntVar(value=0 if "B" not in rider.get_skill_level() else 1),
            "Novice": tk.IntVar(value=0 if "N" not in rider.get_skill_level() else 1),
            "Intermediate": tk.IntVar(value=0 if "I" not in rider.get_skill_level() else 1),
            "Open": tk.IntVar(value=0 if "O" not in rider.get_skill_level() else 1),
        }
        for level, var in skill_levels.items():
            check_box = tk.Checkbutton(skill_frame, text=level, variable=var, bg=m_frame_color, fg=text_color,
                                       selectcolor=m_frame_color)
            check_box.pack(side="left", padx=5)

        lessons = rider.get_weekly_schedule()
        removed_lessons = []

        def remove_lesson(lesson, button, label):
            removed_lessons.append(lesson)
            button.destroy()
            label.destroy()

        lessons_frame = tk.Frame(main_frame, bg=m_frame_color)
        lessons_frame.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        for lesson in lessons:
            lesson_text = f"{self.data_manipulator.military_to_standard(lesson[1])} on {lesson[0]}" + ((f" and {'jumping' if lesson[2] else 'not jumping'}") if self.data_manipulator.military_to_standard(lesson[1]) != "Hack" else "") + ("(Prepaid)" if (len(lesson) > 4 and lesson[4]) else "")
            lesson_frame = tk.Frame(lessons_frame, bg=m_frame_color)
            lesson_frame.pack(anchor="w", pady=2)

            lesson_label = tk.Label(lesson_frame, text=lesson_text, font=(app_font, self.display_font_size),
                                    bg=m_frame_color, fg=text_color)
            lesson_label.pack(side="left")
            remove_button = tk.Button(
                lesson_frame,
                text="Remove",
                command=lambda l=lesson, b=lesson_frame, lbl=lesson_label: remove_lesson(l, b, lbl),
                font=(app_font, self.display_font_size - 2),
                bg="#f44336",
                fg="black"
            )
            remove_button.pack(side="left", padx=5)

        def save_changes():
            try:
                new_name = name_entry.get()
                new_weight = int(weight_entry.get())
                selected_skills = [level for level, var in skill_levels.items() if var.get() == 1]
                if not selected_skills:
                    messagebox.showerror("Skill Issue!", "At least one skill level must be selected!")
                    return
                skills = [skill[0] for skill in selected_skills]
                new_skill = "-".join(skills)

                rider.set_name(new_name)
                rider.set_weight(new_weight)
                rider.set_skill_level(new_skill)

                for lesson in removed_lessons:
                    rider.remove_lesson_time(lesson)

                messagebox.showinfo("Success", "Rider information updated successfully.")
                self.display_rider_information(rider)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update rider: {e}")

        save_button = tk.Button(self, text="Save", command=save_changes, font=(app_font, self.display_font_size),
                                bg=accept_color, fg="black")
        save_button.pack(pady=10)

        back_button = tk.Button(self, text="Cancel", command=lambda: self.display_rider_information(rider),
                                font=(app_font, self.display_font_size), bg=back_color, fg="black")
        back_button.pack(pady=10)

    def load_saves(self):
        self.data_manipulator.load_riders_from_pickle(self.schedule)
        self.data_manipulator.load_horses_from_pickle(self.schedule)
        self.data_manipulator.load_options(self)
        self.schedule.update_schedule()

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

    def save_schedule_data(self):
        self.data_manipulator.save_schedule_to_pickle(self.schedule)

    def add_horse(self):
        '''
        Opens a new window to add a new horse to the schedule, with fields for the horse's name, attributes, and optional leasers.
        :return: None
        '''
        # Reinitialize the background label if it's missing
        self.resize_background()
        if not hasattr(self, "bg_label") or not self.bg_label.winfo_exists():
            self.bg_label = tk.Label(self)
            self.bg_label.place(relwidth=1, relheight=1)
            self.resize_background()

        # Clear all widgets except the background label
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)
        self.resize_background()
        self.active_window = self

        # Create a main frame for the form layout
        main_frame = tk.Frame(self, bg=m_frame_color)
        main_frame.pack(pady=40, padx=10)

        # Name
        tk.Label(main_frame, text="Name:", font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(main_frame,font=(app_font, self.display_font_size))
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Max Weight
        tk.Label(main_frame, text="Max Weight:", bg=m_frame_color, fg=text_color, font=(app_font, self.display_font_size)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        max_weight_entry = tk.Entry(main_frame, font=(app_font, self.display_font_size), width=4)
        max_weight_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Skill Level
        tk.Label(main_frame, text="Skill Level:", bg=m_frame_color, fg=text_color, font=(app_font, self.display_font_size)).grid(row=2, column=0, padx=5, pady=5, sticky="ne")
        skill_frame = tk.Frame(main_frame,bg=m_frame_color)
        skill_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        skill_levels = {
            "Beginner": tk.IntVar(),
            "Novice": tk.IntVar(),
            "Intermediate": tk.IntVar(),
            "Open": tk.IntVar(),
        }
        for level, var in skill_levels.items():
            check_box = tk.Checkbutton(skill_frame, text=level, variable=var, bg=m_frame_color, fg=text_color,
                                       selectcolor=m_frame_color)
            check_box.pack(side="left", padx=5)

        # Is Jumper
        tk.Label(main_frame, text="Is Jumper (yes/no):", bg=m_frame_color, fg=text_color, font=(app_font, self.display_font_size)).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        is_jumper_entry = tk.Entry(main_frame, font=(app_font, self.display_font_size), width=3)
        is_jumper_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Max Rides per Day
        tk.Label(main_frame, text="Max Rides per Day:", bg=m_frame_color, fg=text_color, font=(app_font, self.display_font_size)).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        max_rides_entry = tk.Entry(main_frame, font=(app_font, self.display_font_size), width=3)
        max_rides_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Leasers
        tk.Label(main_frame, text="Leasers (optional):", bg=m_frame_color, fg=text_color, font=(app_font, self.display_font_size)).grid(row=5, column=0, padx=5, pady=5, sticky="ne")
        leaser_frame = tk.Frame(main_frame, bg=m_frame_color)
        leaser_frame.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        leaser_menus = []

        riders = [r.get_name() for r in self.schedule.get_riders()]
        riders.sort()
        if len(riders) == 0:
            riders = ["No Riders"]

        def add_leaser_menu():
            leaser_var = StringVar()
            leaser_var.set(riders[0])  # Default to the first rider in the list
            menu = tk.OptionMenu(leaser_frame, leaser_var, *riders)
            menu.config(font=(app_font, self.display_font_size))
            menu.pack(pady=2)
            leaser_menus.append((leaser_var, menu))

        def remove_leaser_menu():
            if leaser_menus:
                _, last_menu = leaser_menus.pop()
                last_menu.destroy()

        tk.Button(leaser_frame, text="Add Leaser", command=add_leaser_menu, font=(app_font, self.display_font_size)).pack(side=tk.LEFT, padx=0, anchor='nw')
        tk.Button(leaser_frame, text="Remove Leaser", command=remove_leaser_menu, font=(app_font, self.display_font_size)).pack(side=tk.LEFT, padx=10, anchor='nw')

        # Submit Button
        def submit_horse():
            try:
                name = name_entry.get()
                max_weight = int(max_weight_entry.get())
                selected_skills = [level for level, var in skill_levels.items() if var.get() == 1]
                if not selected_skills:
                    messagebox.showerror("Skill Issue!", "At least one skill level must be selected!")
                    return
                skills = [skill[0] for skill in selected_skills]
                skill_level = "-".join(skills)
                is_jumper = is_jumper_entry.get().strip().lower() == "yes"
                max_rides = int(max_rides_entry.get())
                leasers = [leaser_var.get() for leaser_var, _ in leaser_menus if leaser_var.get() != "No Riders"]
                leasers = ";".join(leasers)

                new_horse = Horse(name, is_jumping_horse=is_jumper, max_weight=max_weight, skill_level=skill_level,
                                  max_daily_jumps=max_rides, leaser=leasers)
                self.schedule.add_horse(new_horse)
                messagebox.showinfo("Success", f"Horse '{name}' added successfully.")
                self.display_all_horses()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add horse: {e}")

        tk.Button(self, text="Add Horse", command=submit_horse, bg=accept_color, fg="black", font=(app_font, self.display_font_size+2)).pack(pady=20)
        tk.Button(self, text="Cancel", command=self.display_all_horses, bg=back_color, fg="black", font=(app_font, self.display_font_size+2)).pack(pady=10)

    def add_rider(self):
        '''
        Opens a new window to add a new rider to the schedule, with fields for the rider's name, weight, and skill level.
        :return: None
        '''
        # Reinitialize the background label if it's missing
        if not hasattr(self, "bg_label") or not self.bg_label.winfo_exists():
            self.bg_label = tk.Label(self)
            self.bg_label.place(relwidth=1, relheight=1)
            self.resize_background()

        # Clear all widgets except the background label
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)
        self.resize_background()
        # Create a main frame for the form layout
        main_frame = tk.Frame(self, bg=m_frame_color)
        main_frame.pack(pady=40, padx=10)

        # Name
        tk.Label(main_frame, text="Name:", font=(app_font, self.display_font_size+2), bg=m_frame_color, fg=text_color).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(main_frame, font=(app_font, 15))
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Weight
        tk.Label(main_frame, text="Weight (lbs):", font=(app_font, self.display_font_size+2), bg=m_frame_color, fg=text_color).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        weight_entry = tk.Entry(main_frame, font=(app_font, self.display_font_size+2), width=4)
        weight_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Skill Level
        tk.Label(main_frame, text="Skill Level:", bg=m_frame_color, fg=text_color).grid(row=2, column=0, padx=5, pady=5,
                                                                                        sticky="ne")
        skill_frame = tk.Frame(main_frame, bg=m_frame_color)
        skill_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        skill_levels = {
            "Beginner": tk.IntVar(),
            "Novice": tk.IntVar(),
            "Intermediate": tk.IntVar(),
            "Open": tk.IntVar(),
        }
        for level, var in skill_levels.items():
            check_box = tk.Checkbutton(skill_frame, text=level, variable=var, bg=m_frame_color, fg=text_color,
                                       selectcolor=m_frame_color)
            check_box.pack(side="left", padx=5)

        # Submit Button
        def submit_rider():
            try:
                name = name_entry.get()
                weight = int(weight_entry.get())
                selected_skills = [level for level, var in skill_levels.items() if var.get() == 1]
                if not selected_skills:
                    messagebox.showerror("Skill Issue!", "At least one skill level must be selected!")
                    return
                skills = [skill[0] for skill in selected_skills]
                skill_level = "-".join(skills)

                new_rider = Rider(name, weight=weight, skill_level=skill_level, weekly_schedule=[])
                self.schedule.add_rider(new_rider)
                messagebox.showinfo("Success", f"Rider '{name}' added successfully.")
                self.display_all_riders()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add rider: {e}")

        tk.Button(self, text="Add Rider", command=submit_rider, bg=accept_color, font=(app_font, 15)).pack(pady=20)

        back_button = tk.Button(self, text="Back", command=self.display_all_riders, font=(app_font, self.display_font_size-1), bg=back_color,
                                fg="black")
        back_button.pack(pady=20)

    def add_lesson(self):
        '''
        Opens a new window to add a new lesson to the schedule, with options to select the rider, day, time, type of lesson, and duration.
        :return: None
        '''
        # Clear all widgets except the background label
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)
        self.resize_background()

        self.active_window = self

        main_frame = tk.Frame(self, bg=m_frame_color)
        main_frame.pack(pady=10)

        rider_name_option = StringVar()
        riders = [r.get_name() for r in self.schedule.get_riders()]
        riders.sort()

        if len(riders) == 0:
            riders = ["No Riders"]
        rider_name_option.set(riders[0])

        # Rider Name
        rider_label = tk.Label(main_frame, text="Name Of Rider:", font=(app_font, self.display_font_size-1), bg=m_frame_color, fg=text_color)
        rider_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        rider_options = tk.OptionMenu(main_frame, rider_name_option, *riders)
        rider_options.config(bg="white",relief="raised", bd=5, fg="black")
        rider_options.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Day of Week
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_option = StringVar()
        day_option.set(days_of_week[0])

        day_label = tk.Label(main_frame, text="Day of week:", font=(app_font, self.display_font_size-1), bg=m_frame_color, fg=text_color)
        day_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        day_options = tk.OptionMenu(main_frame, day_option, *days_of_week)
        day_options.config(bg="white",relief="raised", bd=5, fg="black")
        day_options.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Type of Lesson
        jump_var = StringVar()
        jump_var.set("Jumping")

        type_label = tk.Label(main_frame, text="Type of lesson:", font=(app_font, self.display_font_size-1), bg=m_frame_color, fg=text_color)
        type_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        jumping_lesson_dropdown = ttk.Combobox(main_frame, textvariable=jump_var,
                                               values=["Jumping", "Not Jumping", "Hack"],
                                               width=10,
                                               font=(app_font, self.display_font_size-1), state="readonly")
        jumping_lesson_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Duration
        duration_var = StringVar()
        duration_var.set("30")

        duration_label = tk.Label(main_frame, text="Duration of Lesson (in minutes):", font=(app_font, self.display_font_size-1), bg=m_frame_color, fg=text_color)
        duration_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        duration_dropdown = ttk.Combobox(main_frame, textvariable=duration_var, values=["30", "60"], width=5,
                                         font=(app_font, self.display_font_size-1), state="readonly")
        duration_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Time Input
        time_label = tk.Label(main_frame, text="Time:", font=(app_font, self.display_font_size-1), bg=m_frame_color,fg=text_color)
        time_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        time_frame = tk.Frame(main_frame, bg=m_frame_color)
        time_frame.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        hour_var = tk.StringVar(value="12")
        minute_var = tk.StringVar(value="00")
        ampm_var = tk.StringVar(value="AM")

        hour_spinbox = ttk.Spinbox(time_frame, from_=1, to=12, wrap=True, textvariable=hour_var, width=3,
                                   font=(app_font, 12))
        hour_spinbox.pack(side="left", padx=5)

        minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, wrap=True, textvariable=minute_var, format="%02.0f",
                                     width=3,
                                     font=(app_font, 12))
        minute_spinbox.pack(side="left", padx=5)

        ampm_dropdown = ttk.Combobox(time_frame, textvariable=ampm_var, values=["AM", "PM"], width=3,
                                     font=(app_font, self.display_font_size-1),
                                     state="readonly")
        ampm_dropdown.pack(side="left", padx=5)

        prepaids = {
            "Prepaid": tk.IntVar()
        }
        tk.Label(main_frame, text="Prepaid:", font=(app_font, self.display_font_size-1), bg=m_frame_color, fg=text_color).grid(row=5, column=0, padx=10,pady=5, sticky='e')
        check_box = tk.Checkbutton(main_frame, text="", variable=prepaids["Prepaid"], bg=m_frame_color, fg=text_color,
                                       selectcolor=m_frame_color)
        check_box.grid(row=5, column=1, padx=10, pady=5, stick='w')
        def toggle_hack_state(*args):
            if jump_var.get() == "Hack":
                duration_dropdown.config(state="disabled")
                hour_spinbox.config(state="disabled")
                minute_spinbox.config(state="disabled")
                ampm_dropdown.config(state="disabled")
            else:
                duration_dropdown.config(state="readonly")
                hour_spinbox.config(state="normal")
                minute_spinbox.config(state="normal")
                ampm_dropdown.config(state="readonly")

        jump_var.trace("w", toggle_hack_state)

        def get_time():
            if ampm_var.get() == "AM":
                if int(hour_var.get()) < 10:
                    return f"0{hour_var.get()}{minute_var.get()}"
                return f"{hour_var.get()}{minute_var.get()}"
            return f"{int(hour_var.get()) + 12}{minute_var.get()}"

        def submit_lesson():
            try:
                rider = rider_name_option.get()
                time = get_time() if jump_var.get() != "Hack" else "-1"
                day = day_option.get()
                duration = int(duration_var.get()) if jump_var.get() != "Hack" else 30
                jumper = True if jump_var.get() == "Jumping" else False
                prepaid = prepaids["Prepaid"].get()
                self.schedule.add_lesson(rider, day, time, duration, jumper, prepaid)
                messagebox.showinfo("Success", f"Lesson added successfully.")
                self.file_upload_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add rider: {e}")

        submit_button = tk.Button(self, text="Add Lesson", command=submit_lesson, font=(app_font, self.display_font_size-1), bg="#1d9bf0",
                                  fg="black")
        submit_button.pack(pady=20)

        back_button = tk.Button(self, text="Back", command=self.file_upload_screen, font=(app_font, self.display_font_size-1), bg=back_color,
                                fg="black")
        back_button.pack(pady=10)

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

    def pseudo_solve_speed(self):
        self.show_schedule(self.schedule)
        self.leave_schedule_screen()

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

        self.resize_background()
        # Clear all widgets except the background label
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)

        # Header and control buttons
        generate_schedule_button = tk.Button(self, text="Re-Generate Schedule", command=self.process_schedule,
                                             font=(app_font, self.display_font_size+1), bg="white", fg="black")
        generate_schedule_button.pack(pady=10)

        schedule_label = tk.Label(self, text="Week of " + self.data_manipulator.get_time_stamp(), font=(app_font, self.display_font_size+3), bg=m_frame_color, fg=text_color)
        schedule_label.pack(pady=20)

        export_button = tk.Button(self, text="Save to PDF", command=self.export_schedule_as_pdf, font=(app_font, self.display_font_size+1), bg=accept_color, fg="black")
        export_button.pack(pady=10)

        is_maximized = self.state() == 'zoomed'

        if is_maximized:
            # Multi-column layout with horizontal scrolling
            outer_canvas = tk.Canvas(self, bg=m_frame_color)
            x_scrollbar = tk.Scrollbar(self, orient="horizontal", command=outer_canvas.xview)
            y_scrollbar = tk.Scrollbar(self, orient="vertical", command=outer_canvas.yview)
            outer_frame = tk.Frame(outer_canvas, bg=m_frame_color)
            self.resize_background()

            outer_frame.bind(
                "<Configure>",
                lambda e: outer_canvas.configure(scrollregion=outer_canvas.bbox("all"))
            )
            outer_canvas.create_window((0, 0), window=outer_frame, anchor="nw")
            outer_canvas.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

            outer_canvas.pack(side="top", fill="both", expand=True)
            x_scrollbar.pack(side="bottom", fill="x")
            y_scrollbar.pack(side="right", fill="y")

            for col, (day, daily_schedule) in enumerate(self.schedule_data._planner.items()):
                day_frame = tk.Frame(outer_frame, bg="white", borderwidth=2, relief="groove")
                day_frame.grid(row=0, column=col, padx=10, pady=10, sticky="n")

                day_label = tk.Label(day_frame, text=f"{day}:", font=(app_font, self.display_font_size+1, "bold"), bg="white")
                day_label.pack(anchor="w", padx=10, pady=5)

                planner = daily_schedule.get_planner()
                if planner:
                    for time, lessons in sorted(planner.items()):
                        time_label = tk.Label(day_frame, text=f"  {daily_schedule.military_to_standard(time)}",
                                              font=(app_font, self.display_font_size+2), bg="white")
                        time_label.pack(anchor="w", padx=20)

                        for rider, horse in lessons:
                            lesson_label = tk.Label(day_frame,
                                                    text=f"    Rider: {rider} | Horse: {horse if horse else 'TBD'}",
                                                    font=(app_font, self.display_font_size+1), bg="white")
                            lesson_label.pack(anchor="w", padx=40)

                else:
                    no_schedule_label = tk.Label(day_frame, text="  No lessons scheduled.",
                                                 font=(app_font, self.display_font_size+1, "italic"), bg="white")
                    no_schedule_label.pack(anchor="w", padx=20)
        else:
            # Single-column scrollable layout for normal state
            canvas = tk.Canvas(self, bg=m_frame_color)
            scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="y", expand=True)
            scrollbar.pack(side="right", fill="y")

            for day, daily_schedule in self.schedule_data._planner.items():
                day_label = tk.Label(scrollable_frame, text=f"{day}:", font=(app_font, self.display_font_size+3, "bold"), bg="white")
                day_label.pack(anchor="w", padx=10, pady=5)

                planner = daily_schedule.get_planner()
                if planner:
                    for time, lessons in sorted(planner.items()):
                        time_label = tk.Label(scrollable_frame, text=f"  {daily_schedule.military_to_standard(time)}",
                                              font=(app_font, self.display_font_size+2), bg="white")
                        time_label.pack(anchor="w", padx=20)

                        for rider, horse in lessons:
                            lesson_label = tk.Label(scrollable_frame,
                                                    text=f"    Rider: {rider} | Horse: {horse if horse else 'TBD'}",
                                                    font=(app_font, self.display_font_size+1), bg="white")
                            lesson_label.pack(anchor="w", padx=40)
                else:
                    no_schedule_label = tk.Label(scrollable_frame, text="  No lessons scheduled.",
                                                 font=(app_font, self.display_font_size+1, "italic"), bg="white")
                    no_schedule_label.pack(anchor="w", padx=20)

        back_button = tk.Button(self, text="Back", command=self.leave_schedule_screen, font=(app_font, self.display_font_size-1), bg=back_color,
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
                used_horses = []
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
                            if horse_name not in used_horses:
                                used_horses.append(horse_name)
                    unused_horses = [""]
                    line = 0
                    pdf.setFont("Helvetica", 12)
                    pdf.drawString(current_column + 20, y_position, "Unused Horses For Today:")
                    y_position -= 15
                    pdf.setFont("Helvetica", 10)
                    for horse in self.schedule.get_horses():
                        if horse.get_name() not in used_horses:
                            if len(unused_horses[line]) > 30:
                                line += 1
                                unused_horses.append("")
                            unused_horses[line] += f"{horse.get_name()}, "

                    unused_horses[-1] = unused_horses[-1][:-2]
                    for line in unused_horses:
                        pdf.drawString(current_column + 40, y_position, line)
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
            self.save_schedule_data()
            self.charge_riders()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export schedule: {e}")

    def charge_riders(self):
        for rider in self.schedule.get_riders():
            for lesson in rider.get_weekly_schedule():
                if lesson[3] == -1:
                    rider.add_charge(60.0)
                elif lesson[3] <= 30:
                    rider.add_charge(75.0)
                elif lesson[5]:
                    rider.add_charge(85.0)
                else:
                    rider.add_charge(90.0)

    def display_lessons_by_day(self):
        """
        Displays all lessons for a given day with a dropdown to select the day of the week.
        Includes an "Add Lesson" button and "Remove Lesson" buttons for each rider's lesson.
        :return: None
        """
        # Clear all widgets from the current window
        for widget in self.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

        self.bg_label.config(image=self.background_image)
        self.resize_background()

        tk.Label(self, text="View Lessons by Day", font=(app_font, self.display_font_size + 2), bg=m_frame_color,
                 fg=text_color).pack(
            pady=10
        )

        main_frame = tk.Frame(self, bg=m_frame_color)
        main_frame.pack(pady=10)

        # Dropdown to select day
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        selected_day = tk.StringVar(value=days_of_week[0])

        tk.Label(main_frame, text="Select Day:", font=(app_font, self.display_font_size), bg=m_frame_color,
                 fg=text_color).grid(
            row=0, column=0, padx=10, pady=5, sticky="e"
        )
        day_dropdown = tk.OptionMenu(main_frame, selected_day, *days_of_week)
        day_dropdown.config(font=(app_font, self.display_font_size), bg=m_frame_color, fg=text_color)
        day_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        lessons_frame = tk.Frame(main_frame, bg=m_frame_color)
        lessons_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

        removed_lessons = []
        def all_riders_removed_at_time(rider_tuples, time):
            for rider_tuple in rider_tuples:
                if (time, rider_tuple) not in removed_lessons:
                    return False
            return True

        def update_lessons():
            for widget in lessons_frame.winfo_children():
                widget.destroy()

            planners = self.schedule.get_planner()
            day = selected_day.get()
            lessons = planners[day].get_planner()

            if not lessons:
                tk.Label(lessons_frame, text=f"No lessons found for {day}.", font=(app_font, self.display_font_size),
                         bg=m_frame_color, fg=text_color).pack(pady=5)
            else:
                for lesson_time, riders in sorted(lessons.items()):
                    if all_riders_removed_at_time(riders, lesson_time):
                        continue
                    formatted_time = self.data_manipulator.military_to_standard(lesson_time)
                    lesson_frame = tk.Frame(lessons_frame, bg=m_frame_color)
                    lesson_frame.pack(anchor="w", pady=5, fill="x")

                    tk.Label(lesson_frame, text=formatted_time, font=(app_font, self.display_font_size + 1),
                             bg=m_frame_color, fg=text_color).pack(side="left", padx=10)

                    for rider_tuple in riders:
                        if (lesson_time, rider_tuple) in removed_lessons:
                            continue
                        rider_name, horse_name = rider_tuple

                        rider_frame = tk.Frame(lessons_frame, bg=m_frame_color)
                        rider_frame.pack(anchor="w", pady=2, fill="x")

                        rider_label = tk.Label(rider_frame, text=f"{rider_name}", font=(app_font, self.display_font_size),
                                 bg=m_frame_color, fg=text_color)
                        rider_label.pack(side="left", padx=2)

                        remove_button = tk.Button(
                            rider_frame,
                            text="Remove",
                            command=lambda t=lesson_time, r=rider_tuple: remove_lesson(t, r),
                            font=(app_font, self.display_font_size - 3),
                            bg="#f44336",
                            fg="black",
                        )
                        remove_button.pack(side="right", padx=5)

        def remove_lesson(lesson_time, rider_tuple):
            removed_lessons.append((lesson_time, rider_tuple))
            update_lessons()

        def save_changes():
            try:
                for lesson_time, rider_tuple in removed_lessons:
                    self.schedule.get_rider(rider_tuple[0]).remove_lesson_time(lesson_time)
                self.schedule.update_schedule()
                messagebox.showinfo("Success", "Lessons updated successfully.")
                self.file_upload_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save changes: {e}")

        save_button = tk.Button(self, text="Save", command=save_changes, font=(app_font, self.display_font_size),
                                bg=accept_color, fg="black")
        save_button.pack(pady=10)

        back_button = tk.Button(self, text="Cancel", command=self.file_upload_screen, font=(app_font, self.display_font_size),
                                bg="#f44336", fg="black")
        back_button.pack(pady=10)

        selected_day.trace("w", lambda *args: update_lessons())
        update_lessons()


# Application entry
if __name__ == "__main__":
    app = App()
    app.mainloop()
