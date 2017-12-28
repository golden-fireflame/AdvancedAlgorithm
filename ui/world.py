class World:
    rectangles = []
    lines = []
    circles = []
    points = []
    start = None
    goal = None

    def __init__(self):
        pass

    def add_shape(self, shape):
        if isinstance(shape, Rectangle):
            self.rectangles.append(shape)
            print("rectangle added")
        elif isinstance(shape, Line):
            self.lines.append(shape)
        elif isinstance(shape, Circle): 
             self.circles.append(shape)
        elif isinstance(shape, Point):
            self.points.append(shape)
            #print("point added")

    def add_start(self, start):
        self.start = Point(start[0], start[1],"start") # those strings are used to distinguish start and end points with different colours

    def add_goal(self, goal):
        self.goal = Point(goal[0], goal[1],"end")


class Shape:

    def __init__(self):
        pass

    def draw(self):
        pass


class Point(Shape):

    def __init__(self, x, y,start_or_end):
        self.x = x
        self.y = y
        self.start_or_end=start_or_end

    def draw(self, w):
        if self.start_or_end=="start": #if start point , color it with red otherwise with blue
            w.create_oval(self.x, self.y, self.x+10, self.y+10, fill="red")
        else:
            w.create_oval(self.x, self.y, self.x+10, self.y+10, fill="blue") 


class Line(Shape):

    def __init__(self, x, y, x2, y2):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

    def draw(self, w):
        w.create_line(self.x, self.y, self.x2, self.y2, fill="blue")


class Circle(Shape):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, w):
        w.create_oval(self.x, self.y, self.width, self.height, fill="green")


class Rectangle(Shape):

    def __init__(self, x, y, x2, y2):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

    def draw(self, w):
        w.create_rectangle(self.x, self.y, self.x2, self.y2, fill="red")
