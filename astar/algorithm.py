from Queue import PriorityQueue
import time

from ui.world import Point


class Astar:
    def __init__(self, map, x, y, start, goal):
        self.map = map
        self.x = x
        self.y = y
        self.start = start
        self.goal = goal


    def get_neighbors(self, node):
        coords = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (-1, -1), (1, 1), (-1, 1), (1, -1)]
        neighbors = []

        for item in coords:
            x = node[0] + item[0]
            y = node[1] + item[1]
            if x > 0 and x < self.x and y > 0 and y < self.x:
                neighbors.append((x, y))

        return neighbors


    def get_distance(self, from_node, to_node):
        return (from_node[0] - to_node[0]) ** 2 + (from_node[1] - to_node[1]) ** 2

    def build_path(self, goal, came_from, cost_so_far):
        current = goal
        path = []

        while current in came_from:
            print(current)
            print(cost_so_far[current])
            path.append(current)
            current = came_from[current]

        return path


    def a_star(self, start, goal):
        closed_set = set()
        open_set = PriorityQueue()

        came_from = {}
        cost_so_far = {}

        open_set.put(start, 0)

        came_from[start] = None
        cost_so_far[start] = 0

        i = 0
        while not open_set.empty():
            current = open_set.get()
            closed_set.add(current)

            i += 1
            #later refcator this to some drawing method
            #if i % 1000 == 0:
                #self.map.world.add_shape(Point(current[0], current[1]))
                #self.map.draw_shapes()

            if current == goal:
                break

            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue

                new_cost = cost_so_far[current] + self.get_distance(current, neighbor)

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.get_distance(goal, neighbor)
                    open_set.put(neighbor, priority)
                    came_from[neighbor] = current

        return came_from, cost_so_far


class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y