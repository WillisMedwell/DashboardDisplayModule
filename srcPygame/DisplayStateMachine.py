from asyncio import constants
from enum import Enum
from itertools import count
import math
from msilib.schema import Font

from cv2 import circle
from DrawList import DrawList
from CameraThread import CameraThread
from Shapes import Shape, Oval, Image, Line, Text
import pygame, sys, os


class DashState(Enum):
    DEFAULT = 0
    LEFT_VIEW = 1
    RIGHT_VIEW = 2
    REAR_VIEW = 3


class DisplayStateMachine():
    def __init__(self):
        # set initial state
        self._state = DashState.DEFAULT
        DEFAULT_BACKGROUND_COLOUR = (0,0,0);
        
        self._font_test = pygame.font.SysFont('Corbel', 35)
        # load group image lists
        self._rightIndicator   = False
        self._leftIndicator    = False
        self._engineWarning    = False
        self._handbrakeWarning = False 
        self._speed = 0
        self._fuel  = 0
        self._temp  = 0
        self._rpm   = 0
        self._drawlist = DrawList()
        # load individual dynamic images 

    def SetState(self, state):
        self._state = DashState(state)


    def GetDrawList(self):
        self._drawlist.Clear()


        # Major layout objects that need to be drawn
        if self._state == DashState.DEFAULT:
            self._drawlist.SetToDefault(self._speed, self._rpm, self._fuel, self._temp)
        elif self._state == DashState.LEFT_VIEW:
            self._drawlist.SetToLeftView(self._speed, self._rpm, self._fuel, self._temp)
        elif self._state == DashState.RIGHT_VIEW:
            self._drawlist.SetToRightView(self._speed, self._rpm, self._fuel, self._temp)
        elif self._state == DashState.REAR_VIEW:
            self._drawlist.SetToRearView()
        else:
            raise Exception("The desired state does not exist (line 114 DisplayManager.py)")
        return self._drawlist._shapes


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



