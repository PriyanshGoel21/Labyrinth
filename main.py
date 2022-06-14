from queue import Queue
import numpy as np
from PIL import Image
import sys
import os
import time

Image.MAX_IMAGE_PIXELS = 225030001


class Maze:
    def __init__(self, image_path: str):
        self.maze_image = Image.open(image_path)
        self.maze = np.array(self.maze_image)  # noqa
        self.start = (0, 0)
        self.end = (self.maze.shape[0] - 1, self.maze.shape[0] - 1)
        for index, pixel in enumerate(self.maze[0]):
            if pixel == 1:
                self.start = (0, index)
                break
        for index, pixel in enumerate(self.maze[self.maze.shape[0] - 1]):
            if pixel == 1:
                self.end = (self.maze.shape[0] - 1, index)

    def get_neighbors(self, current: tuple[int, int]):
        for n in (-1, 1):
            if not (
                current[0] + n > self.maze.shape[0] - 1
                or current[0] + n < 0
                or self.maze[current[0] + n, current[1]] == 0
            ):
                yield current[0] + n, current[1]
            if not (
                current[1] + n > self.maze.shape[1] - 1
                or current[1] + n < 0
                or self.maze[current[0], current[1] + n] == 0
            ):
                yield current[0], current[1] + n


def main(image_path: str):
    maze = Maze(image_path)
    frontier: Queue[tuple[int, int]] = Queue()
    frontier.put(maze.start)
    came_from = dict()
    came_from[maze.start] = None
    y = 0
    while not frontier.empty():
        current = frontier.get()
        if current == maze.end:
            break
        for next_node in maze.get_neighbors(current):
            if next_node not in came_from:
                frontier.put(next_node)
                came_from[next_node] = current
        image = maze.maze_image.convert("RGB")
        image_pixels = image.load()
        for coordinate in came_from:
            image_pixels[coordinate[1], coordinate[0]] = (0, 255, 0)  # noqa

        image.save(f"{y}-{image_path.split('/')[1]}")
        y += 1

    current = maze.end
    path = []
    while current != maze.start:
        path.append(current)
        current = came_from[current]
    path.append(maze.start)
    path.reverse()

    image = maze.maze_image.convert("RGB")
    image_pixels = image.load()
    for coordinate in path:
        image_pixels[coordinate[1], coordinate[0]] = (255, 0, 0)  # noqa

    image.save(f"{image_path.split('/')[1]}")


if __name__ == "__main__":

    match len(sys.argv):
        case 1:
            for subdir, dirs, files in os.walk("mazes"):
                for file in files:
                    filepath = subdir + "/" + file
                    if filepath.endswith(".png"):
                        start = time.process_time()
                        main(f"{filepath}")
                        end = time.process_time()
                        print(f"{filepath} - {end-start}")

        case _:
            main(sys.argv[1])
