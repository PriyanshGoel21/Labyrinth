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
    grid_x = 41
    grid_y = 41
    if request.method == "POST":
        # grid_x = int(request.form["gridX"])
        # grid_y = int(request.form["gridY"])
        ...
    elif request.headers.get("accept") == "text/event-stream":
        start = int(request.cookies["start"])
        end = int(request.cookies["end"])
        try:
            walls = list(map(int, request.cookies["walls"].split(",")))
        except ValueError:
            walls = []
        maze = Maze(start=start, end=end, walls=walls, grid_y=41, grid_x=41)

        def events():
            for i in breadth_first_search.search(maze):
                if isinstance(i, tuple):
                    yield f"data: i{i[0]*41 + i[1]}\n\n"
                    time.sleep(0.05)
                elif isinstance(i, list):
                    for x in i:
                        yield f"data: xi{x[0] * 41 + x[1]}\n\n"
                        time.sleep(0.02)
            yield f"data: close\n\n"

        return Response(events(), content_type="text/event-stream")
    return render_template(
        "index.html",
        grid_x=grid_x,
        grid_y=grid_y,
    )


if __name__ == "__main__":
    app.run(debug=True)

# {{ 'wall' if id not in white_spaces else '' }} {{ 'start' if id == start[0]*grid_y + start[1] else '' }} {{ 'end'
# if id == end[0]*grid_y + end[1] else '' }}
