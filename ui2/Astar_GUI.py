from Tkinter import *
import tkMessageBox
import tkFont as tkfont
import ttk
import logging
import uuid
import threading
import time
from time import sleep


"""---------------------------------------------------------------------------------------------------------------------
                                          GUI
---------------------------------------------------------------------------------------------------------------------"""
class GUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title('A star algorithm')
        logging.debug('Client has started!')
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # store variables if needed

        # store client UI frames
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

        # head label
        label = Label(self.title_frame, text='A Star Path Finding Algorithm', font=controller.title_font)
        label.pack(fill='x')

        # config panel
        self.execute_button = Button(self.config_frame, text='Play', command=self.startAlgo)
        self.setStart_button = Button(self.config_frame, text='Start Point', command=self.setStartPoint)
        self.setEnd_button = Button(self.config_frame, text='End Point', command=self.setEndPoint)
        self.addLine_button = Button(self.config_frame, text='Add Line', command=self.addLine)
        self.addRect_button = Button(self.config_frame, text='Add Rectangle', command=self.addRect)
        self.addCircle_button = Button(self.config_frame, text='Add Circle', command=self.addCircle)

        self.execute_button.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        self.setStart_button.grid(row=1, column=0)
        self.setEnd_button.grid(row=1, column=1)
        self.addLine_button.grid(row=2, column=0, columnspan=2, sticky=NSEW)
        self.addRect_button.grid(row=3, column=0, columnspan=2, sticky=NSEW)
        self.addCircle_button.grid(row=4, column=0, columnspan=2, sticky=NSEW)

        # canvas
        self.w = Canvas(self.map_frame, width=1000, height=1000, bg='white')
        self.w.pack()
        self.initMap()

        # bind key to start algo
        self.execute_button.bind('<Return>', self.startAlgo)

    def setStartPoint(self):
        frame = self.controller.get_frame('AddShape')
        frame.prepare('Point')
        self.controller.show_frame('AddShape')
        return

    def setEndPoint(self):
        frame = self.controller.get_frame('AddShape')
        frame.prepare('Point')
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
        self.w.create_rectangle(200, 200, 400, 400, fill="blue")
        self.w.create_line(150, 750, 750, 400, fill="red")
        self.w.create_oval(750, 750, 800, 800, fill="green")
        return

    def startAlgo(self):
        return


class AddShape(Frame):
    def __init__(self, master, controller):
        # init Frame
        Frame.__init__(self, master)
        # self.pack(side="top", fill="both", expand=True)
        self.controller = controller

        self.shape = None
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

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

        self.submit_button = Button(self, text='Submit', command=self.drawshape)
        self.back_button = Button(self, text='Back', command=self.goBack)

        self.submit_button.grid(row=4, column=0)
        self.back_button.grid(row=4, column=1)

    def drawshape(self):
        return

    def add2world(self):
        return

    def prepare(self, shape):
        self.shape = shape
        if shape == 'Point':
            self.label_x2.grid_remove()
            self.label_y2.grid_remove()
            self.entry_x2.grid_remove()
            self.entry_y2.grid_remove()
        else:
            self.label_x2.grid()
            self.label_y2.grid()
            self.entry_x2.grid()
            self.entry_y2.grid()
        return

    def goBack(self):
        self.entry_x1.delete(0, 'end')
        self.entry_y1.delete(0, 'end')
        self.entry_x2.delete(0, 'end')
        self.entry_y2.delete(0, 'end')
        self.controller.show_frame('Top')
        return


"""---------------------------------------------------------------------------------------------------------------------
                                          MAIN
---------------------------------------------------------------------------------------------------------------------"""
if __name__ == '__main__':
    app = GUI()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        logging.warn('User terminated client!')
