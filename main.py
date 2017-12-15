from ui.map import Map
from ui.world import *

world = World()
world.add_shape(Rectangle(10, 10, 100, 100))
world.add_shape(Line(50, 50, 300, 450))
world.add_shape(Circle(200, 200, 150, 150))

canvas = Map(world)
canvas.draw()