from astar.algorithm import Astar
from ui.map import Map
from ui.world import *
from Tkinter import *
root = Tk()
canvass = Canvas(root, width=300, height=200)
canvass.pack()
world = World()
#world.add_shape(Rectangle(10, 10, 100, 100))
#world.add_shape(Line(50, 50, 300, 450))
#world.add_shape(Circle(200, 200, 150, 150))
canvass.create_polygon(50,30,150,50,250,30,150,10, fill="green")
canvass.create_line(50, 50, 250, 150, fill="red", width=5)
canvass.create_text(150, 100, text="Amazing!", fill="purple", font="Helvetica 26 bold underline")
canvass.create_text(150, 100, text="Carpe Diem!", anchor=SW, fill="orange", font="Times 18 italic")
world.add_start((420, 310))
world.add_goal((450, 345))

canvas = Map(world)
canvas.draw()
