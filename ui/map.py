from Tkinter import *

from ui.world import *


class Map:

    def __init__(self, world):
        self.world = world

    def draw(self):
        root = Tk()
        root.title("A* pathfinding")

        # create frame to put control buttons onto
        frame = Frame(root, bg='grey', width=400, height=40)
        frame.pack(fill='x')

        button1 = Button(frame, text='Add line', width=25, command=self.add_line_popup)
        button1.pack(side=RIGHT)

        button2 = Button(frame, text='Add rectangle', width=25, command=self.add_rectangle_popup)
        button2.pack(side=RIGHT)

        button3 = Button(frame, text='Add circle', width=25, command=self.add_circle_popup)
        button3.pack(side=RIGHT)
        # set canvas properties
        width = 400
        height = 400
        # invoke canvas
        self.c = Canvas(root, width=width, height=height, bg='white')
        self.draw_shapes()
        self.c.pack()

        root.mainloop()

    def draw_shapes(self):
        for l in self.world.lines:
            l.draw(self.c)

        for c in self.world.circles:
            c.draw(self.c)

        for r in self.world.rectangles:
            r.draw(self.c)

    def add_line_popup(self):
        print ('IMPLEMENT ADD LINE HERE!!!!')

    def add_rectangle_popup(self):
        self.world.add_shape(Rectangle(150, 150, 200, 200))
        self.draw_shapes()
        print ('IMPLEMENT ADD RECTANGLE HERE!!!!')

    def add_circle_popup(self):
        print ('IMPLEMENT ADD CIRCLE HERE!!!!')
