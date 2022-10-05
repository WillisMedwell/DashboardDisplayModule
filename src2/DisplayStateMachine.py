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
    _state = None
    _default_list = None
    _left_view_list = None
    _right_view_list = None
    _rear_view_list = None

    def __init__(self):
        self._state = DashState.DEFAULT
        self._default_list = self._default_contents()
        self._left_view_list = self._left_view_contents()
        self._right_view_list = self._right_view_contents()
        self._right_view_contents = self._rear_view_contents()

    def set_state(self ,state):
        _state = DashState(state)

    def get_shape_list(self):
        if self._state == DashState.DEFAULT:
            return self._default_list
        else:
            raise Exception("The desired state does not exist (line 33 DisplayManager.py)")

    def _default_contents(self):
        return [
            #Image(0,   0, directory = "../images/test.png"), 
            Image(400, 0, directory = "../images/test.gif"),
            Rectangle(50, 50, 0, 0),
            Triangle(100, 0, 100, 50, 150, 25),
            Oval(50, 50, 175, 0),
        ]

    def _left_view_contents(self):
        return []
    
    def _right_view_contents(self):
        return []

    def _rear_view_contents(self):
        return []
