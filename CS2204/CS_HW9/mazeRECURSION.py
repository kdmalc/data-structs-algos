"""Maze generation and path finding"""

__author__ = "malcolkd"


from collections import deque
from random import randrange


class Cell:
    """
    Cell objects represent a single maze location with up-to 4 walls.

    The .N, .E, .S, .W attributes represent the walls in the North,
    East, South and West directions. If the attribute is True, there is a
    wall in the given direction.

    The .x and .y attributes store the coordinates of the cell.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.N = True
        self.E = True
        self.S = True
        self.W = True

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def remove_wall(self, direction):
        """
        Remove one wall - keep all neighbors consistent
        Direction is one of these strings: 'N', 'E', 'S', 'W'
        """
        direction = direction.upper()

        loc = " @(x=%d, y=%d)" % (self.x, self.y)
        if direction == "W":
            if self.x < 1:
                raise ValueError("cannot remove side wall on west" + loc)
            if self.W:
                self.W = False
                assert maze[self.x - 1][self.y].E
                maze[self.x - 1][self.y].E = False
        if direction == "E":
            if self.x >= size_x - 1:
                raise ValueError("cannot remove side wall on east" + loc)
            if self.E:
                self.E = False
                assert maze[self.x + 1][self.y].W
                maze[self.x + 1][self.y].W = False
        if direction == "N":
            if self.y < 1:
                raise ValueError("cannot remove side wall on north" + loc)
            if self.N:
                self.N = False
                assert maze[self.x][self.y - 1].S
                maze[self.x][self.y - 1].S = False
        if direction == "S":
            if self.y >= size_y - 1:
                raise ValueError("cannot remove side wall on south" + loc)
            if self.S:
                self.S = False
                assert maze[self.x][self.y + 1].N
                maze[self.x][self.y + 1].N = False

    def has_wall(self, direction):
        """
        True if there is a wall in the given direction
        Direction is one of these strings: 'N', 'E', 'S', 'W'
        """
        return getattr(self, direction.upper())


# Global variables for the maze and its size
size_x = size_y = 32
maze = [[Cell(x, y) for y in range(size_y)] for x in range(size_x)]
backtrack_check = []


def is_visited(cell, visited):
    if len(visited) == 0:
        return False

    for i in range(1, len(visited)):
        if cell == visited[-i]:
            return True
    return False


def get_unvisited_neighbors(maze, cell, visited):
    print(cell)
    x, y = cell.x, cell.y
    unvisited_neighbors = []
    if (x == 0):
        neighbors = [maze[x][y+1], maze[x+1][y], maze[x][y-1]]
    elif (x == size_x-1):
        neighbors = [maze[x][y+1], maze[x][y-1], maze[x-1][y]]
    elif (y == 0):
        neighbors = [maze[x][y+1], maze[x+1][y], maze[x-1][y]]
    elif (y == size_y-1):
        neighbors = [maze[x+1][y], maze[x][y-1], maze[x-1][y]]
    else:
        print("ELSE")
        '''
        print("--------")
        print("ELSE")
        print(x)
        print(x==0)
        print(y)
        print(y==0)
        print("--------")
        '''
        neighbors = [maze[x][y+1], maze[x+1][y], maze[x][y-1], maze[x-1][y]]
    for neighbor in neighbors:
        dx, dy = neighbor.x - x, neighbor.y - y
        if not is_visited(neighbor, visited) and dx < 2 and dy < 2:
            unvisited_neighbors.append(neighbor)
    return unvisited_neighbors


def choose_cell(unvisited_neighbors):
    n = len(unvisited_neighbors)
    print(n)
    idx = randrange(1, n)
    return unvisited_neighbors[idx]


def get_direction(cell, new_cell):
    x, y = cell.x, cell.y
    new_x, new_y = new_cell.x, new_cell.y
    print(f"({x}, {y}) --> ({new_x}, {new_y})")
    dx, dy = new_x - x, new_y - y
    change = (dx, dy)
    dir_dict = {(0, 1): 'N', (1, 0): 'E', (0, -1): 'S', (-1, 0): 'W'}
    my_dir = dir_dict.get(change)
    if my_dir is None:
        print("ERROR DIRECTION NOT FOUND")
        print(change)
        my_dir = 'DEADEND'
    return my_dir


def backtrack(visited):
    print("Backtracking")
    deadcell = visited.pop()
    prevcell = visited.pop()

    # if backtrack_check.count(deadcell) > 2:
    if len(backtrack_check) > 2:
        return 1

    visited.append(prevcell)
    visited.append(deadcell)
    maze_recursion(prevcell, visited)
    backtrack_check.append(deadcell)


def maze_recursion(cell, visited):
    visited.append(cell)

    unvisited_neighbors = get_unvisited_neighbors(maze, cell, visited)

    if len(unvisited_neighbors) == 0:
        deadend = backtrack(visited)
        if deadend:
            print("Backtrack: Got stuck")
            return
    elif len(unvisited_neighbors) == 1:
        new_cell = unvisited_neighbors[0]
    else:
        new_cell = choose_cell(unvisited_neighbors)

    if (cell.x == 0 or cell.y == 0) and (new_cell.x == 31 or new_cell.y == 31):
        print(unvisited_neighbors)

    my_dir = get_direction(cell, new_cell)

    if my_dir == 'DEADEND':
        return

    try:
        cell.remove_wall(my_dir)
    except ValueError:
        deadend = backtrack(visited)
        if deadend:
            print("Backtrack: Got stuck")
            return

    maze_recursion(new_cell, visited)


def build_maze():
    """
    Build a valid maze by tearing down walls

    The function has access to the following global variables:
        size_x - integer, the horizontal size of the maze
        size_y - integer, the vertical size of the maze
        maze - a two dimensional array (list of lists) for all cells
            e.g. maze[3][4] is a Cell object for x=3, y=4

    This function does not need to return any value but should modify the
    cells (walls) to create a perfect maze.
    When the function is invoked all cells have all their four walls standing.
    """
    # Choose a random start point
    x = randrange(1, size_x)
    y = randrange(1, size_y)
    cell = maze[x][y]
    print(f"Starting cell is ({x},{y})")

    # Implement a stack for backtracking, tracking visited cells
    visited = deque()

    maze_recursion(cell, visited)
    return


def find_path(start, end):
    """
    Find a path from the start position to the end

    The start and end parameters are coordinate pairs (tuples) for the
    start and end (target) position. E.g. (0, 0) or (7, 13).

    The function has access to the following global variables:
        size_x - integer, the horizontal size of the maze
        size_y - integer, the vertical size of the maze
        maze - a two dimensional array (list of lists) for all cells
            e.g. maze[3][4] is a Cell object for x=3, y=4

    The function is invoked after build_maze removed the walls to create a
    perfect maze.

    This function shall return a list of coordinate pairs (tuples or lists)
    which list the cell coordinates on a valid path from start to end.
    E.g.: [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), ..., (7, 13)]
    """
    pass


###############################################################################
# Testing and visualizing results - no need to understand and/or change
def draw_maze(start=None, end=None, path=None):
    """Draw the maze and the path in a graphical window"""
    import tkinter
    cell_size = 20
    master = tkinter.Tk()
    canvas = tkinter.Canvas(master, width=size_x * cell_size + 1,
                            height=size_y * cell_size + 1,
                            bd=0, highlightthickness=0, relief='ridge')
    canvas.pack()
    for x in range(size_x):
        for y in range(size_y):
            if maze[x][y].N:
                canvas.create_line(cell_size * x, cell_size * y,
                                   cell_size * (x + 1), cell_size * y)
            if maze[x][y].E:
                canvas.create_line(cell_size * (x + 1), cell_size * y,
                                   cell_size * (x + 1), cell_size * (y + 1))
            if maze[x][y].S:
                canvas.create_line(cell_size * x, cell_size * (y + 1),
                                   cell_size * (x + 1), cell_size * (y + 1))
            if maze[x][y].W:
                canvas.create_line(cell_size * x, cell_size * y,
                                   cell_size * x, cell_size * (y + 1))

    if path is not None:
        line = [x * cell_size + cell_size // 2 for step in path for x in step]
        canvas.create_line(*line, fill='red', width=2)

    radius = cell_size // 3
    if start is not None:
        img_start = [cell_size * x + cell_size // 2 for x in start]
        canvas.create_oval(img_start[0] - radius,
                           img_start[1] - radius,
                           img_start[0] + radius,
                           img_start[1] + radius, fill='red')
    if end is not None:
        img_end = [cell_size * x + cell_size // 2 for x in end]
        canvas.create_oval(img_end[0] - radius,
                           img_end[1] - radius,
                           img_end[0] + radius,
                           img_end[1] + radius, fill='green')

    master.title('Maze')
    master.lift()
    master.call('wm', 'attributes', '.', '-topmost', True)
    tkinter.mainloop()


def main():
    import sys

    sys.setrecursionlimit(4096)

    print("Testing build_maze()...")
    build_maze()

    # checking maze
    maze_ok = True
    n_edges = 0
    for x in range(size_x):
        for y in range(size_y):
            n_node_edges = 0
            for direction in 'NESW':
                n_node_edges += not maze[x][y].has_wall(direction)
            if n_node_edges < 1:
                # print('ERROR: walled in cell @ (x=%d, y=%d)' % (x, y))
                maze_ok = False
            n_edges += n_node_edges
    n_perfect_edges = (size_x * size_y - 1) * 2
    if n_edges < n_perfect_edges:
        print('ERROR: not a perfect maze, too many walls')
        maze_ok = False
    if n_edges > n_perfect_edges:
        print('ERROR: not a perfect maze, redundant paths')
        maze_ok = False

    if not maze_ok:
        print("Error in maze building task (fix this first): 0 pts")
        draw_maze()
        return

    print("Testing find_path()...")
    start, end = (0, 0), (size_x - 1, size_y - 1)
    path = find_path(start, end)

    # checking path
    path_ok = True
    try:
        assert len(path) >= 2
        if path[0] != start:
            print('ERROR: invalid starting point for path', path[0])
            path_ok = False
        if path[-1] != end:
            print('ERROR: invalid endpoint for path', path[-1])
            path_ok = False

        prev = None
        for step in path:
            assert 0 <= step[0] < size_x
            assert 0 <= step[1] < size_y
            if prev is not None:
                dst = abs(step[0] - prev[0]) + abs(step[1] - prev[1])
                if dst != 1:
                    print('ERROR: invalid step in path', prev, step)
                    path_ok = False
            prev = step

    except Exception as e:
        print(e)
        print('ERROR: invalid path object:', path)
        path_ok = False
        path = None

    if path_ok:
        print("Maze and path looks good: 100 pts")
    else:
        print("Maze looks good, but incorrect path: 50 pts")

    draw_maze(start, end, path)


if __name__ == '__main__':
    main()
