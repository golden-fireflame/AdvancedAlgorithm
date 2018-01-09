from Tkinter import *
import tkMessageBox
import tkFont as tkfont
import ttk
import logging
import uuid
import threading
import time
from time import sleep
from ui.world import World
from ui.world import Shape, Point, Line, Circle, Rectangle
#from astar.algorithm import Astar
from astar.algo2 import Astar


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOG = logging.getLogger()
"""---------------------------------------------------------------------------------------------------------------------
                                          GUI
---------------------------------------------------------------------------------------------------------------------"""
class GUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title('A star algorithm')
        LOG.debug('Application has started!')
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # store UI frames
        self.frames = {}
        for F in (Top, AddShape):
            page_name = F.__name__
            frame = F(master=container, controller=self)  # init page
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Top")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def get_frame(self, page_name):
        return self.frames[page_name]


class Top(Frame):
    def __init__(self, master, controller):
        # init Frame
        Frame.__init__(self, master)
        # self.pack(side="top", fill="both", expand=True)
        self.controller = controller

        # create Frames
        self.title_frame = Frame(self)
        self.title_frame.grid(row=0, column=0, columnspan=2)
        self.config_frame = Frame(self)
        self.config_frame.grid(row=1, column=0)
        self.map_frame = Frame(self)
        self.map_frame.grid(row=1, column=1)
        # some variables if needed
        self.world = World()
        self.s = None
        self.e = None
        # head label
        label = Label(self.title_frame, text='A Star Path Finding Algorithm', font=controller.title_font)
        label.pack(fill='x')

        # config panel
        self.execute_button = Button(self.config_frame, text='Play', command=self.startAlgo)
        self.clear_button = Button(self.config_frame, text='Clear', command=self.clearMap)
        self.init_button = Button(self.config_frame, text='Default Map', command=self.initMap)
        self.setStart_button = Button(self.config_frame, text='Start Point', command=self.setStartPoint)
        self.setEnd_button = Button(self.config_frame, text='End Point', command=self.setEndPoint)
        self.addLine_button = Button(self.config_frame, text='Add Line', command=self.addLine)
        self.addRect_button = Button(self.config_frame, text='Add Rectangle', command=self.addRect)
        self.addCircle_button = Button(self.config_frame, text='Add Circle', command=self.addCircle)

        self.execute_button.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        self.clear_button.grid(row=1, column=0, sticky=NSEW)
        self.init_button.grid(row=1, column=1, sticky=NSEW)
        self.setStart_button.grid(row=2, column=0)
        self.setEnd_button.grid(row=2, column=1)
        self.addLine_button.grid(row=3, column=0, columnspan=2, sticky=NSEW)
        self.addRect_button.grid(row=4, column=0, columnspan=2, sticky=NSEW)
        self.addCircle_button.grid(row=5, column=0, columnspan=2, sticky=NSEW)

        # canvas
        self.w = Canvas(self.map_frame, width=1000, height=1000, bg='white')
        self.w.pack()
        self.initMap()

        # bind key to start algo
        self.execute_button.bind('<Return>', self.startAlgo)

    def setStartPoint(self):
        frame = self.controller.get_frame('AddShape')
        frame.prepare('sPoint')
        self.controller.show_frame('AddShape')
        return

    def setEndPoint(self):
        frame = self.controller.get_frame('AddShape')
        frame.prepare('ePoint')
        self.controller.show_frame('AddShape')
        return

    def addLine(self):
        frame = self.controller.get_frame('AddShape')
        frame.prepare('Line')
        self.controller.show_frame('AddShape')
        return

    def addRect(self):
        frame = self.controller.get_frame('AddShape')
        frame.prepare('Rectangle')
        self.controller.show_frame('AddShape')
        return

    def addCircle(self):
        frame = self.controller.get_frame('AddShape')
        frame.prepare('Circle')
        self.controller.show_frame('AddShape')
        return

    def initMap(self):
        # demo
        self.s = self.w.create_oval(750, 200, 760, 210, fill="black")
        sPoint = Point(750, 200, 'start')
        self.world.start = sPoint

        self.e = self.w.create_oval(200, 750, 210, 760, fill="magenta")
        ePoint = Point(200, 750, 'end')
        self.world.goal = ePoint

        self.w.create_rectangle(200, 200, 400, 400, fill="blue")
        rectangle = Rectangle(200, 200, 400, 400)
        self.world.rectangles.append(rectangle)

        self.w.create_line(150, 750, 750, 400, fill="red")
        line = Line(150, 750, 750, 400)
        self.world.lines.append(line)

        self.w.create_oval(750, 750, 800, 800, fill="green")
        circle = Circle(750, 750, 800, 800)
        self.world.circles.append(circle)
        return

    def clearMap(self):
        self.w.delete(ALL)
        return

    def startAlgo(self):
        LOG.debug('Start Path Finding...')
        start = (self.world.start.x, self.world.start.y)
        goal = (self.world.goal.x, self.world.goal.y)

        alg = Astar(self, 1000, 1000, start, goal)
        came_from, cost_so_far = alg.a_star()
        path = alg.build_path(goal, came_from, cost_so_far)

        for p in path:
            self.w.create_oval(p[0], p[1], p[0]+10, p[1]+10, fill='cyan')
        return


class AddShape(Frame):
    def __init__(self, master, controller):
        # init Frame
        Frame.__init__(self, master)
        # self.pack(side="top", fill="both", expand=True)
        self.controller = controller
        # shape & coordinates
        self.frame = None
        self.shape = None
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        # Labels & Entries
        self.label_x1 = Label(self, text='X1')
        self.label_y1 = Label(self, text='Y1')
        self.label_x2 = Label(self, text='X2')
        self.label_y2 = Label(self, text='Y2')

        self.label_x1.grid(row=0, column=0)
        self.label_y1.grid(row=1, column=0)
        self.label_x2.grid(row=2, column=0)
        self.label_y2.grid(row=3, column=0)

        self.entry_x1 = Entry(self)
        self.entry_y1 = Entry(self)
        self.entry_x2 = Entry(self)
        self.entry_y2 = Entry(self)

        self.entry_x1.grid(row=0, column=1)
        self.entry_y1.grid(row=1, column=1)
        self.entry_x2.grid(row=2, column=1)
        self.entry_y2.grid(row=3, column=1)
        # Buttons
        self.submit_button = Button(self, text='Submit', command=self.drawshape)
        self.back_button = Button(self, text='Back', command=self.goBack)

        self.submit_button.grid(row=4, column=0)
        self.back_button.grid(row=4, column=1)

    def drawshape(self, e=None):
        self.frame = self.controller.get_frame('Top')
        w = self.frame.w
        try:
            if self.shape == 'sPoint' or self.shape == 'ePoint':
                self.x1 = int(self.entry_x1.get())
                self.y1 = int(self.entry_y1.get())
            else:
                self.x1 = int(self.entry_x1.get())
                self.y1 = int(self.entry_y1.get())
                self.x2 = int(self.entry_x2.get())
                self.y2 = int(self.entry_y2.get())
        except ValueError as e:
            tkMessageBox.showwarning('Input Error', 'Please input a number!')
            return

        if self.shape == 'sPoint':
            w.delete(self.frame.s)
            self.frame.s = w.create_oval(self.x1, self.y1, self.x1+10, self.y1+10, fill="black")
        elif self.shape == 'ePoint':
            w.delete(self.frame.e)
            self.frame.e = w.create_oval(self.x1, self.y1, self.x1 + 10, self.y1 + 10, fill="magenta")
        elif self.shape == 'Line':
            w.create_line(self.x1, self.y1, self.x2, self.y2, fill="red")
        elif self.shape == 'Circle':
            w.create_oval(self.x1, self.y1, self.x2, self.y2, fill="green")
        elif self.shape == 'Rectangle':
            w.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="blue")
        tkMessageBox.showinfo('Success', 'Shape added!')
        self.controller.show_frame('Top')
        # sync map with world
        self.add2world(self.shape)
        return

    def add2world(self, shape):
        # get world
        world = self.frame.world
        if self.shape == 'sPoint':
            sPoint = Point(self.x1, self.y1, 'start')
            world.start = sPoint
        elif self.shape == 'ePoint':
            ePoint = Point(self.x1, self.y1, 'end')
            world.goal = ePoint
        elif self.shape == 'Line':
            line = Line(self.x1, self.y1, self.x2, self.y2)
            world.lines.append(line)
        elif self.shape == 'Circle':
            circle = Circle(self.x1, self.y1, self.x2, self.y2)
            world.circles.append(circle)
        elif self.shape == 'Rectangle':
            rectangle = Rectangle(self.x1, self.y1, self.x2, self.y2)
            world.rectangles.append(rectangle)
        return

    def prepare(self, shape):
        self.clearEntry()
        self.entry_x1.focus()

        self.shape = shape
        if shape == 'sPoint' or self.shape == 'ePoint':
            self.label_x2.grid_remove()
            self.label_y2.grid_remove()
            self.entry_x2.grid_remove()
            self.entry_y2.grid_remove()
            self.entry_y1.bind('<Return>', self.drawshape)
        else:
            self.label_x2.grid()
            self.label_y2.grid()
            self.entry_x2.grid()
            self.entry_y2.grid()
            self.entry_y2.bind('<Return>', self.drawshape)
        return

    def goBack(self):
        self.clearEntry()
        self.controller.show_frame('Top')
        return

    def clearEntry(self):
        self.entry_x1.delete(0, 'end')
        self.entry_y1.delete(0, 'end')
        self.entry_x2.delete(0, 'end')
        self.entry_y2.delete(0, 'end')
        return


"""---------------------------------------------------------------------------------------------------------------------
                                          MAIN
---------------------------------------------------------------------------------------------------------------------"""
if __name__ == '__main__':
    app = GUI()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        LOG.warn('User terminated client!')
