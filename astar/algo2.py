import heapq
from Queue import PriorityQueue
from heapq import *
from math import sqrt
import random

Accessible = 1
Obstacle = 0
Sea = 2
Swamp = 3
SQRT2 = 2 ** 0.5


class MyPriorityQueue(PriorityQueue):
    def _put(self, item):
        return super._put((self._get_priority(item), item))

    def _get(self):
        return super._get()[1]

    def _get_priority(self, item):
        return item[1]


class Astar:
    def __init__(self, map, x, y, start, goal):
        self.map = map
        self.x = x
        self.y = y
        self.start = start
        self.goal = goal

    def get_neighbors(self, node):
        coords = [(-1, -1), (1, 1), (-1, 1), (1, -1),
                  (0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbors = []

        for item in coords:
            x = node[0] + item[0]
            y = node[1] + item[1]

            """old method"""
            # if self.map.world.is_allowed(x, y):
            #     if 0 < x < self.x and 0 < y < self.y:
            #         neighbors.append((x, y))
            """new method: check map"""
            area = self.map.world.is_allowed(x, y)
            if area is not Obstacle:
                if 0 < x < self.x and 0 < y < self.y:
                    neighbors.append(((x, y), area))  # neighbor with area property

        return neighbors

    def get_distance(self, from_node, to_node):
        return sqrt((from_node[0] - to_node[0]) ** 2 + (from_node[1] - to_node[1]) ** 2)

    def build_path(self, goal, came_from, cost_so_far):
        current = goal
        path = []

        while current in came_from:
            path.append(current)
            current = came_from[current]

        return path

    def a_star(self):
        closed_set = set()
        closed_set_copy = []  # for plotting process, only new nodes will be plotted to make it faster
        open_set = []
        open_set_copy = []  # for plotting process, the same as above
        came_from = {}
        cost_so_far = {}

        heappush(open_set, (0, self.start))

        came_from[self.start] = None
        cost_so_far[self.start] = 0
        i = 0
        while len(open_set) > 0:
            current = heappop(open_set)  # pop first one, current=(priority, node)
            current = current[1]  # current = node

            i += 1
            # later refcator this to some drawing method
            if i % 500 == 0:
                """uncomment if want to plot both sets"""
                rnd = random.randint(0, 10)
                # for node in open_set_copy:
                #     if rnd < 1:
                #         self.map.visualize_process(node, 'open')
                # for node in closed_set_copy:
                #     if rnd > 9:
                #         self.map.visualize_process(node, 'closed')
                # closed_set_copy = []
                # open_set_copy = []

            if current == self.goal:
                break

            for neighbor in self.get_neighbors(current):
                if neighbor[0] in closed_set:
                    continue

                # distance between current & neighbor only 1 or sqrt2
                if neighbor[0][0] - current[0] == 0 or neighbor[0][1] - current[1] == 0:
                    step = 1
                else:
                    step = SQRT2

                # check neighbor belongs to which area
                if neighbor[1] == Accessible:
                    new_cost = cost_so_far[current] + step
                elif neighbor[1] == Sea:
                    new_cost = cost_so_far[current] + step + 1
                elif neighbor[1] == Swamp:
                    new_cost = cost_so_far[current] + step + 3

                if neighbor[0] not in cost_so_far or new_cost < cost_so_far[neighbor[0]]:
                    cost_so_far[neighbor[0]] = new_cost
                    heuristic_cost = self.get_distance(self.goal, neighbor[0])
                    priority = new_cost + heuristic_cost

                    # check neighbor if in the openset first
                    if neighbor[0] not in closed_set:
                        heappush(open_set, (priority, neighbor[0]))
                        closed_set.add(current)
                        closed_set_copy.append(current)
                    else:
                        old = [v for i, v in enumerate(open_set) if v[1] == neighbor[0]]  # i->index v->tuple
                        open_set.remove(old)
                        heappush(open_set, (priority, neighbor[0]))
                    open_set_copy.append(neighbor[0])  # add for plotting
                    came_from[neighbor[0]] = current

        return came_from, cost_so_far


class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
