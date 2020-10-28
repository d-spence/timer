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
    # Return a formatted time string from a timedelta object

    if reset == True:
        if t_duration.seconds >= 3600:
            return f"{str(t_duration)}.00"
        else:
            return f"{str(t_duration)[2:]}.00"
    else:
        if t_duration.seconds >= 3600:
            return f"{str(t_duration)[0:-4]}"
        else:
            return f"{str(t_duration)[2:-4]}"


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
