from tkinter import *
from tkinter import ttk

from timer.timer import t1, get_formatted_time, get_time_duration, play_sound


default_status_msg = "Enter timer duration..."
default_time = "00:00.00"

# Color values/names
color_status_bar = "light sky blue"
color_t_default = "black"
color_t_run = "green"
color_t_pause = "red"
color_t_done = "light gray"

# Sound file names
sound_t_start = "t_start.wav"
sound_t_reset = "t_reset.wav"
sound_t_pause = "t_reset.wav"
sound_t_done = "t_done.wav"

# Time remaining sounds; Key is the time in seconds and value is the sound file
sound_tr_dict = {'10':'tr_10_sec.wav', '30':'tr_30_sec.wav', '60':'tr_1_min.wav',
    '300':'tr_5_min.wav', '600':'tr_10_min.wav', '1800':'tr_30_min.wav',}
sound_tr_played = [] # Which alerts have already been played


def run_timer():
    global rt_callback

    t_duration = get_time_duration()

    # Check if timer has finished
    if t_duration.days < 0:
        stop_timer()
        return

    # Play audio notifications for time remaining
    for t in sound_tr_dict.keys():
        if t not in sound_tr_played:
            if int(t) == t_duration.seconds:
                play_sound(sound_tr_dict[t], sound_dir="sounds\\time_remaining\\")
                sound_tr_played.append(t)

    time_left.set(get_formatted_time(t_duration))
    rt_callback = root.after(10, run_timer) # Identifier used to cancel next call


def stop_timer():
    # Stops the timer when time is up

    root.after_cancel(rt_callback)
    root.attributes('-topmost', True) # Timer will come to the front when done
    root.attributes('-topmost', False)
    root.focus_force() # Will flash taskbar icon if not the active window

    play_sound(sound_t_done, loop=True)
    status_msg.set("Timer has finished!")
    set_time_color(color_t_done) # Timer text will appear lighter when done
    time_left.set(default_time)

    button_pause["state"] = "disabled" # Disable pause button
    root.bind('<space>', reset_timer) # Bind space to reset function


def start_timer(*args):
    # Starts the timer

    if t1.is_active == False:
        t1.hours = timer_hours.get()
        t1.mins = timer_mins.get()
        t1.secs = timer_secs.get()
        t1.update_initial()

    t1.start() # Start/restart timer and set as active
    play_sound(sound_t_start)
    status_msg.set("> Timer is running...")
    set_time_color(color_t_run)
    run_timer()
    
    # Disable start button until pause or reset button pressed
    button_start["state"] = "disabled"
    button_pause["state"] = "enabled"
    root.focus()
    root.bind('<space>', pause_timer) # Rebind space to pause function
        

def reset_timer(*args):
    # Resets the timer to initial state
    global sound_tr_played

    root.after_cancel(rt_callback)

    if t1.is_active == False:
        # Resets all entry fields back to zero if reset pressed when timer is inactive
        time_left.set(default_time)
        timer_hours.set(t1.hours_default)
        timer_mins.set('')
        timer_secs.set(t1.secs_default)
        time_entry_mins.focus() # Focus on minutes entry field
        status_msg.set(default_status_msg)
    else:
        time_left.set(get_formatted_time(t_duration=t1.t_initial, reset=True)) # Reset time display
        status_msg.set("Timer has been reset!")

    t1.reset()
    play_sound(sound_t_reset)
    sound_tr_played = [] # Reset time remaining played sounds
    set_time_color(color_t_default)

    # Disable/enable start and pause buttons
    button_start["state"] = "enabled"
    button_pause["state"] = "disabled"
    root.bind('<space>', start_timer) # Rebind space to start function


def pause_timer(*args):
    # Pauses the active timer

    root.after_cancel(rt_callback)

    if t1.is_active == True:
        t1.stop()
        play_sound(sound_t_pause)
        status_msg.set("|| Timer is paused...")
        set_time_color(color_t_pause)

        button_start["state"] = "enabled"
        button_pause["state"] = "disabled"
        root.bind('<space>', start_timer) # Rebind space to start function


def set_time_color(color="black"):
    # Sets the color of the time label

    time_label["foreground"] = color


# Set up main Tk window and title
root = Tk()
root.title("Timer")
root.iconbitmap("timer_icon.ico")
root.resizable(width=False, height=False)

# Set up variable classes to track changes
status_msg = StringVar(value=default_status_msg)
timer_hours = StringVar(value=t1.hours_default)
timer_mins = StringVar() # Left empty for faster input
timer_secs = StringVar(value=t1.secs_default)
time_left = StringVar(value=default_time)

# Create a themed frame widget within the main window to hold UI content
mainframe = ttk.Frame(root, padding="5 5 5 5", borderwidth=1, relief='sunken')
mainframe.grid(row=1, column=0, sticky=(N, W, E, S))

# Create a status bar
status_bar = ttk.Label(root, textvariable=status_msg, padding="3 3 3 3",
    borderwidth=1, relief='sunken', anchor=W, background=color_status_bar)
status_bar.grid(row=2, column=0, columnspan=3, sticky=[W, E])

# Create label widgets for hours, mins, and secs
time_label_hours = ttk.Label(mainframe, text="Hours").grid(row=1, column=1)
time_label_mins = ttk.Label(mainframe, text="Mins").grid(row=1, column=2)
time_label_secs = ttk.Label(mainframe, text="Secs").grid(row=1, column=3)

# Create entry widgets for getting timer length in hours, mins, and secs
time_entry_hours = ttk.Entry(mainframe, width=5, textvariable=timer_hours)
time_entry_mins = ttk.Entry(mainframe, width=5, textvariable=timer_mins)
time_entry_secs = ttk.Entry(mainframe, width=5, textvariable=timer_secs)
time_entry_hours.grid(row=2, column=1)
time_entry_mins.grid(row=2, column=2)
time_entry_secs.grid(row=2, column=3)

# Create a label widget to display time left
time_label = ttk.Label(mainframe, textvariable=time_left, padding="5 5 5 5",
    font=("Tahoma", 40), borderwidth=1, relief='groove')
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

# Key bindings
root.bind('<space>', start_timer)
