from Shapes import Shape, Oval, Image, Line, Text, Rectangle
from CameraThread import CameraThread
import pygame
import math
from datetime import datetime
from gpiozero import CPUTemperature

# Math
PI = 3.141592654
DEGREES_TO_RADIAN_FACTOR = PI/180
# Other constants
BACKGROUND_COLOUR = (0,0,0)
# Needle constants
NEEDLE_THICKNESS = 5
NEEDLE_COLOUR = (255,255,255)
# Sources of images
ENGINE_WARNING_IMG_SRC  = "../resources/images/enginewarning.png"
HANDBRAKE_IMG_SRC       = "../resources/images/handbrakewarning.png"
TEMPCOLD_IMG_SRC        = "../resources/images/tempcold.png"
FUELLOW_IMG_SRC         = "../resources/images/fuellow.png"
TEMPHOT_IMG_SRC         = "../resources/images/temphot.png"
DEFAULT_DASH_IMG_SRC    = "../resources/images/dash.png"
SPEEDRING_IMG_SRC       = "../resources/images/speedring.png"
RPMRING_IMG_SRC         = "../resources/images/rpmring.png"
FUELLINE_IMG_SRC        = "../resources/images/fuelline.png"
MASK_IMG_SRC            = "../resources/images/mask.png"
ARROW_LEFT_IMG_SRC      = "../resources/images/leftarrow.png"
ARROW_RIGHT_IMG_SRC     = "../resources/images/rightarrow.png"
STREAK_IMG_SRC          = "../resources/images/streaks.png"
REAR_OVERLAY_IMG_SRC    = "../resources/images/reverseoverlay.png"
SQAURE_IMG_SRC          = "../resources/images/square.png"
BLACKREAR_IMG_SRC       = "../resources/images/black420x270.png"

# font sources
FONT_DEFAULT            = "../resources/fonts/NotoSansJP.otf"

class DrawList():
    def __init__(self) -> None:
        self._shapes = []
        
        # start camera threads
        self._rearCamera = CameraThread("rear", 0)
        self._rearCamera.start()
        self._leftCamera = CameraThread("left", 2)
        self._leftCamera.start()
        self._rightCamera = CameraThread("right", 4)
        self._rightCamera.start()

        # initialise fonts
        self.fontMedium = pygame.font.Font(FONT_DEFAULT, 35)
        self.fontSmall  = pygame.font.Font(FONT_DEFAULT, 20)

        # fonts displayed
        self.speedText   = Text(590, 155, str(0), self.fontMedium, color=(255,255,255))
        self.kmhText     = Text(650, 173, "KMPH", self.fontSmall, color=(255,255,255))
        self.tempText    = Text(450, 75, "°C", self.fontSmall, color=(255,255,255))
        self.KmRemaining = Text(1150, 355, "Km", self.fontSmall, color=(255,255,255))
        self.systemtime  = Text(612, 75, str(datetime.now()), self.fontSmall, color=(255,255,255))
        self.drivingState= Text(625, 20, "P", self.fontMedium, color=(255,255,255))
        self.RPi4TempText= Text(10,10, "loading...", self.fontSmall)

        # masks, backgrounds and other images
        self.speedRing   = Image((50,12),           directory=SPEEDRING_IMG_SRC)
        self.rpmRing     = Image((1280-382-50,12),  directory=RPMRING_IMG_SRC)
        self.fuelLine    = Image((490-4,330),       directory=FUELLINE_IMG_SRC)
        self.streaks     = Image((510,200),         directory=STREAK_IMG_SRC)
        self.maskLeft    = Image((6,-2),            directory=MASK_IMG_SRC)
        self.maskRight   = Image((1280-8-465,-2),   directory=MASK_IMG_SRC)
        self.arrowLeft   = Image((400,20),          directory=ARROW_LEFT_IMG_SRC)
        self.arrowRight  = Image((880-69,20),       directory=ARROW_RIGHT_IMG_SRC)
        self.rearoverlay = Image((460, 305),        directory=REAR_OVERLAY_IMG_SRC)
        self.tempcold    = Image((560, 112),        directory=TEMPCOLD_IMG_SRC)
        self.temphot     = Image((560, 112),        directory=TEMPHOT_IMG_SRC)
        self.engine      = Image((600, 112),        directory=ENGINE_WARNING_IMG_SRC)
        self.handbrake   = Image((650, 112),        directory=HANDBRAKE_IMG_SRC)
        self.square      = Image((616, 25),         directory=SQAURE_IMG_SRC)
        self.blackrear   = Image((430, 110),        directory=BLACKREAR_IMG_SRC)

        # dynamically adjusted lines
        self.fuel       = Line(490-4, 360, 490-4, 360, 21, color=(200,200,200))
        self.topLinebar = Line(450, 105, 830, 105, 2, color=(255,255,255))

        # RPI monitors
        self.RPi4Temp  = CPUTemperature()

    def Add(self, shapes):
        if isinstance(shapes, list):
            for shape in shapes:
                self._shapes.append(shape)
        else:
            self._shapes.append(shapes)
    
    def Clear(self):
        self._shapes = []
        self.RPi4TempText._text = str(self.RPi4Temp.temperature)
        self._shapes.append(self.RPi4TempText)

    def SetToDefault(self, speed, rpm, fuel, temp, state):
        self.Clear()
        self._leftCamera.active = False
        self._rearCamera.active = False
        self._rightCamera.active = False
        self._AppendSpeedometer(speed)
        self._AppendRevmeter(rpm)
        self._AppendCenterSummary(speed, temp, fuel, state)

    def SetToLeftView(self, speed, rpm, fuel, temp, state):
        self.Clear()
        self._leftCamera.active = True
        self._rearCamera.active = False
        self._rightCamera.active = False
        # image cropping
        img = self._leftCamera.GetPyImage();
        if img != None:
            img.set_x(50)
            img.set_y(12)
            self._shapes.append(img)
        # overlay mask
        self._shapes.append(self.maskLeft)
        # everything else
        self._AppendRevmeter(rpm)
        self._AppendCenterSummary(speed, temp, fuel, state)

    def SetToRightView(self, speed, rpm, fuel, temp, state):
        self.Clear()
        # image cropping
        self._rightCamera.active = True
        self._rearCamera.active = False
        self._leftCamera.active = False

        img = self._rightCamera.GetPyImage();
        if img != None:
            img.set_x(1280-132-375+82)
            img.set_y(12)
            self._shapes.append(img)
        # overlay mask
        self._shapes.append(self.maskRight)
        # everything else
        self._AppendSpeedometer(speed)
        self._AppendCenterSummary(speed, temp, fuel, state)
        
    def SetToRearView(self, speed, rpm, fuel, temp, state):
        self.Clear()
        self._AppendCenterSummary(speed, temp, fuel, state)
        self._rearCamera.active = True
        self._leftCamera.active = False
        self._rightCamera.active = False

        # everything else
        self._AppendSpeedometer(speed)
        self._AppendRevmeter(rpm)

        img = self._rearCamera.GetPyImage();
        if img != None:
            img.set_x((1280/2) - (img.width/2))
            img.set_y(400 - img.height - 20)
            self._shapes.append(img)
        else:
            self._shapes.append(self.blackrear)
        self._shapes.append(self.rearoverlay)

    def AddLeftIndicator(self):
        self._shapes.append(self.arrowLeft)

    def AddRightIndicator(self):
        self._shapes.append(self.arrowRight)

    def __del__(self):
        self._rearCamera.Kill()
        self._leftCamera.Kill()
        self._rightCamera.Kill()

        self._rearCamera.join()
        self._leftCamera.join()
        self._rightCamera.join()

    def _AppendSpeedometer(self, speed):
        # speed ring background
        self._shapes.append(self.speedRing)
        # speed needle
        self._shapes.append(GetNeedle(0, 210, 240, -30, speed, (320-82, 200), 180))

    def _AppendRevmeter(self, rpm):
        # rpm ring background
        self._shapes.append(self.rpmRing)
        # rpm needle
        self._shapes.append(GetNeedle(0, 210, 6, -30, rpm, (1280 - 320 + 75, 200), 180))

    def _AppendCenterSummary(self, speed, temp, fuel, state):
        # speed text
        self.speedText._text=str(speed)
        self._shapes.append(self.speedText)
        self._shapes.append(self.kmhText)
        # system time
        self.systemtime._text = str(datetime.now().strftime("%H:%M"))
        self._shapes.append(self.systemtime)
        # temp text
        self.tempText._text=str(temp) + "°C"
        self._shapes.append(self.tempText)
        # fuel meter
        if fuel > 1:
            fuel = 1
        elif fuel < 0:
            fuel = 0
        self.fuel.x2 = 490-3 + (298 * fuel)
        self._shapes.append(self.fuel)
        # fuel line
        self._shapes.append(self.fuelLine)
        self._shapes.append(self.topLinebar)
        # streak lines
        self._shapes.append(self.streaks)
        # driving state
        self._shapes.append(self.square)
        self.drivingState._text=str(state)
        self._shapes.append(self.drivingState)


    def _AppendLeftCamera(self):
        pass

    def _AppendRightCamera(self):
        pass
    
    def AddCold(self):
        self._shapes.append(self.tempcold)
    def AddHot(self):
        self._shapes.append(self.temphot)
    def AddEngine(self):
        self._shapes.append(self.engine)
    def AddHandbrake(self):
        self._shapes.append(self.handbrake)
    def AddFuelLow(self):
        self._shapes.append(self.fuellow)

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

        
