from PIL import Image
import numpy as np


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
