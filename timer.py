# Timer GUI App written in Python

from tkinter import *
from tkinter import ttk
from time import sleep

# TODO Add sound when timer is completed
# TODO Add visual effect when timer is completed
# TODO Flash on tool bar when timer completed

def run_timer():
    # Keeps track of time
    global rt_callback
    t = time_left_float.get()
    if t >= 0 and timer_active.get() == True:
        mins, secs = divmod(t, 60)
        hours = mins / 60
        if int(hours) > 0:
            mins = mins % 60
            time_formatted = f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}"
        else:
            time_formatted = f"{int(mins):02d}:{int(secs):02d}"

        time_left.set(time_formatted)
        time_left_float.set(time_left_float.get() - 1)
        rt_callback = root.after(1000, run_timer)


def start_timer(*args):
    # Starts the timer
    try:
        if timer_active.get() == True:
            run_timer()
        else:
            # Get start time and set time_left_float variable
            t = ((int(timer_hours.get()) * 3600) + (int(timer_mins.get()) * 60) 
                + int(timer_secs.get()))
            time_left_float.set(float(t))
            timer_active.set(True)
            run_timer()
        
        # Disable start button until pause or reset button pressed
        button_start["state"] = "disabled"
        button_pause["state"] = "enabled"
    except ValueError:
        pass


def reset_timer(*args):
    # resets the timer and resets the time
    if timer_active.get() == True:
        timer_active.set(False)
        time_left.set("00:00")
        time_left_float.set(0.0)

        # Disable/enable start and pause buttons
        button_start["state"] = "enabled"
        button_pause["state"] = "disabled"
    else:
        # Resets all entry fields back to zero if reset btn pressed twice
        timer_hours.set(0)
        timer_mins.set('')
        timer_secs.set(0)
        time_entry_mins.focus() # Focus on minutes entry field


def pause_timer(*args):
    # Pauses the active timer
    if timer_active.get() == True:
        root.after_cancel(rt_callback)
        button_start["state"] = "enabled"
        button_pause["state"] = "disabled"


# GUI ==========================================================================
# Set up main Tk window and title
root = Tk()
root.title("Timer")
root.resizable(width=False, height=False)

# Create a themed frame widget within the main window to hold UI content
mainframe = ttk.Frame(root, padding="3 3 3 3", borderwidth=5, relief='sunken')
mainframe.grid(row=0, column=0, sticky=(N, W, E, S), padx=10, pady=10)
root.columnconfigure(0, weight=1) # Expand frame if window is resized
root.rowconfigure(0, weight=1)

# Set up variable classes to track changes
timer_active = BooleanVar(value=False)
timer_hours = StringVar(value=0)
timer_mins = StringVar()
timer_secs = StringVar(value=0)
time_left = StringVar(value="00:00")
time_left_float = DoubleVar()

# Standard info label displayed at the top
# info_label = ttk.Label(mainframe, text="Enter Length of Timer",
#     font=("Helvetica", 14))
# info_label.grid(row=0, column=1, columnspan=3)

# Create label widgets for hours, mins, and secs
time_label_hours = ttk.Label(mainframe, text="Hours")
time_label_mins = ttk.Label(mainframe, text="Mins")
time_label_secs = ttk.Label(mainframe, text="Secs")
time_label_hours.grid(row=1, column=1)
time_label_mins.grid(row=1, column=2)
time_label_secs.grid(row=1, column=3)

# Create entry widgets for getting timer length in hours, mins, and secs
time_entry_hours = ttk.Entry(mainframe, width=5, textvariable=timer_hours)
time_entry_mins = ttk.Entry(mainframe, width=5, textvariable=timer_mins)
time_entry_secs = ttk.Entry(mainframe, width=5, textvariable=timer_secs)
time_entry_hours.grid(row=2, column=1)
time_entry_mins.grid(row=2, column=2)
time_entry_secs.grid(row=2, column=3)

# Create a label widget to display time left
time_label = ttk.Label(mainframe, textvariable=time_left, 
    font=("Tahoma", 40))
time_label.grid(row=3, column=1, columnspan=3)

# Define start, reset and pause buttons
button_start = ttk.Button(mainframe, text="Start", command=start_timer)
button_reset = ttk.Button(mainframe, text="Reset", command=reset_timer)
button_pause = ttk.Button(mainframe, text="Pause", command=pause_timer,
    state="disabled")
button_start.grid(row=4, column=1)
button_reset.grid(row=4, column=2)
button_pause.grid(row=4, column=3)

# Add padding around child widgets of mainframe
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

time_entry_mins.focus() # Focus on this entry widget at startup
root.bind('<Return>', start_timer)
root.bind('<space>', pause_timer)

root.mainloop()
