# pi specifics
import RPi.GPIO as GPIO

import sys, os
from time import sleep
from Timer import Timer
from PygameWindow import PygameWindow
from CameraThread import CameraThread
from DisplayStateMachine import *
import pygame
GPIO.setup()
GPIO.setmode(GPIO.BOARD)

# 10 = default
# 12 = rear
# 16 = left
# 18 = right
# increase
# decrease
# engine
# handbrake
GPIOInputPins = [ 10,12,16,18,22,24,36,38]

for pin in GPIOInputPins:
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def GetPinInputs():
    pressed = []
    for pin in GPIOInputPins:
        pressed.append(GPIO.input(pin)==GPIO.HIGH)
    return pressed;

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
        # inputs to change state.
        keys = pygame.key.get_pressed()
        pins = GetPinInputs()

        # keep average record of times.
        times.append(time.GetElapsed().ms())
        time.Reset()
        if len(times) == 100:
            print("{} ms, {} fps ".format(sum(times) / len(times), len(times)/sum(times)*1000))
            times = []

        if pins[0] == True:
            displayManager.SetState(DashState.DEFAULT)
            displayManager.SetDrivingState("D")
        elif pins[1] == True:
            displayManager.SetState(DashState.REAR_VIEW)
            displayManager.SetDrivingState("R")
        elif pins[2] == True:
            displayManager.SetState(DashState.LEFT_VIEW)
            displayManager.TurnOnLeftIndicator()
        elif pins[3] == True:
            displayManager.SetState(DashState.RIGHT_VIEW)
            displayManager.TurnOnRightIndicator()
        
        if pins[4] == True:
            speed += 2
            fuel += 0.01
            temp += 1
            rpm += 0.05
            displayManager.SetSpeed(speed)
            displayManager.SetFuel(fuel)
            displayManager.SetTemp(temp)
            displayManager.SetRpm(rpm)
        elif pins[5] == True:
            speed -= 2
            fuel -= 0.01
            temp -= 1
            rpm -= 0.05
            displayManager.SetSpeed(speed)
            displayManager.SetFuel(fuel)
            displayManager.SetTemp(temp)
            displayManager.SetRpm(rpm)
        
        if pins[6] == True:
            displayManager.TurnOnEngineWarning()
        else:
            displayManager.TurnOffEngineWarning()
        
        if pins[7] == True:
            displayManager.TurnOnHandbrakeWarning()
        else:
            displayManager.TurnOffHandbrakeWarning()

        ### DESKTOP SPECIFIC
        # change camera views
        # if keys[pygame.K_LEFT]:
        #     displayManager.SetState(DashState.LEFT_VIEW)
        #     displayManager.TurnOnLeftIndicator()
        # elif keys[pygame.K_RIGHT]:
        #     displayManager.SetState(DashState.RIGHT_VIEW)
        #     displayManager.TurnOnRightIndicator()
        # elif keys[pygame.K_UP]:
        #     displayManager.SetState(DashState.DEFAULT)
        #     displayManager.TurnOffIndicators()
        #     displayManager.SetDrivingState("D")
        # elif keys[pygame.K_DOWN]:
        #     displayManager.SetState(DashState.REAR_VIEW)
        #     displayManager.TurnOffIndicators()
        #     displayManager.SetDrivingState("R")
        

        # # change values
        # if keys[pygame.K_1]:
        #     speed += 2
        #     fuel += 0.01
        #     temp += 1
        #     rpm += 0.05
        #     displayManager.SetSpeed(speed)
        #     displayManager.SetFuel(fuel)
        #     displayManager.SetTemp(temp)
        #     displayManager.SetRpm(rpm)
        # elif keys[pygame.K_0]:
        #     speed -= 2
        #     fuel -= 0.01
        #     temp -= 1
        #     rpm -= 0.05
        #     displayManager.SetSpeed(speed)
        #     displayManager.SetFuel(fuel)
        #     displayManager.SetTemp(temp)
        #     displayManager.SetRpm(rpm)
        # elif keys[pygame.K_e]:
        #     displayManager.TurnOnEngineWarning()
        # elif keys[pygame.K_b]:
        #     displayManager.TurnOnHandbrakeWarning()
        
        if keys[pygame.K_ESCAPE]:
            break;
        
        # Drawing screen.
        window.Clear()
        window.ProcessEvents()
        window.Draw(displayManager.GetDrawList())
        window.Refresh()
    window.Close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e)
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e.with_traceback)
        exit(-1)