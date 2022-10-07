
from time import sleep
from Timer import Timer
from PygameWindow import PygameWindow
from CameraThread import CameraThread
from DisplayStateMachine import DisplayStateMachine
import pygame

def main():
    InstanceCameraThread = lambda : CameraThread("pc", 0)
    cameraThread = InstanceCameraThread()
    cameraThread.start()
    window = PygameWindow(1280, 400, "Car Dash")
    displayManager = DisplayStateMachine()
    time = Timer();
    times = [] 
    speed = 0;
    fuel = 0;
    temp = 50;
    rpm = 0;
    cameraDone = False
    cameraImg = None

    while(window.IsRunning()):
        # Timing collections
        while(time.GetElapsed().ms() <= 1/60*1000):
            pass
        #     #time.Sleep((1/60)-time.GetElapsed().s())

        if cameraThread.GetPyImage() != None:
            cameraImg = cameraThread.GetPyImage()            

        times.append(time.GetElapsed().ms())
        time.Reset()
        if len(times) == 100:
            print("{} ms, {} fps ".format(sum(times) / len(times), len(times)/sum(times)*1000))
            times = []

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            displayManager.TurnOnLeftIndicator()
        elif keys[pygame.K_RIGHT]:
            displayManager.TurnOnRightIndicator()
        elif keys[pygame.K_RETURN]:
            displayManager.TurnOffIndicators()

        if keys[pygame.K_UP]:
            speed += 2
            fuel += 0.01
            temp += 1
            rpm += 0.05
            displayManager.SetSpeed(speed)
            displayManager.SetFuel(fuel)
            displayManager.SetTemp(temp)
            displayManager.SetRpm(rpm)
        elif keys[pygame.K_DOWN]:
            speed -= 2
            fuel -= 0.01
            temp -= 1
            rpm -= 0.05
            displayManager.SetSpeed(speed)
            displayManager.SetFuel(fuel)
            displayManager.SetTemp(temp)
            displayManager.SetRpm(rpm)

        if window.WasKeyTyped(pygame.K_e):
            if displayManager._engineWarning:
                displayManager.TurnOffEngineWarning()
            else:
                displayManager.TurnOnEngineWarning()
        elif window.WasKeyTyped(pygame.K_b):
            if displayManager._handbrakeWarning:
                displayManager.TurnOffHandbrakeWarning()
            else:
                displayManager.TurnOnHandbrakeWarning()

        # Drawing screen.
        window.ProcessEvents()
        window.Draw(displayManager.GetDrawList())
        if cameraImg != None:
            pass
            #window.GetSurface().blit(cameraImg, (0,0))
        window.Refresh()

    window.Close()

if __name__ == "__main__":
    main()