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


###############################################################################
# Global variables for the maze and its size
size_x = size_y = 32
maze = [[Cell(x, y) for y in range(size_y)] for x in range(size_x)]
backtrack_check = []
start_coords = []
dir_list = []
back_dir = []


def is_visited(cell, visited):
    '''
    Check if a given cell is in the visited stack
    '''
    return cell in visited


def get_unvisited_neighbors(cell, visited):
    '''
    Check all neighbors, then check is they have bene visited yet
    '''
    x, y = cell.x, cell.y
    unvisited_neighbors = []

    # Get all legal neighbors
    if (x == 0):
        if x == y:
            neighbors = [maze[x+1][y], maze[x][y+1]]
        elif (y == size_y-1):
            neighbors = [maze[x+1][y], maze[x][y-1]]
        else:
            neighbors = [maze[x][y+1], maze[x+1][y], maze[x][y-1]]
    elif (x == size_x-1):
        if x == y:
            neighbors = [maze[x-1][y], maze[x][y-1]]
        elif y == 0:
            neighbors = [maze[x-1][y], maze[x][y+1]]
        else:
            neighbors = [maze[x][y+1], maze[x][y-1], maze[x-1][y]]
    elif (y == 0):
        neighbors = [maze[x][y+1], maze[x+1][y], maze[x-1][y]]
    elif (y == size_y-1):
        neighbors = [maze[x+1][y], maze[x][y-1], maze[x-1][y]]
    else:
        neighbors = [maze[x][y+1], maze[x+1][y], maze[x][y-1], maze[x-1][y]]

    # Check to see if neighbors are visited
    for neighbor in neighbors:
        dx, dy = neighbor.x - x, neighbor.y - y
        if (neighbor not in visited) and dx < 2 and dy < 2:
            unvisited_neighbors.append(neighbor)
    return unvisited_neighbors


def choose_cell(unvisited_neighbors):
    '''
    Choose a random cell to go to next, coming from the pool
    of unvisited neighbors
    '''
    n = len(unvisited_neighbors)
    idx = randrange(1, n)
    return unvisited_neighbors[idx]


def get_direction(cell, new_cell):
    '''
    Get the direction (string) from the current cell to the new cell
    '''
    x, y = cell.x, cell.y
    new_x, new_y = new_cell.x, new_cell.y
    print(f"({x}, {y}) --> ({new_x}, {new_y})")
    dx, dy = new_x - x, new_y - y
    change = (dx, dy)
    dir_dict = {(0, -1): 'N', (1, 0): 'E', (0, 1): 'S', (-1, 0): 'W'}
    my_dir = dir_dict.get(change)
    if my_dir is None:
        print("Pulling from back_dir")
        my_dir = back_dir[-1]
        if my_dir is None:
            print("ERROR DIRECTION NOT FOUND")
            print(f"Change: {change}")
            print(f"{x}, {y}, {new_x}, {new_y}")
            my_dir = 'DEADEND'
    return my_dir


def get_cell_before(my_cell, visited):
    prevcell = 0
    for cell in visited:
        if cell == my_cell:
            return prevcell
        prevcell = cell


def backtrack(visited):
    print("Backtracking")
    deadcell = visited.pop()
    prevcell = visited.pop()
    cell_list = [deadcell, prevcell]
    popped_dir_list = [dir_list[-1], dir_list[-2]]
    subdir_list = dir_list[0:len(dir_list)-3]

    visited.append(deadcell)
    if len(backtrack_check) > 1 and deadcell == backtrack_check[-2]:
        # We are stuck in a loop
        print("---")
        print("---")
        print("---")
        print("Backtracked in loop?")
        print(f"Deadcell: {deadcell}")
        print(f"Previous cell: {prevcell}")
        print(f"Last backtrack: {backtrack_check[-1]}")
        print(f"2nd backtrack: {backtrack_check[-2]}")
        print(f"3rd backtrack: {backtrack_check[-3]}")
        hold = list(visited)
        print("Last 5 visited cells:")
        print(hold[-5:-1])
        print("---")
        print("---")
        print("---")
        return 1

    # Backtrack until we get to a cell that has at least 1 unvisited neighbor
    while len(get_unvisited_neighbors(prevcell, visited)) < 2:
        prevcell = visited.pop()
        cell_list.append(prevcell)
        my_dir = subdir_list[-1]
        subdir_list = subdir_list[0:len(subdir_list)-2]
        popped_dir_list.append(my_dir)

    neighbors = get_unvisited_neighbors(prevcell, visited)
    neighbors = [ne for ne in neighbors if ne is not deadcell]

    # Once we find an unvisited neighbor, rebuild visited stack
    for cell in cell_list:
        if cell not in visited:
            visited.append(cell)

    backtrack_check.append(deadcell)

    if len(neighbors) == 0:
        print("ERROR THIS IS NEVER SUPPOSED TO RUN")
        return 1
    elif (neighbors[0].x == start_coords[0] and
          neighbors[0].y == start_coords[1]):
        # We are at the starting cell, backtracked all the way
        # Pretty sure this should also never run (should get caught above)
        print("Backtracked to start")
        return 1
    else:
        # Failed fix
        # return get_cell_before(prevcell, visited)

        # Results in a not perfect maze
        # back_dir.append(my_dir)
        back_dir.append(subdir_list[-1])
        return prevcell


def maze_recursion(cell, visited):
    if cell not in visited:
        visited.append(cell)

    unvisited_neighbors = get_unvisited_neighbors(cell, visited)

    if len(visited) == (size_x * size_y):
        '''
        for cell in maze:
            if cell not in visited:
                print("NO")
        '''

        print("SUCCESS: Visited all cells")
        return
    elif len(unvisited_neighbors) == 0:
        deadend = backtrack(visited)
        if deadend == 1:
            print("Backtrack ELIF1")
            return
        else:
            new_cell = deadend
    elif len(unvisited_neighbors) == 1:
        new_cell = unvisited_neighbors[0]
    else:
        new_cell = choose_cell(unvisited_neighbors)

    my_dir = get_direction(cell, new_cell)

    if my_dir == 'DEADEND':
        deadend = backtrack(visited)
        if deadend == 1:
            print("Backtrack ELIF2")
            return
        else:
            new_cell = deadend

    dir_list.append(my_dir)

    try:
        cell.remove_wall(my_dir)
    except ValueError:
        deadend = backtrack(visited)
        if deadend == 1:
            print("Backtrack TRY")
            return
        else:
            new_cell = deadend

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
    x, y = randrange(1, size_x), randrange(1, size_y)
    # x, y = 0, 0
    cell = maze[x][y]
    start_coords.append(x)
    start_coords.append(y)
    print(f"Starting cell is ({x},{y})")

    # Implement a stack for backtracking, tracking visited cells
    visited = deque()

    maze_recursion(cell, visited)
    return


###############################################################################


def make_branch(choice_start, my_directions, visited_find, start, end):
    '''
    When we have multiple options of which way to go, this will choose and
    also remember what the cell was that the options appeared at.
    It explores in a DFS manner.  it will come back to choice_start if
    the final cell is not the end
    '''
    # Inits
    int2dir = {1: 'N', 2: 'E', 3: 'S', 4: 'W'}
    int2dz = {1: (0, -1), 2: (1, 0), 3: (0, 1), 4: (-1, 0)}
    cell_possible = []

    for idx in range(1, len(my_directions)):
        my_dir_int = my_directions[idx]
        my_dir = int2dir[my_dir_int]
        my_dz = int2dz[my_dir_int]

        new_cell = maze[choice_start.x + my_dz[0]][choice_start.y + my_dz[1]]
        # "Recurse"
        visited_find.append(new_cell)
        cell_possible.append(new_cell)

    for cell in cell_possible:
        find_recursion(cell, visited_find, start, end)
    print("BRANCH FAIL")


def find_recursion(cell, visited_find, start, end):
    # Base case
    if cell.x == end[0] and cell.y == end[1]:
        print("GREAT SUCCESS")
        return

    # Inits
    int2dir = {1: 'N', 2: 'E', 3: 'S', 4: 'W'}
    int2dz = {1: (0, -1), 2: (1, 0), 3: (0, 1), 4: (-1, 0)}
    my_directions = []

    my_dirs = [cell.has_walls(my_dir) for my_dir in ['N', 'E', 'S', 'W']]
    for idx, val in enumerate(my_dirs):
        if val is False:
            my_directions.append(idx)

    n = len(my_directions)
    if n > 1:
        make_branch(cell, my_directions, visited_find, start, end)
    else:
        idx = 0
        my_dir_int = my_directions[idx]
        my_dir = int2dir[my_dir_int]
        my_dz = int2dz[my_dir_int]

    # Move in the chosen direction
    new_cell = maze[cell.x + my_dz[0]][cell.y + my_dz[1]]
    # "Recurse"
    visited_find.append(new_cell)
    find_recursion(new_cell, visited_find)
    pass


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

    cell = maze[start[0]][start[1]]
    print(f"Starting cell is ({start[0]},{start[1]})")

    # Implement a stack for backtracking, tracking visited cells
    visited_find = deque()
    visited_find.append(cell)

    find_recursion(cell, visited_find, start, end)
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
