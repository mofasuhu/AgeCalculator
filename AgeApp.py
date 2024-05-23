import tkinter as tk
from tkinter import messagebox, font
from datetime import datetime
import time
import threading
from dateutil.relativedelta import relativedelta
from PIL import Image, ImageTk


# Store the original window size
original_height = 330
collapsed_height = 70

# Function to calculate age
def calculate_age():
    try:
        day = int(day_entry.get())
        month = int(month_entry.get())
        year = int(year_entry.get())
        hour = int(hour_entry.get())
        minute = int(minute_entry.get())
        second = int(second_entry.get())

        # Input validation for range
        if not (1 <= day <= 31 and 1 <= month <= 12 and year > 0 and
                0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60):
            raise ValueError("Date or time values are out of range")

        # Validate the actual date to catch invalid dates like February 30
        birth_date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

        def update_age():
            while not stop_event.is_set():
                current_date = datetime.now()
                delta = relativedelta(current_date, birth_date)

                # Update the age label with the calculated age
                age_label.config(text=f'Today you are {delta.years} years {delta.months} months {delta.days} days {delta.hours} hours {delta.minutes} minutes {delta.seconds} seconds old.')
                time.sleep(1)

        global stop_event, age_thread
        # Stop any existing thread
        if stop_event is not None:
            stop_event.set()
        # Create a new event and thread
        stop_event = threading.Event()
        age_thread = threading.Thread(target=update_age, daemon=True)
        age_thread.start()

        # Hide all input components and adjust window size
        hide_components()

    except ValueError as e:
        # Show error message for invalid input
        messagebox.showerror("Invalid input", f"Please enter valid numeric values.")

# Function to clear the inputs and stop the update thread
def reset_fields():
    global stop_event
    if stop_event:
        stop_event.set()
    day_entry.delete(0, tk.END)
    month_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    hour_entry.delete(0, tk.END)
    minute_entry.delete(0, tk.END)
    second_entry.delete(0, tk.END)
    age_label.config(text="")
    show_components()
    day_entry.focus_set()  # Set the focus to the day entry field


# Function to exit the program
def exit_program():
    global stop_event
    if stop_event:
        stop_event.set()
    root.destroy()

# Function to hide input components and adjust window size
def hide_components():
    for widget in input_widgets:
        widget.grid_remove()
    reset_button.grid()
    exit_button.grid()
    root.geometry(f"950x{collapsed_height}")
    root.attributes('-alpha', 0.8)  # Set transparency level
    
    
    
# Function to show input components and adjust window size
def show_components():
    for widget in input_widgets:
        widget.grid()
    reset_button.grid()
    exit_button.grid()
    root.geometry(f"950x{original_height}")
    root.attributes('-alpha', 1)  # Set transparency level

# Create the main window
root = tk.Tk()
root.title("Age Calculator")
root.geometry(f"950x{original_height}")


# Set fonts
label_font = font.Font(family="Helvetica", size=14, weight="bold")
entry_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=10, weight="bold")
result_font = font.Font(family="Helvetica", size=16, weight="bold")

# Create and place the input fields and labels
day_label = tk.Label(root, text="Day of Birth (1-31):", font=label_font)
day_entry = tk.Entry(root, font=entry_font, width=10)

month_label = tk.Label(root, text="Month of Birth (1-12):", font=label_font)
month_entry = tk.Entry(root, font=entry_font, width=10)

year_label = tk.Label(root, text="Year of Birth (e.g., 1990):", font=label_font)
year_entry = tk.Entry(root, font=entry_font, width=10)

hour_label = tk.Label(root, text="Hour of Birth (0-23):", font=label_font)
hour_entry = tk.Entry(root, font=entry_font, width=10)

minute_label = tk.Label(root, text="Minute of Birth (0-59):", font=label_font)
minute_entry = tk.Entry(root, font=entry_font, width=10)

second_label = tk.Label(root, text="Second of Birth (0-59):", font=label_font)
second_entry = tk.Entry(root, font=entry_font, width=10)

# Create and place the buttons
calculate_button = tk.Button(root, text="Calculate Age", command=calculate_age, font=button_font, bg="#4CAF50", fg="white")
reset_button = tk.Button(root, text="Reset", command=reset_fields, font=button_font, bg="#f44336", fg="white")
exit_button = tk.Button(root, text="Exit", command=exit_program, font=button_font, bg="#555555", fg="white")

# Place the widgets in a grid layout
day_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
day_entry.grid(row=0, column=1, padx=10, pady=10)

month_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
month_entry.grid(row=1, column=1, padx=10, pady=10)

year_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
year_entry.grid(row=2, column=1, padx=10, pady=10)

hour_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
hour_entry.grid(row=3, column=1, padx=10, pady=10)

minute_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
minute_entry.grid(row=4, column=1, padx=10, pady=10)

second_label.grid(row=5, column=0, padx=10, pady=10, sticky='e')
second_entry.grid(row=5, column=1, padx=10, pady=10)

calculate_button.grid(row=6, column=1, padx=5, pady=0)
reset_button.grid(row=6, column=0, padx=5, pady=0)
exit_button.grid(row=6, column=4, padx=5, pady=0)

# Label to display the age
age_label = tk.Label(root, text="", font=result_font)
age_label.grid(row=6, column=1, columnspan=3, pady=0)


day_entry.focus_set()  # Set the focus to the day entry field


# Center the grid layout
for i in range(3):
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(6, weight=1)

# Initialize stop_event and age_thread
stop_event = None
age_thread = None

# List of input widgets for easy hide/show
input_widgets = [day_label, day_entry, month_label, month_entry, year_label, year_entry,
                 hour_label, hour_entry, minute_label, minute_entry, second_label, second_entry,
                 calculate_button]


# Bind the "Enter" key to each button
def bind_enter_to_button(button, command):
    button.bind("<Return>", lambda event: command())

bind_enter_to_button(calculate_button, calculate_age)
bind_enter_to_button(reset_button, reset_fields)
bind_enter_to_button(exit_button, exit_program)


# Run the Tkinter event loop
root.mainloop()
