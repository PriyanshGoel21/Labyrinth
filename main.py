import sys
import os
import time

import numpy as np

import breadth_first_search
import greedy_breadth_first_search
from data_structures import Maze

# if __name__ == "__main__":
# algorithms = [breadth_first_search.search, greedy_breadth_first_search.search]
# match len(sys.argv):
#     case 1:
#         for algorithm in algorithms:
#             for subdir, dirs, files in os.walk("mazes"):
#                 for file in files:
#                     filepath = subdir + "/" + file
#                     if filepath.endswith(".png"):
#                         maze = Maze(filepath)
#                         start = time.process_time()
#                         path = algorithm(maze)
#                         end = time.process_time()
#                         print(f"{filepath} - {end-start}")
#     case _:
#         maze = Maze(sys.argv[1])
#         path = breadth_first_search.search(maze)
#         image = maze.maze_image.convert("RGB")
#         image_pixels = image.load()
#         for coordinate in path:
#             image_pixels[coordinate[1], coordinate[0]] = (255, 0, 0)  # noqa
#
#         image.save(f"{sys.argv[1].split('/')[1]}")

import time

from flask import Flask, render_template, request, Response, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    maze = Maze("mazes/normal.png")
    grid_x = 40
    grid_y = 20
    white_spaces = list(np.flatnonzero(maze.maze))
    if request.method == "POST":
        grid_x = int(request.form["gridX"])
        grid_y = int(request.form["gridY"])
    elif request.headers.get("accept") == "text/event-stream":

        def events():
            for i in greedy_breadth_first_search.search(maze):
                yield f"data: i{i[0]*41 + i[1]}\n\n"
                time.sleep(0.05)  # an artificial delay

        return Response(events(), content_type="text/event-stream")
    return render_template(
        "index.html",
        grid_x=grid_x,
        grid_y=grid_y,
        white_spaces=white_spaces,
        start=maze.start,
        end=maze.end,
    )


if __name__ == "__main__":
    app.run(debug=True)
