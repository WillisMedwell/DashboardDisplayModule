from asyncio import events
from operator import truediv
from pickle import FALSE
import this
import turtle
import pygame;
import sys;

class Constants():
    DEFAULT_BACKGROUND_COLOUR = (77,77,77);

class PygameWindow():
    def __init__(self, width, height, title):
        pygame.init()
        self._window = pygame.display.set_mode((width, height))
        self._window.fill(Constants.DEFAULT_BACKGROUND_COLOUR);
        self._running = True
        pygame.display.flip()
        pygame.display.set_caption(title)
        print("init complete")
        self._keys_typed = []

    def IsRunning(self):
        return self._running
 
    def ProcessEvents(self):
        events = pygame.event.get()
        self._keys_typed = []
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                self._keys_typed.append(event.key)

    def WasKeyTyped(self, key):
        for k in self._keys_typed:
            if k == key:
                return True
        return False

    def Close(self):
        pygame.display.quit()
        pygame.quit()

    def Draw(self, drawList):
        for shape in drawList:
            shape.draw(self)

    def Refresh(self):
        pygame.display.flip();

    def GetSurface(self):
        return self._window