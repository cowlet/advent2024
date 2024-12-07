import itertools

guard = "^>v<"

class Obstacle:
    def __init__(self, i, j, side=None):
        self.i = i
        self.j = j
        self.side = side

    def __str__(self):
        if self.side:
            return f"[({self.i}, {self.j}): {self.side}]"
        return f"[({self.i}, {self.j})]"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j and self.side == other.side

def make_blank_grid(lines):
    grid = [list(line.strip()) for line in lines]
    for i, line in enumerate(grid):
        for j, ch in enumerate(line):
            if ch in guard:
                grid[i][j] = "."
    return grid

def trace_path(grid):
    gi, gj = 0, 0
    obstacles = []
    for i, line in enumerate(grid):
        for j, ch in enumerate(line):
            if ch in guard:
                gi, gj = i, j
            if ch == "#":
                obstacles.append(Obstacle(i, j))

    # Did we really find the guard, or did we run out of board?
    on_grid = True
    if grid[gi][gj] not in guard:
        print(f"*** Error: Could not find the guard at the start!! ***")
        raise AttributeError("No guard")
        on_grid = False

    obstacles_hit = []
    while on_grid:
        grid, gi, gj, on_grid, obs = step(gi, gj, grid)
        if obs:
            if obs in obstacles_hit:
                raise ValueError("Loop!")
            obstacles_hit.append(obs)

    return grid, obstacles, obstacles_hit


def step(i, j, grid):
    obs = None # Obstacles hit
    r = len(grid)
    c = len(grid[0])

    if grid[i][j] == "^":
        new_i, new_j = i-1, j
    elif grid[i][j] == "v":
        new_i, new_j = i+1, j
    elif grid[i][j] == "<":
        new_i, new_j = i, j-1
    elif grid[i][j] == ">":
        new_i, new_j = i, j+1
    else:
        print(f"Lost the guard! ({i}, {j}) == {grid[i][j]}")
        return grid, i, j, False, obs

    if new_i < 0 or new_i >= c or new_j < 0 or new_j >= r:
        #print(f"Guard exited the grid at ({new_i}, {new_j})")
        return grid, new_i, new_j, False, obs

    if grid[new_i][new_j] == "#":
        obs = Obstacle(new_i, new_j, grid[i][j]) # Save for later
        # Stay in place and rotate
        idx = guard.index(grid[i][j]) + 1
        if idx >= len(guard):
            idx = 0
        grid[i][j] = guard[idx]
        new_i, new_j = i, j

    #print(f"Taking a step to ({new_i}, {new_j})")
    grid[new_i][new_j] = grid[i][j]

    return grid, new_i, new_j, True, obs


#with open("d6_test.txt", "r") as f:
with open("d6_input.txt", "r") as f:
    lines = f.readlines()

grid = [list(line.strip()) for line in lines]
#for row in grid:
#    print("".join(row))


# Reset the grid and try every position in the guard's path
base_grid = [list(line.strip()) for line in lines]
gi, gj = 0, 0
for i, line in enumerate(base_grid):
    for j, ch in enumerate(line):
        if ch in guard:
            gi, gj = i, j
on_grid = True
new_obs = []
while on_grid:
    future_grid, new_i, new_j, new_on_grid, _ = step(gi, gj, base_grid)
    #print(gi, gj, new_i, new_j, on_grid)
    if new_on_grid and (new_i != gi or new_j != gj):
        # If coords are the same, we've hit an obstacle already. Step again.
        #print(f"Testing object at ({new_i}, {new_j})")
        # Make a blank grid
        hypo_grid = make_blank_grid(lines)
        # Place the guard at gi, gj in same heading
        hypo_grid[gi][gj] = base_grid[gi][gj]
        # Place an obstacle at new_i, new_j
        hypo_grid[new_i][new_j] = "#"
        #for row in hypo_grid:
        #    print("".join(row))
        # trace_path
        try:
            _, _, _ = trace_path(hypo_grid)
            #print(f"--> No loop, so drop obstacle ({new_i},{new_j})")
        except ValueError:
            # If we hit a loop exception, we completed the path!
            obs = Obstacle(new_i, new_j)
            #print(f"Valid new object at {obs}")
            new_obs.append(obs)
            #for row in hypo_grid:
            #    print("".join(row))
    # Actually advance the guard on the base grid
    base_grid = future_grid
    gi, gj = new_i, new_j
    on_grid = new_on_grid
    #print(f"*** After testing, true grid is ***")
    #for row in base_grid:
    #    print("".join(row))


print(f"Possible objects to place: {len(new_obs)}")
#for p in new_obs:
#    print(p)
