from enum import Enum
from itertools import count
import math
from Shapes import Shape, Rectangle, Oval, Triangle, Image, Line


class Const():
    PI = 3.141592654

    SPEED_MIN = 0;
    SPEED_MAX = 240
    SPEED_NEEDLE_LENGTH = 180
    SPEED_NEEDLE_MIN_ANGLE = 198
    SPEED_NEEDLE_MAX_ANGLE = -18
    SPEED_NEEDLE_POS = (351,238)

    FUEL_MIN = 0
    FUEL_MAX = 1
    FUEL_NEEDLE_LENGTH = 100
    FUEL_NEEDLE_MIN_ANGLE = 0
    FUEL_NEEDLE_MAX_ANGLE = 89.5
    FUEL_NEEDLE_POS = (1065,137)

    TEMP_MIN = 50
    TEMP_MAX = 150
    TEMP_NEEDLE_LENGTH = 100
    TEMP_NEEDLE_MIN_ANGLE = 180
    TEMP_NEEDLE_MAX_ANGLE = 89.5
    TEMP_NEEDLE_POS = (136,137)

    RPM_MIN = 0
    RPM_MAX = 6
    RPM_NEEDLE_LENGTH = 180
    RPM_NEEDLE_MIN_ANGLE = 198
    RPM_NEEDLE_MAX_ANGLE = -18
    RPM_NEEDLE_POS = (851,238)

    NEEDLE_THICKNESS = 5
    NEEDLE_COLOUR = (128,128,128)

    DEGREES_TO_RADIAN_FACTOR = PI/180
    
    DEFAULT_DASH_IMG_SRC = "images/dash.png"
    DEFAULT_DASH_POS = (0, 0)
    LEFT_ARROW_IMG_SRC = "images/leftarrow.png"
    LEFT_ARROW_IMG_POS = (540-62, 20)
    RIGHT_ARROW_IMG_SRC = "images/rightarrow.png"
    RIGHT_ARROW_IMG_POS = (660, 20)
    ENGINE_WARNING_IMG_SRC = "images/enginewarning.png"
    ENGINE_WARNING_IMG_POS = (550, 59)
    HANDBRAKE_IMG_SRC = "images/handbrake.png"
    HANDBRAKE_IMG_POS = (610, 60)


class DashState(Enum):
    DEFAULT = 0
    LEFT_VIEW = 1
    RIGHT_VIEW = 2
    REAR_VIEW = 3

class DisplayStateMachine():
    def __init__(self):
        self._state = DashState.DEFAULT
        self._defaultDrawList = self._DefualtContents()
        self._leftDrawList    = self._LeftViewContents()
        self._rightDrawList   = self._RightViewContents()
        self._rearDrawList    = self._RearViewContents()
        self._rightIndicator   = False
        self._leftIndicator    = False
        self._engineWarning    = False
        self._handbrakeWarning = False 
        self._speed = 0
        self._fuel  = 0
        self._temp  = 0
        self._rpm   = 0

        self._handbrakeObj     = Image(Const.HANDBRAKE_IMG_POS, directory = Const.HANDBRAKE_IMG_SRC)
        self._leftArrowObj     = Image(Const.LEFT_ARROW_IMG_POS, directory = Const.LEFT_ARROW_IMG_SRC)
        self._rightArrowObj    = Image(Const.RIGHT_ARROW_IMG_POS, directory = Const.RIGHT_ARROW_IMG_SRC)
        self._enginewarningObj = Image(Const.ENGINE_WARNING_IMG_POS, directory = Const.ENGINE_WARNING_IMG_SRC) 
    def SetState(self, state):
        _state = DashState(state)

    def GetDrawList(self):
        output = [];

        # Major layout objects that need to be drawn
        if self._state == DashState.DEFAULT:
            for obj in self._defaultDrawList:
                output.append(obj)
            output.append(self._GetSpeedNeedle())
            output.append(self._GetFuelNeedle())
            output.append(self._GetTempNeedle())
            output.append(self._GetRpmNeedle())
            if self._engineWarning:
                output.append(self._enginewarningObj)
            if self._handbrakeWarning:
                output.append(self._handbrakeObj)
            if self._leftIndicator: 
                output.append(self._leftArrowObj)
            if self._rightIndicator:
                output.append(self._rightArrowObj)
        else:
            raise Exception("The desired state does not exist (line 33 DisplayManager.py)")
        return output

    def _DefualtContents(self):
        return [
            Image(Const.DEFAULT_DASH_POS, directory = Const.DEFAULT_DASH_IMG_SRC),
        ]

    def _LeftViewContents(self):
        return []
    
    def _RightViewContents(self):
        return []

    def _RearViewContents(self):
        return []

    def TurnOnLeftIndicator(self):
        self._leftIndicator = True;
        self._rightIndicator = False;
    def TurnOnRightIndicator(self):
        self._leftIndicator = False;
        self._rightIndicator = True;
    def TurnOffIndicators(self):
        self._leftIndicator = False
        self._rightIndicator = False
    def TurnOnEngineWarning(self):
        self._engineWarning = True
    def TurnOffEngineWarning(self):
        self._engineWarning = False
    def TurnOnHandbrakeWarning(self):
        self._handbrakeWarning = True
    def TurnOffHandbrakeWarning(self):
        self._handbrakeWarning = False
    
    def SetSpeed(self, speed):
        self._speed = speed
    def SetFuel(self, fuel):
        self._fuel = fuel
    def SetTemp(self, temp):
        self._temp = temp
    def SetRpm(self, rpm):
        self._rpm = rpm

    def _GetNeedle(self, minValue, minAngle, maxValue, maxAngle, value, origin, length, ):
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
        angleRadians = angle * Const.DEGREES_TO_RADIAN_FACTOR
        # start and end points of speed needle line.
        x1 = origin[0]
        y1 = origin[1]
        x2 = math.cos(angleRadians) * length + origin[0]
        y2 = - math.sin(angleRadians) * length + origin[1]
        return Line(x1, y1, x2, y2, Const.NEEDLE_THICKNESS, color=Const.NEEDLE_COLOUR)
    def _GetSpeedNeedle(self):
        return self._GetNeedle(
            Const.SPEED_MIN, 
            Const.SPEED_NEEDLE_MIN_ANGLE, 
            Const.SPEED_MAX, 
            Const.SPEED_NEEDLE_MAX_ANGLE, 
            self._speed, 
            Const.SPEED_NEEDLE_POS, 
            Const.SPEED_NEEDLE_LENGTH
        )
    def _GetFuelNeedle(self):
        return self._GetNeedle(
            Const.FUEL_MIN, 
            Const.FUEL_NEEDLE_MIN_ANGLE, 
            Const.FUEL_MAX, 
            Const.FUEL_NEEDLE_MAX_ANGLE, 
            self._fuel, 
            Const.FUEL_NEEDLE_POS, 
            Const.FUEL_NEEDLE_LENGTH
        )
    def _GetTempNeedle(self):
        return self._GetNeedle(
            Const.TEMP_MIN, 
            Const.TEMP_NEEDLE_MIN_ANGLE, 
            Const.TEMP_MAX, 
            Const.TEMP_NEEDLE_MAX_ANGLE, 
            self._temp, 
            Const.TEMP_NEEDLE_POS, 
            Const.TEMP_NEEDLE_LENGTH
        )
    def _GetRpmNeedle(self):
        return self._GetNeedle(
            Const.RPM_MIN, 
            Const.RPM_NEEDLE_MIN_ANGLE, 
            Const.RPM_MAX, 
            Const.RPM_NEEDLE_MAX_ANGLE, 
            self._rpm, 
            Const.RPM_NEEDLE_POS, 
            Const.RPM_NEEDLE_LENGTH
        )



        





    