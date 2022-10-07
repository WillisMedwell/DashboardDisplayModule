from tkinter import *
import tkinter 


class Shape():
    # Constructor for Shape
    def __init__(self, width=50, height=50, x=None, y=None, color="black"):
        """
        Creates a generic 'shape' which contains properties common to all
        shapes such as height, width, x y coordinates and colour.
        Args:
            width (int): The width of the shape. Defaults to 50.
            height (int): The height of the shape. Defaults to 50.
            x (int): The x position of the shape. If None, the x position will be the middle of the screen. Defaults to None.
            y (int): The y position of the shape. If None, the y position will be the middle of the screen. Defaults to None.
            color (string): The color of the shape. Defaults to "black"
        """
        # Set some attributes
        self.height = height
        self.width = width
        self.color = color
        # put shape in (0,0) if no constructor
        if x is not None: self.x = x
        else: self.x = 0
        if y is not None: self.y = y
        else: self.y = 0
            
    # This is an internal method not meant to be called by users
    # (It has a _ before the method name to show this)
    def _location(self):
        """
        Internal method used by the class to get the location
        of the shape. This shouldn't be called by users, hence why its
        name begins with an underscore.
        """
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y + self.height
        return [x1, y1, x2, y2]

    # Getters and setters for Shape attributes
    def set_width(self, width):
        """
        Sets the width of the shape.

        Args:
            width (int): The width of the shape
        """
        self.width = width

    def set_height(self,height):
        """
        Sets the height of the shape.
        
        Args:
            height (int): The height of the shape.
        """
        self.height = height

    def set_x(self, x):
        """
        Sets the x position of the shape
        
        Args:
            x (int): The x position for the shape.
        """
        self.x = x

    def set_y(self, y):
        """
        Sets the y position of the shape
        
        Args:
            y (int): The y position for the shape.
        """
        self.y = y

    def set_color(self, color):
        """
        Sets the colour of the shape
        
        Args:
            color (string): The color of the shape.
        """
        self.color = color

    def get_color(self):
        """
        Returns the colour of the shape
        
        Returns:
            color (string): The color of the shape
        """
        return self.color

    def draw(self, canvas):
        pass

class Rectangle(Shape):
    def draw(self, tkwindow):
        """
        Draws a rectangle on the canvas. The properties of the rectangle
        can be set using the getter and setter methods in Shape
        """
        x1, y1, x2, y2 = self._location()
        # Draw the rectangle
        tkwindow.get_canvas().create_rectangle(x1, y1, x2, y2, fill=self.color)

class Oval(Shape):
    def draw(self, tkwindow):
        """
        Draws an oval on the canvas. The properties of the oval
        can be set using the getter and setter methods in Shape
        """
        x1, y1, x2, y2 = self._location()
        # Draw the oval
        tkwindow.get_canvas().create_oval(x1, y1, x2, y2, fill=self.color)

class Triangle(Shape):
    # Every constructor parameter has a default setting
    # e.g. color defaults to "black" but you can override this
    def __init__(self, x1=0, y1=0, x2=20, y2=0, x3=20, y3=20, color="black"):
        """
        Overrides the Shape constructor because triangles require three
        coordinate points to be drawn, unlike rectangles and ovals.

        Args:
            x1 (int): The x position of the coordinate 1. Defaults to 0.
            y1 (int): The y position of the coordinate 1. Defaults to 0.
            x2 (int): The x position of the coordinate 2. Defaults to 20.
            y2 (int): The y position of the coordinate 2. Defaults to 0.
            x3 (int): The x position of the coordinate 3. Defaults to 20.
            y4 (int): The y position of the coordinate 3. Defaults to 20.
            color (string): The color of the shape. Defaults to "black"
        """
        # call the Shape constructor
        super().__init__(color=color)

        # Remove height and width attributes which make no sense for a triangle
        # (triangles are drawn via 3 xy coordinates)
        del self.height
        del self.width

        # Instead add three coordinate attributes
        self.x = x1
        self.y = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def _location(self):
        """
        Internal method used by the class to get the location
        of the triangle. This shouldn't be called by users, hence why its
        name begins with an underscore.
        """
        return [self.x, self.y, self.x2, self.y2, self.x3, self.y3]

    def draw(self, tkwindow):
        """
        Draws a triangle on the canvas. The properties of the triangle
        can be set using the getter and setter methods in Shape
        """
        x1, y1, x2, y2, x3, y3 = self._location()
        # Draw a triangle
        tkwindow.get_canvas().create_polygon(x1, y1, x2, y2, x3, y3, fill=self.color)

    def set_width(self, width):
        """
        Sets the width of the shape.

        Args:
            width (int): The width of the shape
        """
        self.width = width

    def set_height(self,height):
        """
        Sets the height of the shape.
        
        Args:
            height (int): The height of the shape.
        """
        self.height = height

    # Change the behaviour of set_width and set_height methods for a triangle
    # because triangles are not drawn in the same way
    def set_width(self, width):
        """
        Overrides the setter method for width

        Args:
            width (int): The width of the shape
        """
        raise Exception("Width cannot be defined for Triangle objects")

    def set_height(self, height):
        """
        Overrides the setter method for height

        Args:
            height (int): The height of the shape
        """
        raise Exception("Height cannot be defined for Triangle objects")

class Image(Shape):
    _directory = None
    _img = None
    def __init__(self, x=None, y=None, directory =""):
        if directory == "":
            raise Exception("Images need a directory")
        
        self._directory = directory
        self._img = tkinter.PhotoImage(file = self._directory)
        self.x = x
        self.y = y
    
    def draw(self, tkwindow):
        tkwindow.get_canvas().create_image(self.x, self.y, image=self._img, anchor=NW)

