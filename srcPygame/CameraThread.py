from pickletools import pyfloat
import cv2
import threading
import pygame
import numpy

# An class that is derived from the thread class. 
#   1) CameraThread.start() method calls the CameraThread.run().
#       - The CameraThread.run() method gets the image from the assingned cameraId and stores it in self.image
#   2) CameraThread.join() method makes the main thread wait for the CameraThread to finish running.
#   3) Now the image can be accessed safely...
class CameraThread(threading.Thread):
    def __init__(self, cameraName, cameraId):
        threading.Thread.__init__(self)
        self.cameraName = cameraName
        self.cameraId = cameraId
        self.camera = cv2.VideoCapture(self.cameraId)
        self.cvImage = None
        self.pyImage1 = None
        self.pyImage2 = None
        self.LastImg = 1;
    
    def run(self):
        while True:
            if not self.camera.isOpened():
                self.camera = cv2.VideoCapture(self.cameraId)
            else:
                ret, self.cvImage = self.camera.read()
                self.cvImage = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB).swapaxes(0,1)
                if self.LastImg == 2:
                    self.pyImage1 = pygame.surfarray.make_surface(self.cvImage)
                    self.LastImg = 1;
                elif self.LastImg == 1:
                    self.pyImage2 = pygame.surfarray.make_surface(self.cvImage)
                    self.LastImg = 2;
                elif self.LastImg == None:
                    self.pyImage1 = pygame.surfarray.make_surface(self.cvImage)
                    self.LastImg = 1;
                

    def GetPyImage(self):
        if self.LastImg == 1:
            return self.pyImage1
        elif self.LastImg == 2: 
            return self.pyImage2
        elif self.LastImg == None:
            return None






# class camThread(threading.Thread):
#     def __init__(self, previewName, camID):
#         threading.Thread.__init__(self)
#         self.previewName = previewName
#         self.camID = camID
#     def run(self):
#         print("Starting " + self.previewName)
#         camPreview(self.previewName, self.camID)

# def camPreview(previewName, camID):
#     cv2.namedWindow(previewName)
#     cam = cv2.VideoCapture(camID)
#     if cam.isOpened():
#         rval, frame = cam.read()
#     else:
#         rval = False

#     while rval:
#         cv2.imshow(previewName, frame)
#         rval, frame = cam.read()
#         key = cv2.waitKey(20)
#         if key == 27:  # exit on ESC
#             break
#     cv2.destroyWindow(previewName)

# # Create threads as follows
# thread1 = camThread("Camera 1", 0)
# thread2 = camThread("Camera 2", 1)
# thread3 = camThread("Camera 3", 2)

# thread1.start()
# thread2.start()
# thread3.start()
# print()
# print("Active threads", threading.activeCount())