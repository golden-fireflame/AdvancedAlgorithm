class World:
    rectangles = []
    lines = []
    circles = []

    def __init__(self):
        pass

    def add_shape(self, shape):
        if isinstance(shape, Rectangle):
            self.rectangles.append(shape)
        elif isinstance(shape, Line):
            self.lines.append(shape)
        elif isinstance(shape, Circle):
            self.lines.append(shape)


class Shape:

    def __init__(self):
        pass

    def draw(self):
        pass


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

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, w):
        w.create_rectangle(self.x, self.y, self.width, self.height, fill="red")
