from math import sqrt


class World:
    def __init__(self):
        self.rectangles = []
        self.lines = []
        self.circles = []
        self.points = []
        self.start = None
        self.goal = None
        # create map:   0->accessible(False)  1->blocked 2->sea 3->swamp(True)
        self.map = {}
        for i in range(600):
            for j in range(600):
                self.map[(i, j)] = 0  # all coordinates set 0

    def update_map(self, shape, area):
        # function called to update map, area->text
        # shape = Shape(), area = 'Obstacle'
        if area == 'Obstacle':
            area = 1
        elif area == 'Sea':
            area = 2
        elif area == 'Swamp':
            area = 3

        if isinstance(shape, Rectangle):
            for i in range(shape.x, shape.x2+1):  # +1 needed
                for j in range(shape.y, shape.y2+1):
                    self.map[i, j] = area
        elif isinstance(shape, Circle):
            center = (shape.x_center, shape.y_center)
            radius = shape.radius
            for i in range(shape.x, shape.x2+1):
                for j in range(shape.y, shape.y2+1):
                    if sqrt((i - center[0]) ** 2 + (j - center[1]) ** 2) <= radius:  # check if in the circle
                        self.map[i, j] = area
        return

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
        self.start = Point(start[0], start[1], "start")  # those strings are used to distinguish start and end points with different colours

    def add_goal(self, goal):
        self.goal = Point(goal[0], goal[1], "end")

    def is_allowed(self, x, y):
        """old method"""
        # for circle in self.circles:
        #     if circle.is_within(x, y):
        #         return False
        # for rectangle in self.rectangles:
        #     if rectangle.is_within(x, y):
        #         return False
        # return True
        """new method: use map"""
        return self.map[x, y]


class Shape:
    def __init__(self):
        pass

    def draw(self, w):
        pass

    @staticmethod
    def distance(x1, x2, y1, y2):
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Point(Shape):
    def __init__(self, x, y,start_or_end):
        Shape.__init__(self)
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
        Shape.__init__(self)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

    def draw(self, w):
        w.create_line(self.x, self.y, self.x2, self.y2, fill="blue")

    #def is_within(self, x_point, y_point):
    #    return abs(
    #        self.distance(x_point, self.x, y_point, self.y) +
    #        self.distance(x_point, self.x2, y_point, self.y2) -
    #        self.distance(self.x, self.x2, self.y, self.y2)
    #    ) < 0.2;


class Circle(Shape):
    def __init__(self, x, y, x2, y2):
        Shape.__init__(self)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

        self.x_center = (x + x2) / 2
        self.y_center = (y + y2) / 2
        self.radius = self.x_center - x

    def draw(self, w):
        w.create_oval(self.x, self.y, self.x2, self.y2, fill="green")

    def is_within(self, x_point, y_point):
        return self.distance(x_point,  self.x_center,y_point, self.y_center) <= self.radius


class Rectangle(Shape):
    def __init__(self, x, y, x2, y2):
        Shape.__init__(self)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

    def draw(self, w):
        w.create_rectangle(self.x, self.y, self.x2, self.y2, fill="red")

    def is_within(self, x_point, y_point):
        return self.x <= x_point <= self.x2 and self.y <= y_point <= self.y2
