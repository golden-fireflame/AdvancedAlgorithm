from Tkinter import *

from ui.world import *


class PopUp:

    def submit_popup(self):
        print("submit")
        x = self.e1.get()
        y = self.e2.get()
        x2 = self.e3.get()
        y2 = self.e4.get()
        if self.shape == 'Rectangle':
            self.world_map.world.add_shape(Rectangle(x, y, x2, y2))
        elif self.shape == 'Line':
            self.world_map.world.add_shape(Line(x, y, x2, y2))
        elif self.shape == 'Circle':
            self.world_map.world.add_shape(Circle(x, y, x2, y2))
        self.world_map.draw_shapes()
        self.master.destroy()

    def __init__(self, world_map, shape):
        self.shape = shape
        self.world_map = world_map
        self.master = Tk()
        self.master.title("Add " + shape)

        label1 = Label(self.master, text="X").grid(row=0)
        label2 = Label(self.master, text="Y").grid(row=1)
        label3 = Label(self.master, text="X2").grid(row=2)
        label4 = Label(self.master, text="Y2").grid(row=3)

        self.e1 = Entry(self.master)
        self.e2 = Entry(self.master)
        self.e3 = Entry(self.master)
        self.e4 = Entry(self.master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)

        close_button = Button(self.master, text='Quit', command=self.master.destroy).grid(row=4, column=0, sticky=W,
                                                                                          pady=4)
        add_button = Button(self.master, text='Add', command=self.submit_popup).grid(row=4, column=1, sticky=W, pady=4)

        self.master.mainloop()


class Map:

    def __init__(self, world):
        self.world = world

    def draw(self):
        root = Tk()
        root.title("A* pathfinding")

        # create frame to put control buttons onto
        frame = Frame(root, bg='grey', width=600, height=40)
        frame.pack(fill='x')

        start_button = Button(frame, text='Start', width=40, command=self.add_circle_popup)
        start_button.pack(side=LEFT, fill=BOTH)

        button1 = Button(frame, text='Add line', width=25, command=self.add_line_popup)
        button1.pack(side=TOP)

        button2 = Button(frame, text='Add rectangle', width=25, command=self.add_rectangle_popup)
        button2.pack(side=TOP)

        button3 = Button(frame, text='Add circle', width=25, command=self.add_circle_popup)
        button3.pack(side=TOP)
        # set canvas properties
        width = 600
        height = 600
        # invoke canvas
        self.c = Canvas(root, width=width, height=height, bg='white')
        self.c.pack()
        self.draw_shapes()

        root.mainloop()

    def draw_shapes(self):
        for l in self.world.lines:
            l.draw(self.c)

        for c in self.world.circles:
            c.draw(self.c)

        for r in self.world.rectangles:
            r.draw(self.c)

    def add_line_popup(self):
        PopUp(self, Line.__name__)

    def add_rectangle_popup(self):
        PopUp(self, Rectangle.__name__)

    def add_circle_popup(self):
        PopUp(self, Circle.__name__)
