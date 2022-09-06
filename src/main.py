# This code requires Python 3 and tkinter (which is usually installed by default)
# This code will NOT work on trinket.io as the tkinter module is not supported
# Raspberry Pi Foundation 2020
# CC-BY-SA 4.0

try:
    from tkinter import Tk, Canvas, BOTH
except ImportError:
    raise Exception("tkinter did not import successfully - check you are running Python 3 and that tkinter is available.")

import random


class Paper():
    
    # the tk object which will be used by the shapes
    tk = None

    def __init__(self, width=1200, height=400):
        """
        Create a Paper object which is required to draw shapes onto.

        It is only possible to create 1 Paper object.

        Args:
            width (int): The width of the display. Defaults to 600.
            height (int): The height of the display. Defaults to 600.

        Returns:
            Paper: A Paper object
        """

        if Paper.tk is not None:
            raise Exception("Error: Paper has already been created, there can be only one.")

        try:
            Paper.tk = Tk()
        except ValueError:
            raise Exception("Error: could not instantiate tkinter object")

        # Set some attributes
        Paper.tk.title("Drawing shapes")
        Paper.tk.geometry(str(width)+"x"+str(height))
        Paper.tk.paper_width = width
        Paper.tk.paper_height = height

        # Create a tkinter canvas object to draw on
        Paper.tk.canvas = Canvas(Paper.tk)
        Paper.tk.canvas.pack(fill=BOTH, expand=1)
       ## Paper.tk.canvas.create_text(500,50,fill='white',font='Times 22 bold', text='Welcome')
    def display(self):
        """
        Displays the paper
        """
        Paper.tk.mainloop()

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
        if Paper.tk is None:
            raise Exception("A Paper object has not been created. There is nothing to draw on.")

        # Set some attributes
        self.height = height
        self.width = width
        self.color = color

        # Put the shape in the centre if no xy coords were given
        if x is None:
            self.x = (Paper.tk.paper_width/2) - (self.width/2)
        else:
            self.x = x
        if y is None:
            self.y = (Paper.tk.paper_height/2) - (self.height/2)
        else:
            self.y = y

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

    # Randomly generate what the shape looks like
    def randomize(self, smallest=20, largest=200):
        """
        Randomly generates width, height, position and colour for a shape. You can specify
        the smallest and largest random size that will be generated. If not specified, the
        generated shape will default to a random size between 20 and 200.

        Args:
            smallest (int): The smallest the shape can be. Defaults to 20
            largest (int): The largest the the shape can be. Defaults to 200.

        """
        self.width = random.randint(smallest, largest)
        self.height = random.randint(smallest, largest)

        self.x = random.randint(0, Paper.tk.paper_width-self.width)
        self.y = random.randint(0, Paper.tk.paper_height-self.height)

        self.color = random.choice(["red", "yellow", "blue", "green", "gray", "white", "black", "cyan", "pink", "purple"])

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


# Rectangle class is a subclass of Shape
class Rectangle(Shape):

    # This is how to draw a rectangle
    def draw(self):
        """
        Draws a rectangle on the canvas. The properties of the rectangle
        can be set using the getter and setter methods in Shape
        """
        x1, y1, x2, y2 = self._location()

        # Draw the rectangle
        Paper.tk.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)


class Oval(Shape):

    def draw(self):
        """
        Draws an oval on the canvas. The properties of the oval
        can be set using the getter and setter methods in Shape
        """
        x1, y1, x2, y2 = self._location()

        # Draw the oval
        Paper.tk.canvas.create_oval(x1, y1, x2, y2, fill=self.color)


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

    def draw(self):
        """
        Draws a triangle on the canvas. The properties of the triangle
        can be set using the getter and setter methods in Shape
        """
        x1, y1, x2, y2, x3, y3 = self._location()
        # Draw a triangle
        Paper.tk.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=self.color)

    def randomize(self):
        """
        Randomly chooses the location of all 3 triangle points as well
        as the colour of the triangle
        """
        # Randomly choose all the points of the triangle
        self.x = random.randint(0, Paper.tk.paper_width)
        self.y = random.randint(0, Paper.tk.paper_height)
        self.x2 = random.randint(0, Paper.tk.paper_width)
        self.y2 = random.randint(0, Paper.tk.paper_height)
        self.x3 = random.randint(0, Paper.tk.paper_width)
        self.y3 = random.randint(0, Paper.tk.paper_height)

        # Randomly choose a colour of this triangle
        self.color = random.choice(["red", "yellow", "blue", "green", "gray", "white", "black", "cyan", "pink", "purple"])

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


# This if statement means
# "if you run this file (rather than importing it), run this demo script"
if __name__ == "__main__":

    my_drawing = Paper()
    
    # Random size and location triangle
    #tri = Triangle()
   # tri.randomize()
   # tri.draw()
    #
    # BACKGROUND COLOUR
    rect = Rectangle(height=400, width=1200, x=0, y=0, color="black")
    rect.draw()

    #WHITE LINE MIDDLE UPPER INBETWEEN TWO RINGS
    rect1 = Rectangle(height=1.5, width=400, x=370, y=100, color="white")
    rect1.draw()


    ###Turning arrow RIGHT
    rect2 = Rectangle(height=15, width=20, x=805, y=62, color="green2")
    rect2.draw()
    tri = Triangle(x1=850, y1=70, x2= 825, y2 = 55, x3 = 825, y3 =85, color = 'green2')
    tri.draw()

    ##Tunring arrow LEFT
    rect3 = Rectangle(height=15, width=20, x=339, y=62, color="green2")
    rect3.draw()
    tri2 = Triangle(x1=315, y1=70, x2= 340, y2 = 55, x3 = 340, y3 =85, color = 'green2')
    tri2.draw()
   
   # RPM right ring
    oval = Oval()
    oval.set_height(300)
    oval.set_width(300)
    oval.set_color("orange red")
    oval.set_x(800)
    oval.set_y(50)
    oval.draw()
       ##inner black ring of right ring
    oval4 = Oval()
    oval4.set_height(285)
    oval4.set_width(285)
    oval4.set_color("grey10")
    oval4.set_x(807.5)
    oval4.set_y(57.5)
    oval4.draw()
    ###second colour ring on right
    oval5 = Oval()
    oval5.set_height(165)
    oval5.set_width(165)
    oval5.set_color("orange red")
    oval5.set_x(865)
    oval5.set_y(120)
    oval5.draw()
    ## black layer 2nd inner circle
    oval6 = Oval()
    oval6.set_height(150)
    oval6.set_width(150)
    oval6.set_color("grey9")
    oval6.set_x(872)
    oval6.set_y(127.5)
    oval6.draw()
    ###END OF RIGHT RING


    # KM/H left ring
    oval2 = Oval()
    oval2.set_height(300)
    oval2.set_width(300)
    oval2.set_color("orange red")
    oval2.set_x(50)
    oval2.set_y(50)
    oval2.draw()
   ##inner black ring of left ring
    oval3 = Oval()
    oval3.set_height(285)
    oval3.set_width(285)
    oval3.set_color("grey10")
    oval3.set_x(57.5)
    oval3.set_y(57.5)
    oval3.draw()
     ###second colour ring on left
    oval7 = Oval()
    oval7.set_height(165)
    oval7.set_width(165)
    oval7.set_color("orange red")
    oval7.set_x(115)
    oval7.set_y(120)
    oval7.draw()
    ## black layer 2nd inner circle
    oval8 = Oval()
    oval8.set_height(150)
    oval8.set_width(150)
    oval8.set_color("grey9")
    oval8.set_x(122)
    oval8.set_y(127.5)
    oval8.draw()
    ### end of KM/H ring
   

    ##KM/H numbers
    
    Numb1 = Paper.tk.canvas.create_text(110,275,fill='white',font='Robinson 22 bold', text='0')
    Numb2 = Paper.tk.canvas.create_text(90,225,fill='white',font='Robinson 22 bold', text='20')
    Numb3 = Paper.tk.canvas.create_text(95,160,fill='white',font='Robinson 22 bold', text='40')
    Numb4 = Paper.tk.canvas.create_text(130,105,fill='white',font='Robinson 22 bold', text='60')
    Numb5 = Paper.tk.canvas.create_text(200,85,fill='white',font='Robinson 22 bold', text='80')
    Numb6 = Paper.tk.canvas.create_text(260,105,fill='white',font='Robinson 22 bold', text='100')
    Numb7 = Paper.tk.canvas.create_text(300,160,fill='white',font='Robinson 22 bold', text='120')
    Numb8 = Paper.tk.canvas.create_text(310,225,fill='white',font='Robinson 22 bold', text='140')
    Numb9 = Paper.tk.canvas.create_text(280,275,fill='white',font='Robinson 22 bold', text='160')

      ### WHITE LINE BOTTOM between 2 rings
    rect1 = Rectangle(height=1.5, width=430, x=365, y=320, color="white")
    rect1.draw()
    ## left streak details
    tri = Triangle(x1=367, y1=320, x2= 500, y2 = 180, x3 = 367.5, y3 =320, color = 'orange red')
    tri.draw()
    tri = Triangle(x1=380, y1=320, x2= 513, y2 = 180, x3 = 381, y3 =320, color = 'red')
    tri.draw()
    tri = Triangle(x1=410, y1=320, x2= 538, y2 = 180, x3 = 410.5, y3 =320, color = 'orange red')
    tri.draw()
    ##middle stripe
    tri = Triangle(x1=525, y1=320, x2= 600, y2 = 200, x3 = 525.5, y3 =320, color = 'red')
    tri.draw()
    ###Right streak details
    tri = Triangle(x1=700, y1=320, x2= 600, y2 = 180, x3 = 699, y3 =320, color = 'orange red')
    tri.draw()
    tri = Triangle(x1=720, y1=320, x2= 620, y2 = 200, x3 = 720.5, y3 =320, color = 'orange red')
    tri.draw()
    tri = Triangle(x1=793, y1=320, x2= 680, y2 = 185, x3 = 793.5, y3 =320, color = 'red')
    tri.draw()


    ### KMH DIGITAL
    KMH = Paper.tk.canvas.create_text(640,230,fill='grey',font='Robinson 16', text='KMH')
    KMH = Paper.tk.canvas.create_text(570,220,fill='white',font='Robinson 40 bold', text='153')

    ### SPORT LOGO
    Sport = Paper.tk.canvas.create_text(890,365,fill='red',font='Robinson 16 bold', text='SPORT')

### Gear of car (Drive example)
    Gear = Paper.tk.canvas.create_text(385,80,fill='white',font='Robinson 30 bold', text='D')

    ## RANGE
    Range = Paper.tk.canvas.create_text(130,365,fill='white',font='Robinson 12 ', text='Range    300 km')

    ##KMH in left ring
    KMHLR = Paper.tk.canvas.create_text(200,250,fill='grey',font='Robinson 16 ', text='KMH')

  
    my_drawing.display()
