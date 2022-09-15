# This code requires Python 3 and tkinter (which is usually installed by default)
# This code will NOT work on trinket.io as the tkinter module is not supported
# Raspberry Pi Foundation 2020
# CC-BY-SA 4.0
import math
try:
    from tkinter import  Tk, Canvas, BOTH
except ImportError:
    raise Exception("tkinter did not import successfully - check you are running Python 3 and that tkinter is available.")
from tkinter import *
import random
from datetime import datetime



global KM_PH 
print('Enter speed (0 - 160):')
KM_PH = input()
#KM_PH = 175

global RP_M
print('Enter RPM (0 - 8):')
RP_M = input()
#RP_M = 4.5

global OutTemp
print('Enter Temp (0 - 50):')
OutTemp = input()
#OutTemp = 23.5

global Rangekm
print('Enter Range in km (0 - 500):')
Rangekm = input()     #MAX FUEL 500km
#Rangekm = 400


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
        Paper.tk.title("Dashboard")
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
    

    def outline_right_arrow():
        #### Turning arrow whie outline RIGHT
        rect2 = Rectangle(height=22, width=23, x=802, y=58.5, color="white")
        rect2.draw()
        tri = Triangle(x1=855, y1=70, x2= 822, y2 = 49, x3 = 822, y3 =92, color = 'white')
        tri.draw()
    ##BLACK FILL
        rect2 = Rectangle(height=15, width=20, x=805, y=62, color="black")
        rect2.draw()
        tri = Triangle(x1=850, y1=70, x2= 825, y2 = 55, x3 = 825, y3 =85, color = 'black')
        tri.draw()


    

   ###  TURNING RIGHT ARROW 

    def right_arrow():
        rect2 = Rectangle(height=15, width=20, x=805, y=62, color="green2")
        rect2.draw()
        tri = Triangle(x1=850, y1=70, x2= 825, y2 = 55, x3 = 825, y3 =85, color = 'green2')
        tri.draw()

    
         
    
    def outline_left_arrow():
        ##Tunring arrow white outline   LEFT
        rect3 = Rectangle(height=22, width=23, x=340, y=58.5, color="white")
        rect3.draw()
        tri2 = Triangle(x1=310, y1=70, x2= 343, y2 = 49, x3 = 343, y3 =92, color = 'white')
        tri2.draw()
        ##black outline
        rect3 = Rectangle(height=15, width=20, x=339, y=62, color="black")
        rect3.draw()
        tri2 = Triangle(x1=315, y1=70, x2= 340, y2 = 55, x3 = 340, y3 =85, color = 'black')
        tri2.draw()

   

    def left_arrow():
        ##Tunring arrow LEFT
        rect3 = Rectangle(height=15, width=20, x=339, y=62, color="green2")
        rect3.draw()
        tri2 = Triangle(x1=315, y1=70, x2= 340, y2 = 55, x3 = 340, y3 =85, color = 'green2')
        tri2.draw()
    
    #left_arrow()
    #right_arrow()
         ### conditional statement RIGHT ARROW
    def motion(event):
        x, y = event.x, event.y
        print('{}, {}'.format(x, y))

        ### RIGHT ARROW CONDITION
        if  (806 < x < 846)  & (62 < y < 77):
            right_arrow()

        else:
            outline_right_arrow()

        ### LEFT ARROW CONDITION
        if (316 < x < 358) & (65 < y < 77):
            left_arrow()
        else:
            outline_left_arrow()

        
             
    Paper.tk.bind('<Motion>', motion)

   # RPM right ring
   #Right ring shade
    oval = Oval()
    oval.set_height(310)
    oval.set_width(310)
    oval.set_color("light blue")
    oval.set_x(795)
    oval.set_y(41.5)
    oval.draw()
   #right ring base
    oval = Oval()
    oval.set_height(300)
    oval.set_width(300)
    oval.set_color("cyan2")
    oval.set_x(800)
    oval.set_y(50)
    oval.draw()
       ##inner black ring of right ring
    oval4 = Oval()
    oval4.set_height(285)
    oval4.set_width(285)
    oval4.set_color("dark slate gray")
    oval4.set_x(807.5)
    oval4.set_y(57.5)
    oval4.draw()
    ###second colour ring on right
    oval5 = Oval()
    oval5.set_height(165)
    oval5.set_width(165)
    oval5.set_color("grey20")
    oval5.set_x(865)
    oval5.set_y(120)
    oval5.draw()
    ## black layer 2nd inner circle
    oval6 = Oval()
    oval6.set_height(150)
    oval6.set_width(150)
    oval6.set_color("grey10")
    oval6.set_x(872)
    oval6.set_y(127.5)
    oval6.draw()
    ###END OF RIGHT RING



    # KM/H left ring
    #Right ring shade
    oval = Oval()
    oval.set_height(310)
    oval.set_width(310)
    oval.set_color("light salmon")
    oval.set_x(45)
    oval.set_y(41.5)
    oval.draw()
    #base left ring
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
    
    Numb1 = Paper.tk.canvas.create_text(115,275,fill='OliveDrab1',font='Robinson 22 bold', text='0')
    Numb2 = Paper.tk.canvas.create_text(90,225,fill='OliveDrab1',font='Robinson 22 bold', text='20')
    Numb3 = Paper.tk.canvas.create_text(95,160,fill='OliveDrab1',font='Robinson 22 bold', text='40')
    Numb4 = Paper.tk.canvas.create_text(130,105,fill='OliveDrab1',font='Robinson 22 bold', text='60')
    Numb5 = Paper.tk.canvas.create_text(195,85,fill='OliveDrab1',font='Robinson 22 bold', text='80')
    Numb6 = Paper.tk.canvas.create_text(265.5,108,fill='OliveDrab1',font='Robinson 22 bold', text='100')
    Numb7 = Paper.tk.canvas.create_text(300,160,fill='OliveDrab1',font='Robinson 22 bold', text='120')
    Numb8 = Paper.tk.canvas.create_text(310,225,fill='OliveDrab1',font='Robinson 22 bold', text='140')
    Numb9 = Paper.tk.canvas.create_text(280,275,fill='OliveDrab1',font='Robinson 22 bold', text='160')

    ## RPM NUMBERS
    RPM1 = Paper.tk.canvas.create_text(865,275,fill='OliveDrab1',font='Robinson 22 bold', text='0')
    RPM2 = Paper.tk.canvas.create_text(840,225,fill='OliveDrab1',font='Robinson 22 bold', text='1')
    RPM3 = Paper.tk.canvas.create_text(845,160,fill='OliveDrab1',font='Robinson 22 bold', text='2')
    RPM4 = Paper.tk.canvas.create_text(885,105,fill='OliveDrab1',font='Robinson 22 bold', text='3')
    RPM5 = Paper.tk.canvas.create_text(950,85,fill='OliveDrab1',font='Robinson 22 bold', text='4')
    RPM6 = Paper.tk.canvas.create_text(1020,105,fill='OliveDrab1',font='Robinson 22 bold', text='5')
    RPM7 = Paper.tk.canvas.create_text(1060,160,fill='OliveDrab1',font='Robinson 22 bold', text='6')
    RPM8 = Paper.tk.canvas.create_text(1055,225,fill='OliveDrab1',font='Robinson 22 bold', text='7')
    RPM9 = Paper.tk.canvas.create_text(1030,275,fill='OliveDrab1',font='Robinson 22 bold', text='8')

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
    tri = Triangle(x1=425, y1=320, x2= 515, y2 = 220, x3 = 425.5, y3 =320, color = 'red')
    tri.draw()
    #tri = Triangle(x1=440, y1=320, x2= 535, y2 = 220, x3 = 440.5, y3 =320, color = 'red')
  #  tri.draw()
    ## road dotted line
    #rect3 = Rectangle(height=30, width=8, x=600, y=280, color="grey70")
    #rect3.draw()
    #rect3 = Rectangle(height=25, width=6, x=600, y=230, color="grey60")
   # rect3.draw()
   # tri = Triangle(x1=600, y1=210, x2= 607, y2 = 210, x3 = 603.5, y3 =195, color = 'grey50')
   # tri.draw()


    ###Right streak details
    #rect1 = Rectangle(height=120, width=120, x=575, y=200, color="turquoise3")
    #rect1.draw()
    tri = Triangle(x1=700, y1=320, x2= 600, y2 = 180, x3 = 699, y3 =320, color = 'turquoise1')
    tri.draw()
    tri = Triangle(x1=720, y1=320, x2= 630, y2 = 200, x3 = 720.5, y3 =320, color = 'turquoise1')
    tri.draw()
    tri = Triangle(x1=770, y1=320, x2= 705, y2 = 240, x3 = 770.5, y3 =320, color = 'turquoise3')
    tri.draw()
   # tri = Triangle(x1=695, y1=200, x2= 695, y2 = 320, x3 = 795, y3 = 320, color = 'turquoise3')
   # tri.draw()
    #econd=Paper.tk.canvas.create_line(780,320,670,200,fill='white',width=2) # draw the needle
    tri = Triangle(x1=790, y1=320, x2= 675, y2 = 180, x3 = 790.5, y3 =320, color = 'turquoise3')
    tri.draw()

    ### KMH DIGITAL
    KMH = Paper.tk.canvas.create_text(645,195,fill='OliveDrab1',font='Robinson 16', text='KMH')
    KM_PHstr = str(KM_PH)
    KMH = Paper.tk.canvas.create_text(570,180,fill='OliveDrab1',font='Robinson 44 bold', text= KM_PHstr)

    ### RPM DIGITAL Right ring
    RPMDIG = KMH = Paper.tk.canvas.create_text(950,250,fill='OliveDrab1',font='Robinson 12', text='x1000/min')

    ### SPORT LOGO
    Sport = Paper.tk.canvas.create_text(885,365,fill='red',font='Robinson 16 bold', text='SPORT')

### Gear of car (Drive example)
    Gear = Paper.tk.canvas.create_text(385,80,fill='white',font='Robinson 30 bold', text='D')

    ## RANGE JUICE GREEN SLAB
    Rangekm = str(Rangekm)
    Rangekm = int(Rangekm)
    Range = Paper.tk.canvas.create_text(580,340,fill='white',font='Robinson 12 bold ', text='Range           km')
    Range = Paper.tk.canvas.create_text(595,340,fill='white',font='Robinson 12 bold', text= Rangekm)
    ##circular round off
    oval12 = Oval()
    oval12.set_height(25)
    oval12.set_width(25)
    oval12.set_color("lawn green")
    oval12.set_x(362.5)
    oval12.set_y(355)
    oval12.draw()
    rect3 = Rectangle(height=25, width=10, x=380, y=355, color="black")
    rect3.draw()
    ##long green box
    rect3 = Rectangle(height=25, width=400*(Rangekm/500), x=380, y=355, color="lawn green")
    rect3.draw()
    ## reserve fuel
    rect3 = Rectangle(height=25, width=3, x=378, y=355, color="black")
    rect3.draw()
    #LOW PETROL
    rect3 = Rectangle(height=25, width=3, x=480, y=355, color="black")
    rect3.draw()
    #MEIDUM
    rect3 = Rectangle(height=25, width=3, x=580, y=355, color="black")
    rect3.draw()
    #HIGH
    rect3 = Rectangle(height=25, width=3, x=680, y=355, color="black")
    rect3.draw()
    if (Rangekm < 25) :
         Reserve_warning = Paper.tk.canvas.create_text(450,367.5,fill='red',font='Robinson 12 bold ', text='Reserve Fuel')
    
  ## End of Range module




    ##KMH in left ring
    KMHLR = Paper.tk.canvas.create_text(200,260,fill='OliveDrab1',font='Robinson 16 ', text='KMH')

    
    ### Temperature outside
    OutTemp = str(OutTemp)
    Temp = Paper.tk.canvas.create_text(575,80,fill='white',font='Robinson 16 bold', text=OutTemp)
    Temp = Paper.tk.canvas.create_text(615,80,fill='white',font='Robinson 16 bold', text = "c")
    ## celcius symbol
    oval9 = Oval()
    oval9.set_height(10)
    oval9.set_width(10)
    oval9.set_color("white")
    oval9.set_x(595)
    oval9.set_y(68)
    oval9.draw()

    oval10 = Oval()
    oval10.set_height(4)
    oval10.set_width(4)
    oval10.set_color("black")
    oval10.set_x(598)
    oval10.set_y(71)
    oval10.draw()
    ### END TEMP


    ### Real time
    now = datetime.now()

    current_time = now.strftime("%H:%M")
    Time = Paper.tk.canvas.create_text(740,80,fill='white',font='Robinson 16 bold', text=current_time)
    ### END TIME


    ### KMH NEEDLE
    oval11 = Oval()
    oval11.set_height(30)
    oval11.set_width(30)
    oval11.set_color("grey")
    oval11.set_x(180)
    oval11.set_y(176.5)
    oval11.draw()
    KM_PH = int(KM_PH)
    Angular_shift = ((KM_PH)-80) * 1.8
    xbegin = 195
    ybegin = 191.5
    in_radian = math.radians(Angular_shift)
    xend = xbegin + 120*math.sin(in_radian)
    yend = ybegin - 120*math.cos(in_radian)
    second=Paper.tk.canvas.create_line(xbegin,ybegin,xend,yend,fill='tomato',width=5) # draw the needle
    ## END OF LEFT HAND NEEDLE

    ### RPM NEEDLE RIGHT HAND
    oval12 = Oval()
    oval12.set_height(30)
    oval12.set_width(30)
    oval12.set_color("grey")
    oval12.set_x(935)
    oval12.set_y(185)
    oval12.draw()
    RP_M = float(RP_M)
    Angular_shift2 = ((RP_M)-4) * 36
    xbegin2 = 950
    ybegin2 = 200
    in_radian2 = math.radians(Angular_shift2)
    xend2 = xbegin2 + 120*math.sin(in_radian2)
    yend2 = ybegin2 - 120*math.cos(in_radian2)
    second=Paper.tk.canvas.create_line(xbegin2,ybegin2,xend2,yend2,fill='firebrick1',width=5) # draw the needle



    


    
  

    my_drawing.display()


