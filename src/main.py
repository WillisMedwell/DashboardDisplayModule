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
        print('{} -> {}'.format(timer.get_elapsed().s(), FRAME_TIME))
        if timer.get_elapsed().s() >= FRAME_TIME:
            timer.reset()
            # Clear last frame, draw frame, refresh screen to new frame.
            window.clear()
            window.draw(display_manager.get_shape_list())
            window.refresh()

            # Measure average frame times.
            time_list.append(timer.get_last_lap().s())
            if len(time_list) == 100:
                time_elapsed_average = sum(time_list) / len(time_list)
                print("%.2f ms, %.2f fps" % (time_elapsed_average*1000, 1/time_elapsed_average))
                time_list = []
            
            print('')
            print(timer.get_elapsed().s())

            # Sleep for ~70% of remaining time.
            #print('{} VS {}'.format(timer.get_elapsed().s(), FRAME_TIME))
            if timer.get_elapsed().s() < FRAME_TIME:
               time_remaining = FRAME_TIME - timer.get_elapsed().s()
               timer.sleep(time_remaining)
               print("sleep")
        
            print(timer.get_elapsed().s())

if __name__ == "__main__":
    main()




