
import tkinter
from tkinter.constants import *

DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 400

class TkWindow():
    # Private
    _window = None
    _canvas = None

    # Constructor
    def __init__(self, width = DEFAULT_WINDOW_WIDTH, height = DEFAULT_WINDOW_HEIGHT):
        if TkWindow._window is not None:
            raise Exception("Error: Paper has already been created, there can be only one.")
        try:
            TkWindow._window = tkinter.Tk()
        except ValueError:
            raise Exception("Error: could not instantiate tkinter object")

        # Set some attributes
        self._window.title("Dashboard")
        self._window.geometry(str(width)+"x"+str(height))
        self._window.Window_width = width
        self._window.Window_height = height
        self._window.resizable(False,False)

        # Create a tkinter canvas object to draw on
        TkWindow._canvas = tkinter.Canvas(TkWindow._window, bg = 'white')
        TkWindow._canvas.pack(fill=BOTH, expand=YES)

    
    def clear(self):
        self.get_canvas().delete('all')
    
    # Draws to screen. Only appears once screen is refreshed.
    def draw(self, shape_list):
        for shape in shape_list:
            shape.draw(self)

    # Redraws the screen
    def refresh(self):
        try:
            self.get_canvas().update()
            self.get_canvas().update_idletasks()
        except:
            print("Quitting...")
            exit(0)

    # Returns true when want to quit
    def quit(self):
        if TkWindow._window.state() == 'normal':
            return False
        else:
            return True
    
    def get_width(this): 
        return TkWindow._canvas.winfo_width()

    def get_height(this): 
        return TkWindow._canvas.winfo_height()

    def get_canvas(self):
        return TkWindow._canvas

    def get_mouseX(self):
        x = self._window.winfo_pointerx() - self._window.winfo_rootx()
        if x <= self._window.winfo_width() and x >= 0:
            return x
        else:
            return None

    def get_mouseY(self):
        y = self._window.winfo_pointery() - self._window.winfo_rooty()
        if y <= self._window.winfo_height() and y >= 0:
            return y
        else:
            return None
    
    def get_mouseXY(self):
        if self.get_mouseX() == None or self.get_mouseY() == None:
            return None
        else:
            return self.get_mouseX(), self.get_mouseY()