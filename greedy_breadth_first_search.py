import time
from queue import PriorityQueue

from data_structures import Maze


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def search(maze: Maze):
    frontier = PriorityQueue()
    frontier.put(maze.start, 0)
    came_from = dict()
    came_from[maze.start] = None
    while not frontier.empty():
        current = frontier.get()
        if current == maze.end:
            break
        for next_node in maze.get_neighbors(current):
            if next_node not in came_from:
                frontier.put(next_node, heuristic(maze.end, next_node))
                came_from[next_node] = current
                yield next_node
    # current = maze.end
    # path = []
    # while current != maze.start:
    #     path.append(current)
    #     current = came_from[current]
    # path.append(maze.start)
    # path.reverse()
    # return path
