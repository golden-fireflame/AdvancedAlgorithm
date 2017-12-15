from Tkinter import *

from ui.world import *


class Map:

    def __init__(self, world):
        self.world = world

    def draw(self):

        self.root = Tk()
        self.root.title("A* pathfinding")

        self.w = Canvas(self.root, width=500, height=500)
        self.w.pack()

        self.draw_shapes()

        button = Button(self.root, text='Add line', width=25, command=self.add_line_popup)
        button.pack(side=RIGHT)

        button2 = Button(self.root, text='Add rectangle', width=25, command=self.add_rectangle_popup)
        button2.pack(side=RIGHT)

        button3 = Button(self.root, text='Add circle', width=25, command=self.add_circle_popup)
        button3.pack(side=RIGHT)

        self.root.mainloop()

    def draw_shapes(self):
        for l in self.world.lines:
            l.draw(self.w)

        for c in self.world.circles:
            c.draw(self.w)

        for r in self.world.rectangles:
            r.draw(self.w)

    def add_line_popup(self):
        print ('IMPLEMENT ADD LINE HERE!!!!')

    def add_rectangle_popup(self):
        self.world.add_shape(Rectangle(50, 50, 500, 500))
        self.draw()
        print ('IMPLEMENT ADD RECTANGLE HERE!!!!')

    def add_circle_popup(self):
        print ('IMPLEMENT ADD CIRCLE HERE!!!!')
