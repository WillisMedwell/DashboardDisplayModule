# window, drawing and other general gui 
from tkinter import Tk, Canvas, BOTH
# frame timing 
import time

# custom classes
from TkWindow import TkWindow
from DisplayStateMachine import *

# 60 fps only required
FRAME_TIME = 1/60.0

def main():
    window = TkWindow()
    time_start = time.perf_counter()
    display_manager = DisplayStateMachine()
    has_drawable_list = False

    ## update loop
    while(window.quit() != True):
        time_elapsed = time.perf_counter() - time_start

        if has_drawable_list != True:
            has_drawable_list = True
            window.draw(display_manager.get_shape_list())

        if time_elapsed >= FRAME_TIME:
            ## Render frame.
            print(1/time_elapsed)
            window.refresh_screen()
            time_start = time.perf_counter()
            has_drawable_list = False
        else:
            pass
            # Sleep for 50% of the time to save power. 
            # This will have to be adjusted to accomodate other logic.
            if time_elapsed < FRAME_TIME * 0.02:
                time.sleep(FRAME_TIME*0.5)

if __name__ == "__main__":
    main()




