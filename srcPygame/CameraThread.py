import cv2
import threading
import pygame
from Timer import Timer
from Shapes import *

# An class that is derived from the thread class. 
#   1) CameraThread.start() method calls the CameraThread.run().
#       - The CameraThread.run() method gets the image from the assingned cameraId and stores it in self.image
#   2) CameraThread.join() method makes the main thread wait for the CameraThread to finish running.
#   3) Now the image can be accessed safely...
class CameraThread(threading.Thread):
    def __init__(self, cameraName, cameraId):
        threading.Thread.__init__(self, daemon=True)
        self.cameraName = cameraName
        self.cameraId = cameraId
        self.cvImage = None
        self.pyImage1 = None
        self.pyImage2 = None
        self.LastImg = 1;
        self._kill = False
        self._init = False
        self.pyImageSquare1 = None
        self.pyImageSquare2 = None
        self.imageDetection = False
        self.carCascade = cv2.CascadeClassifier("../resources/detection/cars4.xml")
        self.camera = None
        self.active = False

    def _cameraInit(self):
        self.camera = cv2.VideoCapture(self.cameraId)
        # set scaling for each image
        if self.cameraName == "rear":       # set image x, y size (full screen)
            # self.camera.set(3, 420)
            # self.camera.set(4, 270)
            pass
        elif self.cameraName == "left":     # set image x, y size (square image)
            self.camera.set(3, 375)
            self.camera.set(4, 375)
            self.imageDetection = True
        elif self.cameraName == "right":    # set image x, y size (square image)
            self.camera.set(3, 375)
            self.camera.set(4, 375)
            self.imageDetection = True
        # most efficient format.
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self._init = True

    def run(self):
        self.timer = Timer()

        self.init = False
        while self.init == False:
            try:
                self._cameraInit()
                self.init = True
            except:
                self.init = False
                self.timer.Sleep(1/60)
        self.active = False
        # main loop
        while not self._kill:
            # get the camera stream.
            if not self.camera.isOpened():
                self._cameraInit();
                continue
            elif not self.active:
                self.timer.Sleep((1/10))
            else:
                ret, self.cvImage = self.camera.read()
                if ret == False:
                    continue;
                # do image detection if enabled.
                if self.imageDetection:
                    self.gray = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2GRAY)
                    self.cars = self.carCascade.detectMultiScale(self.gray, 1.1, 1)
                    for (x,y,w,h) in self.cars:
                        cv2.rectangle(self.cvImage,(x,y),(x+w,y+h),(0,0,0),3)
                        cv2.rectangle(self.cvImage,(x,y),(x+w,y+h),(0,0,255),2)
                        break
                # load images into memory
                self.cvImage = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB).swapaxes(0,1)
                self._AssignPyImage()
                # Sleep after image is read.
                if(self.timer.GetElapsed().s() <= 1/30):
                    self.timer.Sleep((1/30 - self.timer.GetElapsed().s())*0.9)
            self.timer.Reset()
                
        self.camera.release()

    def _AssignPyImage(self):
        if self.cameraName != "rear":
            if self.LastImg == 2:
                self.pyImage1 = Image((0,0), img=pygame.transform.scale(pygame.surfarray.make_surface(self.cvImage), (375, 375)))
                #self.pyImage1 = Image((0,0), img=pygame.surfarray.make_surface(self.cvImage))
                self.LastImg = 1;
            elif self.LastImg == 1:
                self.pyImage2 = Image((0,0), img=pygame.transform.scale(pygame.surfarray.make_surface(self.cvImage), (375, 375)))
                #self.pyImage2 = Image((0,0), img=pygame.surfarray.make_surface(self.cvImage))
                self.LastImg = 2;
            elif self.LastImg == None:
                self.pyImage1 = Image((0,0), img=pygame.transform.scale(pygame.surfarray.make_surface(self.cvImage), (375, 375)))                        
                #self.pyImage1 = Image((0,0), img=pygame.surfarray.make_surface(self.cvImage))
                self.LastImg = 1;
        elif self.cameraName == "rear":
            if self.LastImg == 2:
                self.pyImage1 = Image((0,0), img=pygame.transform.scale(pygame.surfarray.make_surface(self.cvImage), (420, 270)))
                self.LastImg = 1;
            elif self.LastImg == 1:
                self.pyImage2 = Image((0,0), img=pygame.transform.scale(pygame.surfarray.make_surface(self.cvImage), (420, 270)))
                self.LastImg = 2;
            elif self.LastImg == None:                        
                self.pyImage1 = Image((0,0), img=pygame.transform.scale(pygame.surfarray.make_surface(self.cvImage), (420, 270)))
                self.LastImg = 1;
        
    def GetPyImage(self):
        if not self._init:
            return None
        if self.LastImg == 1:
            return self.pyImage1
        elif self.LastImg == 2: 
            return self.pyImage2
        elif self.LastImg == None:
            return None

    def Kill(self):
        self._kill = True
