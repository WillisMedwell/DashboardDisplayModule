from time import sleep
from PygameWindow import PygameWindow
from DisplayStateMachine import DisplayStateMachine
import pygame

def main():
    window = PygameWindow(1200, 400, "Car Dash")
    displayManager = DisplayStateMachine()
    while(window.IsRunning()):
        window.ProcessEvents()
        window.Draw(displayManager.get_shape_list())
        window.Refresh()
    window.Close()

if __name__ == "__main__":
    main()