from Queue import PriorityQueue

from astar.algorithm import Astar


start = (1, 1)
goal = (100, 150)

alg = Astar(400, 400)
came_from, cost_so_far = alg.a_star()

alg.build_path(goal, came_from, cost_so_far)
