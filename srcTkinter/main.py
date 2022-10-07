# window, drawing and other general gui 
from tkinter import Tk, Canvas, BOTH
# sleeping functionality
import time

# custom classes
from TkWindow import TkWindow
from DisplayStateMachine import *
from Timer import *

# 60 fps only required
FRAME_TIME = 1/60.0


def main():
    window = TkWindow()
    timer = Timer()
    display_manager = DisplayStateMachine()
    time_list = []
    
    # Render loop
    while(window.quit() != True):
        time_list.append(timer.get_elapsed().ms())
        timer.reset()
        # Measure average frame times.
        if len(time_list) == 100:
            print("{} ms, {} fps ".format(sum(time_list) / len(time_list), len(time_list)/sum(time_list)*1000))
            time_list = []

        # Clear last frame, draw frame, refresh screen to new frame.
        window.clear()
        window.draw(display_manager.GetDrawList())
        window.refresh()

if __name__ == "__main__":
    main()




