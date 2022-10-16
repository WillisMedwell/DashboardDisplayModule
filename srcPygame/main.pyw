
from time import sleep
from Timer import Timer
from PygameWindow import PygameWindow
from CameraThread import CameraThread
from DisplayStateMachine import *
import pygame

def main():
    window = PygameWindow(1280, 400, "Car Dash")
    displayManager = DisplayStateMachine()
    time = Timer();
    times = [] 
    speed = 0;
    fuel = 0;
    temp = 50;
    rpm = 0;

    while(window.IsRunning()):
        # Sleep on windows system is very hit and miss; however, on linux it is very good. 
        # So this improves efficiency on the targeted device.
        while(time.GetElapsed().s() <= 1/60):
            time.Sleep(((1/60)-time.GetElapsed().s())*0.9)

        # keep average record of times.
        times.append(time.GetElapsed().ms())
        time.Reset()
        if len(times) == 100:
            print("{} ms, {} fps ".format(sum(times) / len(times), len(times)/sum(times)*1000))
            times = []

        # inputs to change state.
        keys = pygame.key.get_pressed()

        # change camera views
        if keys[pygame.K_LEFT]:
            displayManager.SetState(DashState.LEFT_VIEW)
            displayManager.TurnOnLeftIndicator()
        elif keys[pygame.K_RIGHT]:
            displayManager.SetState(DashState.RIGHT_VIEW)
            displayManager.TurnOnRightIndicator()
        elif keys[pygame.K_UP]:
            displayManager.SetState(DashState.DEFAULT)
            displayManager.TurnOffIndicators()
            displayManager.SetDrivingState("D")
        elif keys[pygame.K_DOWN]:
            displayManager.SetState(DashState.REAR_VIEW)
            displayManager.TurnOffIndicators()
            displayManager.SetDrivingState("R")
        

        # change values
        if keys[pygame.K_1]:
            speed += 2
            fuel += 0.01
            temp += 1
            rpm += 0.05
            displayManager.SetSpeed(speed)
            displayManager.SetFuel(fuel)
            displayManager.SetTemp(temp)
            displayManager.SetRpm(rpm)
        elif keys[pygame.K_0]:
            speed -= 2
            fuel -= 0.01
            temp -= 1
            rpm -= 0.05
            displayManager.SetSpeed(speed)
            displayManager.SetFuel(fuel)
            displayManager.SetTemp(temp)
            displayManager.SetRpm(rpm)
        elif keys[pygame.K_e]:
            displayManager.TurnOnEngineWarning()
        elif keys[pygame.K_b]:
            displayManager.TurnOnHandbrakeWarning()
        
        if keys[pygame.K_ESCAPE]:
            break;
        
        # Drawing screen.
        window.Clear()
        window.ProcessEvents()
        window.Draw(displayManager.GetDrawList())
        window.Refresh()
    window.Close()

if __name__ == "__main__":
    main()