from enum import Enum
from itertools import count
from turtle import circle
from Shapes import *

class DashState(Enum):
    DEFAULT = 0
    LEFT_VIEW = 1
    RIGHT_VIEW = 2
    REAR_VIEW = 3

class DisplayStateMachine():
    def __init__(self):
        self._state = DashState.DEFAULT
        self._defaultDrawList = self._DefualtContents()
        self._leftDrawList = self._LeftViewContents()
        self._rightDrawList = self._RightViewContents()
        self._rearDrawList = self._RearViewContents()
        self._leftIndicator = False
        self._rightIndicator = False
        self._speed = 0


    def SetState(self, state):
        _state = DashState(state)

    def GetDrawList(self):
        output = None;

        # Major layout objects that need to be drawn
        if self._state == DashState.DEFAULT:
            output = self._defaultDrawList
        else:
            raise Exception("The desired state does not exist (line 33 DisplayManager.py)")

        # Time/Dynamic dependent objects
        


        return output

    def _DefualtContents(self):
        return [
            Image(0,   0, directory = "images/test.png"), 
            #Image(400, 0, directory = "images/test.gif"),
            #Image(0, 0, directory = "images/dash.png"),
            Rectangle(50, 50, 0, 0),
            Triangle(100, 0, 100, 50, 150, 25),
            Oval(50, 50, 175, 0),
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
        self._leftIndicator = True;
        self._rightIndicator = False;
    
    def TurnOffIndicators(self):
        self._leftIndicator = False
        self._rightIndicator = False
    
    def SetSpeed(self, speed):
        self._speed = speed

    