from Tkinter import *
import tkMessageBox
import tkFont as tkfont
import ttk
import logging
from ui.world import World
from ui.world import Shape, Point, Line, Circle, Rectangle
#from astar.algorithm import Astar
from astar.algo2 import Astar
from threading import Thread
from PIL import ImageTk
from PIL import Image


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
        self.title_frame.grid(row=0, column=0)
        self.config_frame = Frame(self)
        self.config_frame.grid(row=2, column=0)
        self.map_frame = Frame(self)
        self.map_frame.grid(row=1, column=0)
        # some variables if needed
        self.world = World()
        self.s = None
        self.e = None
        # head label
        label = Label(self.title_frame, text='Run! Jerry Run!', font=controller.title_font)
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

        self.execute_button.grid(row=0, column=0, rowspan=2, sticky=NS)
        self.clear_button.grid(row=0, column=1, sticky=NSEW)
        self.init_button.grid(row=1, column=1, sticky=NSEW)
        self.setStart_button.grid(row=0, column=2, sticky=NSEW)
        self.setEnd_button.grid(row=1, column=2, sticky=NSEW)
        #self.addLine_button.grid(row=3, column=0, columnspan=2, sticky=NSEW)
        self.addRect_button.grid(row=0, column=3, sticky=NSEW)
        self.addCircle_button.grid(row=1, column=3, sticky=NSEW)

        # config panel for drag&draw
        self.area_label = Label(self.config_frame, text='Drag & Draw')
        self.obstacle_button = Button(self.config_frame, text='Obstacle', command=self.area_obstacle)
        self.sea_button = Button(self.config_frame, text='Sea', command=self.area_sea)
        self.swamp_button = Button(self.config_frame, text='Swamp', command=self.area_swamp)
        self.cancel_button = Button(self.config_frame, text='Cancel', command=self.area_cancel)

        self.area_label.grid(row=0, column=4)
        self.obstacle_button.grid(row=1, column=4, sticky=NSEW)
        self.sea_button.grid(row=1, column=5, sticky=NSEW)
        self.swamp_button.grid(row=1, column=6, sticky=NSEW)
        self.cancel_button.grid(row=0, column=5, sticky=NSEW)
        self.cancel_button['state'] = 'disabled'

        # canvas
        self.w = Canvas(self.map_frame, width=600, height=600, bg='white', bd=0, highlightthickness=0, relief='ridge')
        self.w.pack()
        self.initMap()

        # bind key to start algo
        self.execute_button.bind('<Return>', self.startAlgo)
        # bind key for create rectangle
        self.area = None
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None
        self.w.bind("<ButtonPress-1>", self.on_button_press)
        self.w.bind("<B1-Motion>", self.on_move_press)
        self.w.bind("<ButtonRelease-1>", self.on_button_release)

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
        # add Tom & Jerry
        self.bg = ImageTk.PhotoImage(file="1.png")
        self.w.create_image(0, 0, image=self.bg, anchor=NW)
        image = Image.open('4.png')
        self.tompic = ImageTk.PhotoImage(image)
        self.tom = self.w.create_image(500-40, 100-70, image=self.tompic, anchor=NW)
        image2 = Image.open('3.png')
        self.jerrypic = ImageTk.PhotoImage(image2)
        self.jerry = self.w.create_image(100 + 15, 500 + 10, image=self.jerrypic, anchor=NW)

        # demo
        self.s = self.w.create_oval(500-5, 100-5, 510, 110, fill="black")
        sPoint = Point(500, 100, 'start')
        self.world.start = sPoint

        self.e = self.w.create_oval(100-5, 500-5, 110, 510, fill="magenta")
        ePoint = Point(100, 500, 'end')
        self.world.goal = ePoint

        self.w.create_rectangle(150, 150, 300, 300, fill="blue")
        rectangle = Rectangle(150, 150, 300, 300)
        self.world.rectangles.append(rectangle)
        self.world.update_map(rectangle, 'Obstacle')

        self.w.create_rectangle(100, 400, 550, 410, fill="#808000")
        rectangle = Rectangle(100, 400, 550, 410)
        self.world.rectangles.append(rectangle)
        self.world.update_map(rectangle, 'Obstacle')

        self.w.create_rectangle(300, 300, 400, 310, fill="#808080")
        rectangle = Rectangle(300, 300, 400, 310)
        self.world.rectangles.append(rectangle)
        self.world.update_map(rectangle, 'Obstacle')

        self.w.create_oval(420, 300, 470, 350, fill="red")
        circle = Circle(420, 300, 470, 350)
        self.world.circles.append(circle)
        self.world.update_map(circle, 'Obstacle')
        return

    def clearMap(self):
        self.w.delete(ALL)
        return

    def startAlgo(self):
        LOG.debug('Start Path Finding...')
        self.execute_button['state'] = 'disabled'
        # put algorithm into a independent thread, so that can visualize the process
        t = Thread(target=self.Algo)
        t.start()
        return

    def Algo(self):
        start = (self.world.start.x, self.world.start.y)
        goal = (self.world.goal.x, self.world.goal.y)

        alg = Astar(self, 600, 600, start, goal)
        came_from, cost_so_far = alg.a_star()
        path = alg.build_path(goal, came_from, cost_so_far)
        LOG.debug('Path Finding Finished! Printing final path...')
        self.execute_button['state'] = 'normal'
        # to draw the final path
        for p in path:
            self.w.create_rectangle(p[0], p[1], p[0] + 1, p[1] + 1, fill='cyan')
        LOG.debug('Complete!')
        return

    def visualize_process(self, node, flag):
        # draw the explored area
        if flag == 'open':
            self.w.create_oval(node[0], node[1], node[0] + 1, node[1] + 1, fill='cyan', outline='cyan')
        else:
            self.w.create_oval(node[0], node[1], node[0] + 1, node[1] + 1, fill='yellow', outline='yellow')

    def on_button_press(self, e):
        self.rect = None
        # save mouse drag start position
        self.start_x = self.w.canvasx(e.x)
        self.start_y = self.w.canvasy(e.y)
        # decide color
        if not self.area:
            color = 'red'
        elif self.area == 'Obstacle':
            color = '#808080'
        elif self.area == 'Sea':
            color = 'blue'
        elif self.area == 'Swamp':
            color = '#808000'
        else:
            color = 'white'
        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.w.create_rectangle(0, 0, 1, 1, fill=color)
        return

    def on_move_press(self, e):
        self.curX = self.w.canvasx(e.x)
        self.curY = self.w.canvasy(e.y)

        # expand rectangle as you drag the mouse
        self.w.coords(self.rect, int(self.start_x), int(self.start_y), int(self.curX), int(self.curY))
        return

    def on_button_release(self, e):
        # check button
        if not self.area:
            tkMessageBox.showwarning('Input Error', 'Please select an area type first!')
            self.w.delete(self.rect)
            self.rect = None
            return
        # draw into world
        rectangle = Rectangle(int(self.start_x), int(self.start_y), int(self.curX), int(self.curY))
        self.world.rectangles.append(rectangle)
        self.world.update_map(rectangle, self.area)
        self.area = None
        # enable buttons
        self.obstacle_button['state'] = 'normal'
        self.sea_button['state'] = 'normal'
        self.swamp_button['state'] = 'normal'
        pass

    def area_obstacle(self):
        self.area = 'Obstacle'
        self.cancel_button['state'] = 'normal'
        self.obstacle_button['state'] = 'disabled'
        self.sea_button['state'] = 'disabled'
        self.swamp_button['state'] = 'disabled'
        return

    def area_sea(self):
        self.area = 'Sea'
        self.cancel_button['state'] = 'normal'
        self.obstacle_button['state'] = 'disabled'
        self.sea_button['state'] = 'disabled'
        self.swamp_button['state'] = 'disabled'
        return

    def area_swamp(self):
        self.area = 'Swamp'
        self.cancel_button['state'] = 'normal'
        self.obstacle_button['state'] = 'disabled'
        self.sea_button['state'] = 'disabled'
        self.swamp_button['state'] = 'disabled'
        return

    def area_cancel(self):
        self.area = None
        self.cancel_button['state'] = 'disabled'
        # enable buttons
        self.obstacle_button['state'] = 'normal'
        self.sea_button['state'] = 'normal'
        self.swamp_button['state'] = 'normal'
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
        # Selection
        self.area_label = Label(self, text='Type')
        self.area_label.grid(row=4, column=0)
        self.area = StringVar()
        self.area.set('Obstacle')
        self.area_option = OptionMenu(self, self.area, 'Obstacle', 'Sea', 'Swamp')
        self.area_option.grid(row=4, column=1, sticky=NSEW)
        # Buttons
        self.submit_button = Button(self, text='Submit', command=self.drawshape)
        self.back_button = Button(self, text='Back', command=self.goBack)

        self.submit_button.grid(row=5, column=0)
        self.back_button.grid(row=5, column=1)

    def drawshape(self, e=None):
        self.frame = self.controller.get_frame('Top')
        w = self.frame.w
        try:
            area = self.area.get()
            if area == 'Obstacle':
                color = '#808080'
            elif area == 'Sea':
                color = 'blue'
            elif area == 'Swamp':
                color = '#808000'
            else:
                color = 'white'
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
            w.delete(self.frame.tom)
            self.frame.s = w.create_oval(self.x1, self.y1, self.x1+10, self.y1+10, fill="black")
            self.frame.tom = w.create_image(self.x1 - 40, self.y1 - 70, image=self.frame.tompic, anchor=NW)
        elif self.shape == 'ePoint':
            w.delete(self.frame.e)
            w.delete(self.frame.jerry)
            self.frame.e = w.create_oval(self.x1, self.y1, self.x1 + 10, self.y1 + 10, fill="magenta")
            self.frame.jerry = w.create_image(self.x1 + 15, self.y1 + 10, image=self.frame.jerrypic, anchor=NW)
        elif self.shape == 'Line':
            w.create_line(self.x1, self.y1, self.x2, self.y2, fill=color)
        elif self.shape == 'Circle':
            if self.x2-self.x1 == self.y2-self.y1:
                w.create_oval(self.x1, self.y1, self.x2, self.y2, fill=color)
            else:
                tkMessageBox.showwarning('Input Error', 'Please value invalid! Must be a circle!')
                return
        elif self.shape == 'Rectangle':
            w.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=color)
        tkMessageBox.showinfo('Success', 'Shape added!')
        self.controller.show_frame('Top')
        # sync map with world
        self.add2world(area)
        return

    def add2world(self, area):
        # get world
        world = self.frame.world
        if self.shape == 'sPoint':
            sPoint = Point(self.x1, self.y1, 'start')
            world.start = sPoint
        elif self.shape == 'ePoint':
            ePoint = Point(self.x1, self.y1, 'end')
            world.goal = ePoint
        elif self.shape == 'Line':  # not use any more
            line = Line(self.x1, self.y1, self.x2, self.y2)
            world.lines.append(line)
        elif self.shape == 'Circle':
            circle = Circle(self.x1-5, self.y1-5, self.x2, self.y2)
            world.circles.append(circle)
            world.update_map(circle, area)
        elif self.shape == 'Rectangle':
            rectangle = Rectangle(self.x1, self.y1, self.x2, self.y2)
            world.rectangles.append(rectangle)
            world.update_map(rectangle, area)
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
            self.area_label.grid_remove()
            self.area_option.grid_remove()
        else:
            self.label_x2.grid()
            self.label_y2.grid()
            self.entry_x2.grid()
            self.entry_y2.grid()
            self.entry_y2.bind('<Return>', self.drawshape)
            self.area_label.grid()
            self.area_option.grid()
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
