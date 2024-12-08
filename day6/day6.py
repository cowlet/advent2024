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

def find_items(grid, items):
    locations = []
    for i, line in enumerate(grid):
        for j, ch in enumerate(line):
            if ch in items:
                locations.append([i, j])
    return locations

def trace_path(grid):
    locs = find_items(grid, guard)
    if len(locs) != 1:
        raise AttributeError(f"Wrong number of guards! {len(locs)}")
    gi, gj = locs[0][0], locs[0][1]
    on_grid = True

    obstacles = find_items(grid, "#O")
    obstacles = [Obstacle(loc[0], loc[1]) for loc in obstacles]

    obstacles_hit = [] # Check for loops
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

    if grid[new_i][new_j] in "#O":
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

# Read the orig grid and try every position in the guard's path
base_grid = [list(line.strip()) for line in lines]
locs = find_items(base_grid, guard)
if len(locs) != 1:
    print(f"Wrong number of guards at the start! {len(locs)}")
orig_gi, orig_gj = locs[0][0], locs[0][1]
orig_gd = base_grid[orig_gi][orig_gj]
gi, gj = orig_gi, orig_gj
on_grid = True

new_obs = []
while on_grid:
    future_grid, new_i, new_j, new_on_grid, _ = step(gi, gj, base_grid)
    # If we step off the grid, can't place an obstacle there
    # If both coords are the same, we've hit an obstacle already, so loop
    # If we're at the original guard position, can't place
    if new_on_grid and (new_i != gi or new_j != gj) and \
            (new_i != orig_gi or new_j != orig_gj):
        #print(f"Testing object at ({new_i}, {new_j})")
        # Make a blank grid
        hypo_grid = make_blank_grid(lines)
        # Place the guard at original spot, so we know the object doesn't
        # interfere with path to here
        hypo_grid[orig_gi][orig_gj] = orig_gd
        # Place an obstacle at new_i, new_j
        hypo_grid[new_i][new_j] = "O"

        # trace_path
        try:
            new_grid, _, _ = trace_path(hypo_grid)
            #print(f"--> No loop, so drop obstacle ({new_i},{new_j})")
        except ValueError:
            # If we hit a loop exception, we completed the path!
            obs = Obstacle(new_i, new_j)
            #print(f"Valid new object at {obs}")
            new_obs.append(obs)
    # Actually advance the guard on the base grid, regardless of
    # whether we tested an obstacle or not
    base_grid = future_grid
    gi, gj = new_i, new_j
    on_grid = new_on_grid

# Filter out dups
uniq = []
for obs in new_obs:
    # Only location matters now, not heading
    match = [1 for it in uniq if it.i==obs.i and it.j==obs.j]
    if len(match) == 0:
        uniq.append(obs)
print(f"Possible objects to place: {len(new_obs)}, uniques: {len(uniq)}")

