from Shapes import Shape, Oval, Image, Line, Text, Rectangle
from CameraThread import CameraThread
import pygame
import math
from datetime import datetime


# Math
PI = 3.141592654
DEGREES_TO_RADIAN_FACTOR = PI/180

# other constants
BACKGROUND_COLOUR = (0,0,0)

# needle constants
NEEDLE_THICKNESS = 5
NEEDLE_COLOUR = (255,255,255)

# Sources of images
DEFAULT_DASH_IMG_SRC    = "resources/images/dash.png"
LEFT_ARROW_IMG_SRC      = "resources/images/leftarrow.png"
RIGHT_ARROW_IMG_SRC     = "resources/images/rightarrow.png"
ENGINE_WARNING_IMG_SRC  = "resources/images/enginewarning.png"
HANDBRAKE_IMG_SRC       = "resources/images/handbrake.png"
SPEEDRING_IMG_SRC       = "resources/images/speedring.png"
RPMRING_IMG_SRC         = "resources/images/rpmring.png"
FUELLINE_IMG_SRC        = "resources/images/fuelline.png"
MASK_IMG_SRC            = "resources/images/mask.png"
STREAK_IMG_SRC          = "resources/images/Streaks.png"


# font sources
FONT_DEFAULT = "resources/fonts/NotoSansJP.otf"


class DrawList():
    def __init__(self) -> None:
        self._shapes = []
        
        # start camera threads
        self._rearCamera = CameraThread("rear", 0)
        self._rearCamera.start()
        self._leftCamera = CameraThread("left", 1)
        self._leftCamera.start()
        self._rightCamera = CameraThread("right", 2)
        self._rightCamera.start()

        # initialise fonts
        self.fontMedium = pygame.font.Font(FONT_DEFAULT, 35)
        self.fontSmall  = pygame.font.Font(FONT_DEFAULT, 20)

        self.speedText  = Text(590, 155, str(0), self.fontMedium, color=(255,255,255))
        self.kmhText    = Text(650, 173, "KMPH", self.fontSmall, color=(255,255,255))
        self.tempText   = Text(500, 62, "°C", self.fontSmall, color=(255,255,255))
        self.KmRemaining   = Text(1150, 355, "Km", self.fontSmall, color=(255,255,255))

        self.speedRing  = Image((132,12), directory=SPEEDRING_IMG_SRC)
        self.rpmRing    = Image((1148-378,12), directory=RPMRING_IMG_SRC)
        self.fuelLine   = Image((490,345), directory=FUELLINE_IMG_SRC)
        self.streaks   = Image((510,200), directory=STREAK_IMG_SRC)
        self.maskLeft   = Image((88,0), directory=MASK_IMG_SRC)
        self.maskRight  = Image((1280 - 88 - 465,0), directory=MASK_IMG_SRC)

        self.fuel       = Line(490, 378, 490, 378, 22, color=(255,255,255))
        self.topLinebar = Line(510, 90, 750, 90, 2, color=(255,255,255))

        ##TIme
       
        self._systemtime  = Text(600,62, str(datetime.now()), self.fontSmall, color=(255,255,255))


    def Add(self, shapes):
        if isinstance(shapes, list):
            for shape in shapes:
                self._shapes.append(shape)
        else:
            self._shapes.append(shapes)
    
    def Clear(self):
        self._shapes = []

    def SetToDefault(self, speed, rpm, fuel, temp):
        self.Clear()
        # speed needle
        
        # speed ring
        self._shapes.append(self.speedRing)
        # speed text
        self.speedText._text=str(speed)
        self._shapes.append(self.speedText)
        self._shapes.append(self.kmhText)
        # rpm needle
        
        # rpm ring
        self._shapes.append(self.rpmRing)
        # temp text
        self.tempText._text=str(temp) + "°C"
        self._shapes.append(self.tempText)
        # fuel line
        self._shapes.append(self.fuelLine)
        # fuel meter
        if fuel > 1:
            fuel = 1
        elif fuel < 0:
            fuel = 0
        self.fuel.x2 = 491 + (298 * fuel)
        self._shapes.append(self.fuel)
        self._shapes.append(self.topLinebar)
        self._shapes.append(self.KmRemaining)
        self._shapes.append(GetNeedle(0, 210, 240, -30, speed, (320, 200), 180))
        self._shapes.append(GetNeedle(0, 210, 6, -30, rpm, (1280 - 320, 200), 180))

        self._shapes.append(self.streaks)

        ##TIME
        self._systemtime._text = str(datetime.now().strftime("%H:%M"))
        self._shapes.append(self._systemtime)
    def SetToLeftView(self, speed, rpm, fuel, temp):
        self.Clear()

        # image cropping
        img = self._rearCamera.GetSquarePyImage();
        if img != None:
            img.set_x(132)
            img.set_y(12)
            self._shapes.append(img)
        self._shapes.append(self.maskLeft)
        # speed text
        self.speedText._text=str(speed)
        self._shapes.append(self.speedText)
        self._shapes.append(self.kmhText)
        # rpm needle
        self._shapes.append(GetNeedle(0, 210, 6, -30, rpm, (1280 - 320, 200), 180))
        # rpm ring
        self._shapes.append(self.rpmRing)
        # temp text
        self.tempText._text=str(temp) + "°C"
        self._shapes.append(self.tempText)
        # fuel line
        self._shapes.append(self.fuelLine)
        # fuel meter
        if fuel > 1:
            fuel = 1
        elif fuel < 0:
            fuel = 0
        self.fuel.x2 = 491 + (298 * fuel)
        self._shapes.append(self.fuel)

    def SetToRightView(self, speed, rpm, fuel, temp):
        self.Clear()
        # image cropping
        img = self._rearCamera.GetSquarePyImage();
        if img != None:
            img.set_x(1280-132-375)
            img.set_y(12)
            self._shapes.append(img)
        self._shapes.append(self.maskRight)
        # speed needle
        self._shapes.append(GetNeedle(0, 210, 240, -30, speed, (320, 200), 180))
        # speed ring
        self._shapes.append(self.speedRing)
        # speed text
        self.speedText._text=str(speed)
        self._shapes.append(self.speedText)
        self._shapes.append(self.kmhText)
        # temp text
        self.tempText._text=str(temp) + "°C"
        self._shapes.append(self.tempText)
        # fuel line
        self._shapes.append(self.fuelLine)
        # fuel meter
        if fuel > 1:
            fuel = 1
        elif fuel < 0:
            fuel = 0
        self.fuel.x2 = 491 + (298 * fuel)
        self._shapes.append(self.fuel)
        
    def SetToRearView(self):
        self.Clear()
        img = self._rearCamera.GetPyImage();
        if img != None:
            img.set_x(1280/2)
            img.set_y(0)
            self._shapes.append(img)

    
    def __del__(self):
        self._rearCamera.Kill()
        self._leftCamera.Kill()
        self._rightCamera.Kill()

        self._rearCamera.join()
        self._leftCamera.join()
        self._rightCamera.join()

def GetNeedle(minValue, minAngle, maxValue, maxAngle, value, origin, length):
    valueClamped = value
    if(value < minValue):
        valueClamped = minValue
    elif(value > maxValue):
        valueClamped = maxValue
    # y = m*x + c
    m = (maxAngle-minAngle)/(maxValue-minValue)
    c = maxAngle - (m * maxValue)
    angle = (m*valueClamped) + c
    # rotate vector (1,0) by angle
    angleRadians = angle * DEGREES_TO_RADIAN_FACTOR
    # start and end points of speed needle line.
    x1 = origin[0] 
    y1 = origin[1] 
    x2 = math.cos(angleRadians) * length + origin[0]
    y2 = - math.sin(angleRadians) * length + origin[1]
    return Line(x1, y1, x2, y2, NEEDLE_THICKNESS, color = NEEDLE_COLOUR)
        
# def _GetSpeedNeedle(self):
#     return self._GetNeedle(
#         Const.SPEED_MIN, 
#         Const.SPEED_NEEDLE_MIN_ANGLE, 
#         Const.SPEED_MAX, 
#         Const.SPEED_NEEDLE_MAX_ANGLE, 
#         self._speed, 
#         Const.SPEED_NEEDLE_POS, 
#         Const.SPEED_NEEDLE_LENGTH
#     )
# def _GetFuelNeedle(self):
#     return self._GetNeedle(
#         Const.FUEL_MIN, 
#         Const.FUEL_NEEDLE_MIN_ANGLE, 
#         Const.FUEL_MAX, 
#         Const.FUEL_NEEDLE_MAX_ANGLE, 
#         self._fuel, 
#         Const.FUEL_NEEDLE_POS, 
#         Const.FUEL_NEEDLE_LENGTH
#     )
# def _GetTempNeedle(self):
#     return self._GetNeedle(
#         Const.TEMP_MIN, 
#         Const.TEMP_NEEDLE_MIN_ANGLE, 
#         Const.TEMP_MAX, 
#         Const.TEMP_NEEDLE_MAX_ANGLE, 
#         self._temp, 
#         Const.TEMP_NEEDLE_POS, 
#         Const.TEMP_NEEDLE_LENGTH
#     )
# def _GetRpmNeedle(self):
#     return self._GetNeedle(
#         Const.RPM_MIN, 
#         Const.RPM_NEEDLE_MIN_ANGLE, 
#         Const.RPM_MAX, 
#         Const.RPM_NEEDLE_MAX_ANGLE, 
#         self._rpm, 
#         Const.RPM_NEEDLE_POS, 
#         Const.RPM_NEEDLE_LENGTH
#     )