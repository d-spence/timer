# Timer App - Written in Python using Tkinter GUI

import time, winsound, os
import datetime as dt

import timer.timer_tk


class Timer:

    # Timer Defaults
    hours_default = '0'
    mins_default = '1'
    secs_default = '0'

    def __init__(self, hours=hours_default, mins=mins_default, secs=secs_default):
        self.hours = hours
        self.mins = mins
        self.secs = secs
        self.t_initial = dt.timedelta(hours=int(self.hours), minutes=int(self.mins), 
            seconds=int(self.secs))
        self.is_active = False # Whether this is an active timer
        self.t_start = 0 # Time when timer was started stored as a float
        self.t_stop = 0 # Time when timer was stopped or paused
        self.t_total = dt.timedelta() # Total time ellapsed

    def start(self):
        self.t_start = time.time()
        self.is_active = True

    def stop(self):
        if self.is_active == True:
            self.t_stop = time.time()
            self.t_total += dt.timedelta(seconds=self.t_stop - self.t_start)

    def reset(self):
        self.t_start = self.t_stop = 0
        self.t_total = dt.timedelta()
        self.is_active = False

    def update_initial(self):
        self.t_initial = dt.timedelta(hours=int(self.hours), minutes=int(self.mins), 
            seconds=int(self.secs))


def get_formatted_time(t_duration=None, reset=False):
    # Return a formatted time string from a timedelta object (ex. HH:MM:SS.xx)

    if reset == True:
        t_duration = t1.t_initial # Override t_duration with initial time

    t_hours = t_duration.seconds // 3600
    t_mins = t_duration.seconds // 60
    t_secs = float(f"{t_duration.seconds}.{t_duration.microseconds}") % 60

    if t_mins > 60:
        t_mins = t_mins % 60 # Get remainder of minutes divided by the hour
        t_formatted = f"{t_hours:02d}:{t_mins:02d}:{t_secs:05.2f}"
    else:
        t_formatted = f"{t_mins:02d}:{t_secs:05.2f}"

    return t_formatted


def get_time_duration():
    # Gets the duration of time ellapsed so far returned as a timedelta object

    t_since_start = dt.timedelta(seconds=time.time() - t1.t_start) # Time since last start/unpause
    t_ellapsed = t1.t_total + t_since_start # Time ellapsed so far
    t_duration = t1.t_initial - t_ellapsed
    
    return t_duration


def play_sound(fn, sound_dir="sounds\\", loop=False):
    # Plays a sound specified by fn parameter

    cwd_path = os.getcwd()
    full_sound_path = os.path.join(cwd_path, sound_dir, fn)

    if loop == True:
        winsound.PlaySound(full_sound_path, 
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    else:
        winsound.PlaySound(full_sound_path, 
            winsound.SND_FILENAME | winsound.SND_ASYNC)


# Create a new timer
t1 = Timer()
