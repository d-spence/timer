from tkinter import *
from tkinter import ttk

from timer.timer import get_formatted_time, t1


def run_timer_tk():
    global rt_callback

    time_left.set(get_formatted_time())
    rt_callback = root.after(10, run_timer_tk)


def start_timer(*args):
    # Starts the timer

    try:
        if t1.is_active == False:
            t1.hours = timer_hours.get()
            t1.mins = timer_mins.get()
            t1.secs = timer_secs.get()
            t1.update_initial()

        t1.start() # Start/restart timer and set as active
        run_timer_tk()
        
        # Disable start button until pause or reset button pressed
        button_start["state"] = "disabled"
        button_pause["state"] = "enabled"
    except NameError:
        pass
        

def reset_timer(*args):
    # Resets the timer to initial state

    if t1.is_active == False:
        # Resets all entry fields back to zero if reset pressed when timer is inactive
        timer_hours.set(t1.hours_default)
        timer_mins.set(t1.mins_default)
        timer_secs.set(t1.secs_default)
        time_entry_mins.focus() # Focus on minutes entry field

    t1.reset()
    time_left.set("00:00.00")

    # Disable/enable start and pause buttons
    button_start["state"] = "enabled"
    button_pause["state"] = "disabled"


def pause_timer(*args):
    # Pauses the active timer

    if t1.is_active == True:
        t1.stop()
        button_start["state"] = "enabled"
        button_pause["state"] = "disabled"

    root.after_cancel(rt_callback)


# Set up main Tk window and title
root = Tk()
root.title("Timer")
root.resizable(width=False, height=False)

# Create a themed frame widget within the main window to hold UI content
mainframe = ttk.Frame(root, padding="3 3 3 3", borderwidth=5, relief='sunken')
mainframe.grid(row=0, column=0, sticky=(N, W, E, S), padx=5, pady=5)
root.columnconfigure(0, weight=1) # Expand frame if window is resized
root.rowconfigure(0, weight=1)

# Set up variable classes to track changes
timer_hours = StringVar(value=t1.hours_default)
timer_mins = StringVar()
timer_secs = StringVar(value=t1.secs_default)
time_left = StringVar(value="00:00.00")

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
